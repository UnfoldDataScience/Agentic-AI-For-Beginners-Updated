# Part 1 - Building Your First AI Agent

Learn the LangChain building blocks of an agent: prompt templates, chat models, LLM chains, tools and a ReAct agent that searches the web.

| Notebook | What it shows |
|---|---|
| `Basic_Agent.ipynb` | Prompt templates, chat models, LLM chains, and a ReAct agent with web search and a summarizer tool |

---

# API Keys

| Key | Required? | Create it here |
|---|---|---|
| `OPENAI_API_KEY` | Required | https://platform.openai.com/api-keys |
| `TAVILY_API_KEY` | Optional - only if DuckDuckGo search is rate-limited | https://app.tavily.com/home |

DuckDuckGo search needs no key.

---

# Run the Notebook

1. Set up the course environment once (see `LOCAL_SETUP.MD` in the course folder, or `BEGINNER_SETUP.md` if you are new to coding): `uv sync`
2. Copy `.env.example` to `.env` in the course folder and add your keys.
3. Open `Basic_Agent.ipynb` and select the **`.venv`** kernel (Python 3.12).
4. Run the cells from top to bottom.

---

# Differences from the Recorded Lesson

The concepts and flow are unchanged. Small compatibility updates are explained inside the notebook:

* `gpt-3.5-turbo` models → `gpt-4o-mini`
* `ChatOpenAI` is imported from `langchain_openai`
* `.run(...)` → `.invoke(...)`
* Optional Tavily search if DuckDuckGo is rate-limited

---

# Included Files

* `Basic_Agent.ipynb` - the lesson notebook

---

# Tested Environment

Last updated: November 2026 - Python 3.12, LangChain 0.3.

Happy Learning!
