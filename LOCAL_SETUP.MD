# Local Development Environment Setup

This guide sets up **one Python environment for the whole course**. You do it once, and every notebook and script in Parts 1-4 runs in it.

> **Python version:** 3.12 (uv installs it for you)
>
> **Last Updated:** November 2026

New to coding or to the terminal? Follow [`BEGINNER_SETUP.md`](BEGINNER_SETUP.md) instead. It covers the same steps in more detail.

---

# Quick Start

```bash
# 1. Install uv (one time) - see Step 1 for Windows
# 2. In a terminal, go to the course folder (the folder that contains pyproject.toml)
cd path/to/Agentic-AI-For-Beginners-Updated
# 3. Create the environment (installs Python 3.12 and all packages into .venv)
uv sync
# 4. Create your settings file, then add your API keys to it
cp .env.example .env            # Windows PowerShell: Copy-Item .env.example .env
```

Then open a notebook in VS Code, select the **`.venv`** kernel, and run the cells from top to bottom.

---

# Step 1 - Install uv

[uv](https://docs.astral.sh/uv/) is a fast tool that installs the right Python version and the exact package versions this course was tested with.

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen your terminal, then check:

```bash
uv --version
```

You do **not** need to install Python separately - `uv sync` downloads Python 3.12 automatically if it is missing.

---

# Step 2 - Get the Course Files

Download the course repository (from Udemy or GitHub) and extract it.

> **Windows: keep the folder path short.** Some packages contain very long file names. Windows limits full paths
> to 260 characters, so use a short location such as `C:\courses\Agentic-AI-For-Beginners-Updated`.
> Avoid deeply nested folders (for example inside OneDrive). If installation fails with *"The system cannot find the
> path specified"*, move the folder to a shorter path, delete the `.venv` folder, and run `uv sync` again.

---

# Step 3 - Create the Environment

Open a terminal **in the course folder** (the folder that contains `pyproject.toml` and `uv.lock`).

In VS Code: *File → Open Folder…* → select the course folder, then *Terminal → New Terminal*.

```bash
uv sync
```

This creates a `.venv` folder with Python 3.12 and every package used in Parts 1-4. The first run takes a few minutes.

---

# Step 4 - Add Your API Keys

Copy the example settings file and fill in your own keys:

```bash
cp .env.example .env                 # macOS / Linux
Copy-Item .env.example .env          # Windows PowerShell
```

Open `.env` in a text editor. You only need the keys for the lessons you run - each Part's `readme.md` lists them.
See `Managing_Secrets.md` for how to create an OpenAI key and keep it safe.

The notebooks find `.env` automatically (in the notebook's folder or any parent folder). You never need to type a file path.

---

# Step 5 - Install VS Code and Its Extensions

1. Install Visual Studio Code: https://code.visualstudio.com/
2. Open the Extensions view (`Ctrl + Shift + X`) and install **Python** and **Jupyter** (both published by Microsoft).

Any Jupyter-compatible editor works. From the terminal you can also run `uv run --with jupyter jupyter lab`.

---

# Step 6 - Open a Notebook and Select the Kernel

1. Open a notebook, for example `Part1/Basic_Agent.ipynb`.
2. Click **Select Kernel** (top right) → *Python Environments* → choose **`.venv` (Python 3.12)**.
3. Run the cells from top to bottom. The first code cell prints `Ready: course .venv kernel | Python 3.12...`
   (if it prints a warning instead, you selected the wrong kernel).
   The second cell confirms that your API keys were loaded.

The same `.venv` kernel is used for **every** notebook in the course.

---

# Running the Python Scripts

Run scripts from the course folder with `uv run`, which always uses the course environment:

```bash
uv run python Part3/Langflow/TestMyAgent.py "What is 2+2?"
uv run streamlit run Part4/Basic_SL.py
uv run streamlit run Part4/Call_AWS_Agent_through_UI.py
```

---

# Troubleshooting

## `uv` is not recognized

Close and reopen the terminal (or VS Code) after installing uv. On Windows you may need to sign out and back in.

## Installation fails with "The system cannot find the path specified" (Windows)

The course folder path is too long - see Step 2.

## The `.venv` kernel is not listed in VS Code

Make sure you opened the **course folder** in VS Code (not a single Part folder) and that `uv sync` finished. Then run *Python: Select Interpreter* (`Ctrl + Shift + P`) and choose `.venv`. Restart VS Code if it still does not appear.

## "Missing required keys" in the second cell

Check that your file is named exactly `.env` (no `.txt` extension), that it is in the course folder, and that the key names match `.env.example`. Restart the kernel after editing `.env`.

## `ModuleNotFoundError`

The notebook is using the wrong kernel. Select the `.venv` kernel (Step 6) and restart it.

---

# Frequently Asked Questions

### Do I need a new environment for every section?

No. One `.venv` works for the whole course.

### Can I use PyCharm, Jupyter Lab or Anaconda?

Yes. Create the environment with `uv sync` as described above, then point your editor at the course `.venv` interpreter.
Do not install the course packages with pip or conda: `uv sync` is the only tested way to get the exact package versions.

### How do I update to a newer version of the course?

Download the new course files and run `uv sync` again in the course folder.

### Do the AI libraries send usage data?

CrewAI, Agno and ChromaDB send anonymous usage statistics by default. To turn this off, add these lines to your `.env` file. They are already included, commented out, in `.env.example`:

```
CREWAI_DISABLE_TELEMETRY=true
AGNO_TELEMETRY=false
ANONYMIZED_TELEMETRY=False
```

| Library (version in this course) | Setting | Notes |
|---|---|---|
| CrewAI 1.14 (Part 2) | `CREWAI_DISABLE_TELEMETRY=true` | `OTEL_SDK_DISABLED=true` also works, but it turns off all OpenTelemetry. CrewAI's detailed execution traces are a separate feature, and they are off unless you enable them. |
| Agno 1.8 (Part 3) | `AGNO_TELEMETRY=false` | |
| ChromaDB 1.1 (installed with CrewAI) | `ANONYMIZED_TELEMETRY=False` | CrewAI already turns this off for the databases it creates itself. |

---

Happy Learning!
