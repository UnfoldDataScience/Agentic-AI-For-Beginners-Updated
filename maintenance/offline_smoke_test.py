"""Offline smoke test: runs the credential-free parts of every lesson without any paid API calls.

Run from the course folder:
    uv run --group dev python maintenance/offline_smoke_test.py

What it does
  * Executes each notebook in a fresh kernel, top to bottom, with dummy API keys and all network
    traffic routed to an unreachable proxy (so nothing can reach OpenAI, Groq, AWS, search engines...).
  * Statements that call a live service (LLM calls, crew kickoffs, Bedrock calls, ...) are skipped,
    together with any later statement that uses their results. Everything else - imports, prompt
    templates, agent/tool/crew/team construction, configuration - really runs.
  * Checks a few expected objects per notebook, tests the Lambda handlers with sample events,
    and drives both Streamlit apps with Streamlit's AppTest.

Passing this test does NOT prove that the live services work. See LIVE_VALIDATION.md for live tests.
"""
import ast
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]

# Calls that would reach a paid or external service.
LIVE_CALL = re.compile(
    r"\.(invoke|run|kickoff|print_response|generate_reply|converse|invoke_agent|assume_role)\("
    r"|\binitiate_chats\("
)

# Expressions evaluated at the end of each notebook (must all be True).
EXPECT = {
    "Part1/Basic_Agent.ipynb": [
        "formatted_prompt == 'Hello, David! How can I help you today?'",
        "chat_model.model_name == 'gpt-4o-mini'",
        "type(chain).__name__ == 'LLMChain'",
        "search_tool.name == 'duckduckgo_search'",
        "search_with_fallback('offline query').startswith('Search failed')",
        "type(agent).__name__ == 'AgentExecutor'",
        "sorted(t.name for t in agent.tools) == ['Summarizer', 'duckduckgo_search']",
    ],
    "Part2/First_Multi_Agent.ipynb": [
        "type(crewaman).__name__ == 'Crew'",
        "[a.role for a in crewaman.agents] == ['chef', 'nutritionist']",
        "os.environ['OPENAI_MODEL_NAME'] == 'gpt-4o-mini'",
    ],
    "Part2/CustomerServiceMAS.ipynb": [
        "type(crewCSMAS).__name__ == 'Crew'",
        "customer_query_task.tools[0].website_url == 'https://docs.crewai.com/introduction'",
        "bool(crewCSMAS.memory)",
    ],
    "Part3/Investment_Analysis_Agentic_System.ipynb": [
        "type(investment_analysis_team).__name__ == 'Team'",
        "len(investment_analysis_team.members) == 4",
        "any(type(t).__name__ == 'DuckDuckGoTools' for t in market_sentiment_bot.tools)",
    ],
    "Part3/MAS_Using_MSAutogen.ipynb": [
        "config_list[0]['model'] == 'openai/gpt-oss-120b'",
        "all(c['summary_args']['summary_role'] == 'user' for c in conversation_flow)",
        "relay_agent.human_input_mode == 'ALWAYS'",
        "len(conversation_flow) == 3",
    ],
    "Part4/Intro_to_AwsBedrock.ipynb": [
        "bedrock_runtime.meta.region_name == 'us-east-1'",
        "kwargs['modelId'] == 'amazon.titan-text-express-v1'",
    ],
    "Part4/Running_first_AWS_BedrockAgent.ipynb": [
        "AGENT_ID == 'TESTAGENT1' and AGENT_ALIAS_ID == 'TESTALIAS1'",
        "sts_client.meta.region_name == 'us-east-1'",
    ],
}


