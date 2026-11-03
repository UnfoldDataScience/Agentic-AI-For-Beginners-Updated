# Part 2 - Multi-Agent Systems with CrewAI

Build crews of agents with roles, goals and backstories, give them tasks and tools, and let them collaborate.

| Notebook | What it shows |
|---|---|
| `First_Multi_Agent.ipynb` | A chef and a nutritionist collaborate on recipes |
| `CustomerServiceMAS.ipynb` | Two-level customer support with a web-scraping tool and crew memory |

---

# API Keys

| Key | Required? | Create it here |
|---|---|---|
| `OPENAI_API_KEY` | Required | https://platform.openai.com/api-keys |

No Serper key is needed.

---

# Run the Notebooks

1. Set up the course environment once (see `LOCAL_SETUP.MD` in the course folder, or `BEGINNER_SETUP.md` if you are new to coding): `uv sync`
2. Copy `.env.example` to `.env` in the course folder and add your key.
3. Open a notebook and select the **`.venv`** kernel (Python 3.12).
4. Run the cells from top to bottom.

---

# Differences from the Recorded Lesson

The recorded CrewAI 0.28 can no longer be installed (its tools package depends on `lancedb` versions that were removed from PyPI), so these notebooks use **CrewAI 1.x**. Agents, tasks, crews, tools and `{placeholders}` work the same way. Details are explained inside each notebook:

* `verbose=2` → `verbose=True`, and the console output looks different
* `First_Multi_Agent.ipynb` uses `gpt-4o-mini` instead of the far more expensive `gpt-4`
* `CustomerServiceMAS.ipynb` uses CrewAI's default model (`gpt-4.1-mini`); `memory=True` also makes OpenAI embedding calls and stores memory files on your computer

---

# Included Files

* `First_Multi_Agent.ipynb`, `CustomerServiceMAS.ipynb` - the lesson notebooks

---

# Tested Environment

Last updated: November 2026 - Python 3.12, CrewAI 1.14.

Happy Learning!
