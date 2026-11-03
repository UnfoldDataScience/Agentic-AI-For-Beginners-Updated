# Maintaining the Course Repository

Student setup lives in `BEGINNER_SETUP.md` (new to coding) and `LOCAL_SETUP.MD`. This page is for course maintainers.

The course runs **locally only**, in one `uv` environment. There is no Google Colab version: notebooks contain
no install cells, no Colab links and no Colab Secrets code (`check_repo.py` enforces this).

## Single source of truth

| What | Source | Generated from it |
|---|---|---|
| Package versions | `pyproject.toml` + `uv.lock` | - |
| Lessons | One notebook per lesson (original filenames) | - |
| Settings and keys | `.env.example` (placeholders only) | - |

`uv sync` is the only supported setup path. There are no `requirements.txt` files to keep in sync.

## Updating dependencies

```bash
uv lock --upgrade-package <package>     # or: uv lock --upgrade
uv sync --group dev
uv run --group dev python maintenance/check_repo.py           # must print "All checks passed."
uv run --group dev python maintenance/offline_smoke_test.py   # must print "All offline smoke tests passed."
```

Then run the live tests below for the lessons whose packages changed, and update the *Last updated* lines.

Known constraint: `pyautogen==0.2.35` (Part 3) needs `numpy<2`, so `pyarrow` is held below 25 in
`[tool.uv] constraint-dependencies`. Remove both together if AutoGen is upgraded.

## What the checks do not cover

The offline tests block all network traffic and skip every live LLM, search, market-data or AWS call.
Before a release, run each notebook top to bottom with real keys in the course `.venv`
and check that the results match the lesson's intent (step-by-step checklist: `LIVE_VALIDATION.md`):

| Notebook | Live services | Expected result |
|---|---|---|
| `Part1/Basic_Agent.ipynb` | OpenAI, DuckDuckGo (or Tavily) | Prompt, chat and chain answers; agent traces using the search and summarizer tools |
| `Part2/First_Multi_Agent.ipynb` | OpenAI | Five chicken recipes, then a nutritionist recommendation |
| `Part2/CustomerServiceMAS.ipynb` | OpenAI (chat + embeddings), docs.crewai.com | Scraped-docs answer, then a quality-checked reply |
| `Part3/Investment_Analysis_Agentic_System.ipynb` | OpenAI, DuckDuckGo (news), Yahoo Finance | Calculator steps; team report with tables and BUY/SELL/HOLD |
| `Part3/MAS_Using_MSAutogen.ipynb` | Groq (interactive) | Joke; three chats; JSON summaries printed per step |
| `Part4/*.ipynb`, `Part4/Call_AWS_Agent_through_UI.py` | AWS Bedrock, STS, Lambda | Model answer; agent response events; chat UI replies |
| `Part3/Langflow/TestMyAgent.py` | Langflow | JSON response from your flow |