def offline_env(workdir):
    env = dict(os.environ)
    blackhole = "http://127.0.0.1:9"  # nothing listens here: any network call fails fast
    env.update({
        "HTTP_PROXY": blackhole, "HTTPS_PROXY": blackhole, "ALL_PROXY": blackhole,
        "http_proxy": blackhole, "https_proxy": blackhole, "NO_PROXY": "", "no_proxy": "",
        # Dummy credentials - real values are never needed and must never be loaded.
        "OPENAI_API_KEY": "offline-test-dummy-key", "GROQ_API_KEY": "gsk-offline-test",
        "TAVILY_API_KEY": "", "GROQ_MODEL": "", "BEDROCK_MODEL_ID": "", "AWS_REGION": "us-east-1",
        "BEDROCK_AGENT_ID": "TESTAGENT1", "BEDROCK_AGENT_ALIAS_ID": "TESTALIAS1",
        "BEDROCK_INVOKE_ROLE_ARN": "arn:aws:iam::<account-id>:role/offline-test",
        "LANGFLOW_APPLICATION_TOKEN": "", "LANGFLOW_ID": "", "LANGFLOW_FLOW_ID": "", "LANGFLOW_BASE_URL": "",
        "AWS_ACCESS_KEY_ID": "offline-test", "AWS_SECRET_ACCESS_KEY": "offline-test",
        "AWS_CONFIG_FILE": str(workdir / "no-aws-config"), "AWS_SHARED_CREDENTIALS_FILE": str(workdir / "no-aws-creds"),
        "AWS_EC2_METADATA_DISABLED": "true",
        # Framework telemetry and local storage
        "OTEL_SDK_DISABLED": "true", "CREWAI_DISABLE_TELEMETRY": "true", "AGNO_TELEMETRY": "false",
        "ANONYMIZED_TELEMETRY": "false", "CREWAI_STORAGE_DIR": str(workdir / "crewai"),
    })
    return env


def names(node, ctx):
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ctx)}


def offline_source(source, tainted):
    """Drop live-call statements and statements that depend on them; return (code, skipped list)."""
    lines = source.splitlines()
    if any(l.lstrip().startswith(("%", "!")) for l in lines):
        return "", ["notebook magic"]
    tree = ast.parse(source)
    kept, skipped = [], []
    for stmt in tree.body:
        segment = ast.get_source_segment(source, stmt)
        is_def = isinstance(stmt, (ast.FunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom))
        if not is_def and (LIVE_CALL.search(segment) or names(stmt, ast.Load) & tainted):
            tainted |= names(stmt, ast.Store)
            skipped.append(segment.splitlines()[0][:70])
        else:
            kept.append(segment)
    return "\n".join(kept), skipped


def run_notebook(rel):
    nb = nbformat.read(ROOT / rel, as_version=4)
    tainted, report = set(), []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        code, skipped = offline_source(cell.source, tainted)
        cell.source = code or "pass"
        if skipped:
            report.append(f"cell {i}: skipped {skipped}")
    checks = EXPECT[rel]
    nb.cells.append(nbformat.v4.new_code_cell(
        "import os\n_failed = [c for c in %r if not eval(c)]\n"
        "assert not _failed, f'Expectation failed: {_failed}'\nprint('expectations passed:', %d)" % (checks, len(checks))))
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        client = NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": tmp}})
        env_backup = dict(os.environ)
        os.environ.update(offline_env(workdir))  # inherited by the kernel process
        try:
            client.execute()
        finally:
            os.environ.clear()
            os.environ.update(env_backup)
    return report


