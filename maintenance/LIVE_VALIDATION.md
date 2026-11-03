# Live Validation Checklist (local)

Manual release check: run each notebook with real keys, in the course `.venv`, the way a student would.
The offline checks (`check_repo.py`, `offline_smoke_test.py`) cannot catch API, model or rate-limit changes.

Record each result as **Pass**, **Fail** (paste the error message, never a key) or **N/A**.

## 0. One-time preparation

| # | Step | Expected |
|---|---|---|
| 0.1 | Start from a clean environment: delete `.venv`, then run `uv sync` in the course folder. | Completes without errors and creates `.venv` with Python 3.12. |
| 0.2 | Check your OpenAI usage page and note today's spend. You will compare it afterwards. Prefer keys with low spending limits. | - |
| 0.3 | Put `OPENAI_API_KEY` and `GROQ_API_KEY` in `.env` (copied from `.env.example`). `TAVILY_API_KEY` is optional. | - |

## 1. Steps for every notebook

Run them in this order: Part 1, Part 2 (`First_Multi_Agent`, then `CustomerServiceMAS`), Part 3 (`MAS_Using_MSAutogen`, then `Investment_Analysis_Agentic_System`).

| # | Step | Expected result |
|---|---|---|
| 1.1 | Open the notebook in VS Code and select the **`.venv`** kernel. *Restart* the kernel so the run starts fresh. | The *How to run* and *Compatibility update* sections are shown. |
| 1.2 | Run the **setup check cell** (the first code cell). | `Ready: course .venv kernel \| Python 3.12.x` |
| 1.3 | Run the **key cell**. | `All required API keys are loaded.` |
| 1.4 | Run the remaining cells from top to bottom. | No error tracebacks. Check the demonstration listed in section 2. |
| 1.5 | **Negative tests** (once, on the Part 1 notebook only): (a) select a different Python kernel and run the setup check cell; (b) rename `OPENAI_API_KEY` in `.env`, restart the kernel and run the key cell. | (a) A warning that tells the student to select the `.venv` kernel. (b) `Missing required keys: OPENAI_API_KEY - see 'How to run this notebook' above.` Undo both afterwards. |

## 2. Notebook-specific checks

| Notebook | Keys | First meaningful demonstration | Full-run expectations | Approx. cost |
|---|---|---|---|---|
| `Part1/Basic_Agent.ipynb` | `OPENAI_API_KEY` (optional `TAVILY_API_KEY`) | The chat-model cell prints the capital of the USA (Washington, D.C.). | The chain lists Deep Learning topics. Both agent cells show `Action: duckduckgo_search` (or `tavily_search`) and end with `Final Answer:`. The last cell shows the langchain and openai versions. **Known risk:** DuckDuckGo may rate-limit. Record any `DDGSException` and repeat once with a `TAVILY_API_KEY`. | < $0.01 |
| `Part2/First_Multi_Agent.ipynb` | `OPENAI_API_KEY` | `kickoff` shows the chef agent's task output (5 chicken recipes). | Then the nutritionist's analysis. The last cell prints the recommended recipe. | < $0.01 |
| `Part2/CustomerServiceMAS.ipynb` | `OPENAI_API_KEY` | `kickoff` shows the support agent using **Read website content** on docs.crewai.com. | Then the quality-checked reply. The last cell prints a reply addressed to Unfold Data Science about Crews and Agents. Note any memory or embedding errors. | about $0.01-0.05 |
| `Part3/MAS_Using_MSAutogen.ipynb` | `GROQ_API_KEY` (optional `GROQ_MODEL`) | `Using Groq model: openai/gpt-oss-120b`, then a joke. | `initiate_chats` asks for **your input** in a text box. Type, in turn: your name, company and product of interest; a follow-up question; "Yes, I would like to proceed"; then "exit" when asked again. The last cell prints three summaries: **check that they are non-empty JSON-like text**. | Groq free tier, or cents |
| `Part3/Investment_Analysis_Agentic_System.ipynb` | `OPENAI_API_KEY` | The calculator agent shows step-by-step tool calls and the answer **2500**. | The team response streams with member tool calls, tables, sentiment scores and a BUY/SELL/HOLD recommendation for AMD and TSM. The sentiment section cites recent news (DuckDuckGo news). Record any DuckDuckGo or Yahoo Finance errors (rate limits). | about $0.10-0.50 |
| `Part4/*.ipynb`, `Part4/Call_AWS_Agent_through_UI.py` | Your AWS account (`aws configure`) and the Part 4 settings in `.env` | Model answer from Bedrock. | Agent response events; the chat UI replies. | AWS pricing |
| `Part3/Langflow/TestMyAgent.py` | Langflow settings in `.env` | JSON response from your flow. | - | - |

## 3. Things to watch and record

- **`uv sync` time and errors** on a clean machine, especially on Windows (long-path errors, see `LOCAL_SETUP.MD` Step 2).
- **Python version:** the setup check cell must report 3.12.
- **Spend:** compare your OpenAI usage page with step 0.2 afterwards. The total should be well under $1.

## 4. After the check

Clear the notebook outputs before committing (committed notebooks have no outputs). Update the *Last updated* line
only for notebooks that passed. Record failures with the error text in an issue or in the maintainer notes.
