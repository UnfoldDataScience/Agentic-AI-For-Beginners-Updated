# Part 3 - Agent Teams with Agno, AutoGen and Langflow

| Notebook / file | What it shows |
|---|---|
| `Investment_Analysis_Agentic_System.ipynb` | A team of specialist agents (news sentiment, financial data, deep financials, strategy) coordinated by a team leader, using Agno (formerly phidata) |
| `MAS_Using_MSAutogen.ipynb` | Microsoft AutoGen: conversable, assistant and user-proxy agents in a sequence of chats with structured JSON summaries |
| `Langflow/TestMyAgent.py` | Calling the agent you built in Langflow through its API |

---

# API Keys and Settings

| Key | Used by | Required? | Create it here |
|---|---|---|---|
| `OPENAI_API_KEY` | Investment analysis | Required | https://platform.openai.com/api-keys |
| `GROQ_API_KEY` | AutoGen | Required | https://console.groq.com/keys (free tier) |
| `GROQ_MODEL` | AutoGen | Optional (default `openai/gpt-oss-120b`) | https://console.groq.com/docs/models |
| `LANGFLOW_APPLICATION_TOKEN`, `LANGFLOW_ID`, `LANGFLOW_FLOW_ID` | `TestMyAgent.py` | Required for that script | Your flow's *API* panel in Langflow |

---

# Run the Notebooks and Script

1. Set up the course environment once (see `LOCAL_SETUP.MD` in the course folder, or `BEGINNER_SETUP.md` if you are new to coding): `uv sync`
2. Copy `.env.example` to `.env` in the course folder and add your keys.
3. Open a notebook and select the **`.venv`** kernel (Python 3.12). Run the cells from top to bottom.
4. Langflow script, from the course folder: `uv run python Part3/Langflow/TestMyAgent.py "What is 2+2?"`

---

# Differences from the Recorded Lessons

Explained inside each notebook:

* **Investment analysis:** `phidata` is now called **Agno** (`phi.*` → `agno.*`, `Calculator` → `CalculatorTools`), and the team uses Agno's `Team` class. News search now uses **`DuckDuckGoTools`** instead of Google search and Yahoo Finance news, which no longer return results. The prompt analyses the most recent month instead of January 2025.
* **AutoGen:** the recorded Groq model `llama-3.3-70b-versatile` is no longer offered, so the default is `openai/gpt-oss-120b` (change it with `GROQ_MODEL`); summaries are requested with `summary_role: "user"`; the agent explanations are now Markdown cells; no OpenAI key is needed.
* **Langflow:** your token and flow IDs come from `.env` instead of being written in the script.

Yahoo Finance data and DuckDuckGo results are fetched live and can be rate-limited. Re-run later if a tool reports an error. Educational example only - not financial advice.

---

# Included Files

* `Investment_Analysis_Agentic_System.ipynb`, `MAS_Using_MSAutogen.ipynb` - the lesson notebooks
* `Langflow/TestMyAgent.py` - Langflow API client
* `fibonacci_series.py` - small example code file (not used by the notebooks)

---

# Tested Environment

Last updated: November 2026 - Python 3.12, Agno 1.8, AutoGen (pyautogen) 0.2.35.

Happy Learning!