def test_lambdas():
    results = []
    for module_name, params, expected in [
        ("MapCourseRecommendationFunction", [{"name": "years_experience", "value": "4"}], "Intermediate Machine Learning"),
        ("MapCourseRecommendationFunction", [{"name": "years_experience", "value": "two"}], "Data Science Fundamentals"),
        ("ProvideCourseReasoningPythonFunction",
         [{"name": "years_experience", "value": "7"}, {"name": "recommended_course", "value": "Advanced Deep Learning and AI"}],
         "Advanced Deep Learning and AI course"),
    ]:
        spec = importlib.util.spec_from_file_location(module_name, ROOT / "Part4" / f"{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        event = {"agent": {}, "actionGroup": "group", "function": "fn", "parameters": params, "messageVersion": "1.0"}
        body = module.lambda_handler(event, None)["response"]["functionResponse"]["responseBody"]["TEXT"]["body"]
        assert expected in body, (module_name, params, body)
        results.append(f"{module_name}({params[0]['value']!r}) ok")
    return results


def test_streamlit_apps():
    from streamlit.testing.v1 import AppTest

    with tempfile.TemporaryDirectory() as tmp:
        backup = dict(os.environ)
        os.environ.update(offline_env(Path(tmp)))
        try:
            at = AppTest.from_file(str(ROOT / "Part4" / "Basic_SL.py")).run()
            at.text_input[0].input("Ada").run()
            assert any("Hello, Ada!" in m.value for m in at.markdown), "Basic_SL greeting missing"

            ui = ROOT / "Part4" / "Call_AWS_Agent_through_UI.py"
            for key in ("BEDROCK_AGENT_ID", "BEDROCK_AGENT_ALIAS_ID"):
                os.environ[key] = ""
            at = AppTest.from_file(str(ui)).run()
            assert at.error and "BEDROCK_AGENT_ID" in at.error[0].value, "missing-config message not shown"

            os.environ.update({"BEDROCK_AGENT_ID": "TESTAGENT1", "BEDROCK_AGENT_ALIAS_ID": "TESTALIAS1"})
            at = AppTest.from_file(str(ui), default_timeout=120).run()
            assert not at.exception and at.title[0].value == "Bedrock Agent Chat"
            at.button[0].click().run()  # empty input: must not call the agent
            assert not at.error and not at.text, "empty message should not call the agent"
            at.text_input[0].input("Hello").run()
            at.button[0].click().run()  # network is blocked: the error must appear in the chat history
            chat = [t.value for t in at.text]
            assert chat[:1] == ["You: Hello"] and chat[1].startswith("Agent: Error:"), chat
        finally:
            os.environ.clear()
            os.environ.update(backup)
    return ["Basic_SL.py ok", "Call_AWS_Agent_through_UI.py ok (config check, empty input, error handling)"]


def test_dotenv_discovery():
    """The notebooks call load_dotenv(): a .env in the course folder must be found from a PartN folder."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / ".env").write_text("COURSE_DOTENV_CHECK=found\n", encoding="utf-8")
        part_dir = Path(tmp) / "Part1"
        part_dir.mkdir()
        nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
            "import os\nfrom dotenv import load_dotenv\nload_dotenv()\n"
            "assert os.getenv('COURSE_DOTENV_CHECK') == 'found'")])
        NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(part_dir)}}).execute()
    return [".env in the course folder is found from a Part folder"]


def test_langflow_cli():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run([sys.executable, str(ROOT / "Part3" / "Langflow" / "TestMyAgent.py"), "hi"],
                                cwd=tmp, env=offline_env(Path(tmp)), capture_output=True, text=True, timeout=120)
    assert result.returncode == 2 and "LANGFLOW_ID" in result.stderr, result.stderr
    return ["TestMyAgent.py reports missing settings ok"]


def main():
    failures = 0
    for rel in EXPECT:
        print(f"\n== {rel}")
        try:
            for line in run_notebook(rel):
                print("  ", line)
            print("   PASS")
        except Exception as e:  # report and continue with the next lesson
            failures += 1
            print("   FAIL:", str(e).strip().splitlines()[-1][:500] if str(e).strip() else repr(e))
    for name, test in [("Lambda handlers", test_lambdas), ("Streamlit apps", test_streamlit_apps),
                       ("Langflow client", test_langflow_cli), (".env discovery", test_dotenv_discovery)]:
        print(f"\n== {name}")
        try:
            for line in test():
                print("  ", line)
            print("   PASS")
        except Exception as e:
            failures += 1
            print("   FAIL:", repr(e)[:500])
    print(f"\n{failures} failure(s)." if failures else "\nAll offline smoke tests passed.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
