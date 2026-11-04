# Setup Guide for Beginners

New to coding? This guide walks you through everything, from installing the tools to running your first AI agent.
You only do this **once**. After that, every notebook in the course works without any further installation.

**Time needed:** about 20-30 minutes, most of it waiting for downloads.

Already comfortable with Python and the terminal? Use the shorter [`LOCAL_SETUP.MD`](LOCAL_SETUP.MD) instead.

---

## What you will set up

| What | Why |
|---|---|
| **VS Code** | The free editor where you open and run the course notebooks. |
| **uv** | A small tool that installs Python and all the course packages for you, at the exact versions the course was tested with. |
| **The course folder** | All notebooks and files of the course. |
| **A `.env` file** | A private file that holds your API keys, so you never type them into a notebook. |

You do **not** need to install Python yourself. uv does it for you.

---

## Step 1 - Install VS Code

1. Download VS Code from https://code.visualstudio.com/ and install it with the default options.
2. Open VS Code. Click the **Extensions** icon in the left bar (four small squares), or press `Ctrl + Shift + X` (`Cmd + Shift + X` on a Mac).
3. Search for **Python** and click **Install** on the one published by *Microsoft*.
4. Search for **Jupyter** and click **Install** on the one published by *Microsoft*.

---

## Step 2 - Put the course folder in a simple location

1. Download the course files (from the Udemy resources or GitHub) and **extract** the ZIP file. Do not work from inside the ZIP.
2. Move the extracted folder to a short, simple location, for example:
   - Windows: `C:\courses\Agentic-AI-For-Beginners-Updated`
   - Mac: your *Documents* folder, for example `Documents/Agentic-AI-For-Beginners-Updated`

> **Windows users:** avoid long paths and OneDrive folders. Windows has a limit on path length, and some packages
> fail to install in deeply nested folders.

The course folder is the one that contains `pyproject.toml`, `README.md` and the `Part1` ... `Part4` folders.

---

## Step 3 - Open the course folder in VS Code

1. In VS Code: **File → Open Folder…** (on a Mac: **File → Open…**).
2. Select the **course folder** itself (not `Part1` or another subfolder) and click **Select Folder** / **Open**.
3. If VS Code asks *"Do you trust the authors of the files in this folder?"*, click **Yes, I trust the authors**.

You now see the course files in the **Explorer** panel on the left.

---

## Step 4 - Open the terminal inside VS Code

The **terminal** is a window where you type commands instead of clicking buttons. You only need it for a few commands in this guide.

In VS Code: **Terminal → New Terminal**. A panel opens at the bottom of the window.
It is already "inside" the course folder, so the commands below run in the right place.

To run a command: copy it, paste it into the terminal, and press **Enter**.

---

## Step 5 - Install uv

Paste the command for your computer into the VS Code terminal and press **Enter**.

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

When it finishes, **close VS Code completely and open it again** (so it notices that uv is installed).
VS Code reopens your course folder. Open a new terminal (**Terminal → New Terminal**) and check that uv works:

```bash
uv --version
```

You should see something like `uv 0.x.y`. If you see *"uv is not recognized"* or *"command not found"*, see [Common problems](#common-problems).

---

## Step 6 - Install everything for the course

In the VS Code terminal, run:

```bash
uv sync
```

This downloads Python 3.12 and every package used in Parts 1-4 into a folder called **`.venv`** inside the course folder.
The first time takes a few minutes. When the terminal shows the prompt again with no red error messages, it is done.

> You can safely run `uv sync` again at any time. It only installs what is missing.

---

## Step 7 - Create your `.env` file and add your API key

1. Create your own copy of the example settings file. In the VS Code terminal, run the command for your computer:

   **Windows:**
   ```powershell
   Copy-Item .env.example .env
   ```

   **Mac:**
   ```bash
   cp .env.example .env
   ```

2. Click the new **`.env`** file in the Explorer panel to open it.
3. Create your OpenAI API key (see [`Managing_Secrets.md`](Managing_Secrets.md), Part A - billing must be enabled).
4. In `.env`, replace `your-openai-api-key-here` with your key. Keep it on one line, with **no quotes and no spaces**:

   ```
   OPENAI_API_KEY=sk-...your key...
   ```

5. Save the file: `Ctrl + S` (`Cmd + S` on a Mac).

You only need the keys for the lessons you are running. Each Part's `readme.md` lists them.
Never share your `.env` file, and never paste a key into a notebook, a screenshot or a Q&A question.

---

## Step 8 - Run your first notebook

1. In the Explorer panel, open **`Part1`** and click **`Basic_Agent.ipynb`**.
2. Click **Select Kernel** in the top-right corner of the notebook → **Python Environments** → choose **`.venv`** (Python 3.12).
   The *kernel* is the Python environment that runs the notebook. You select `.venv` once per notebook, and VS Code remembers it.
3. Click into the first **code** cell and press `Shift + Enter` to run it. It should print:

   ```
   Ready: course .venv kernel | Python 3.12...
   ```

4. Run the next cell. It should print:

   ```
   All required API keys are loaded.
   ```

5. Keep pressing `Shift + Enter` to run the cells from top to bottom.

Your setup is done. Every other notebook in the course works the same way: open it, select the `.venv` kernel, and run the cells from top to bottom.

---

## Coming back later

Open VS Code, then **File → Open Recent** → your course folder. There is nothing to install again.

---

## Common problems

| What you see | What to do |
|---|---|
| `uv is not recognized` / `uv: command not found` | Close VS Code completely and open it again. On Windows, if it still fails, sign out of Windows and back in. |
| `uv sync` fails with *"The system cannot find the path specified"* (Windows) | The course folder path is too long. Move the folder to `C:\courses\` (Step 2), delete the `.venv` folder, and run `uv sync` again. |
| `.venv` is not offered when you select the kernel | Check that you opened the **course folder** in VS Code (Step 3) and that `uv sync` finished. Then press `Ctrl + Shift + P`, type **Python: Select Interpreter**, and choose the `.venv` one. Restart VS Code if it still does not appear. |
| The first cell prints *"Warning: … select the .venv kernel"* | The notebook is using a different Python. Select the `.venv` kernel (Step 8) and run the cell again. |
| `ModuleNotFoundError: No module named …` | Same cause: wrong kernel. Select `.venv`, then click **Restart** in the notebook toolbar and run the cells again from the top. |
| *"Missing required keys: OPENAI_API_KEY"* | Check that the file is named exactly `.env` (not `.env.txt`), that it is in the course folder, and that the key is on the `OPENAI_API_KEY=` line with no quotes. Save it, click **Restart** in the notebook toolbar, and run the cells again. |
| An OpenAI error about *quota*, *billing* or *401* | Your key is wrong or your OpenAI account has no billing set up. See `Managing_Secrets.md`, Part A. |
| *"Do you trust the authors"* keeps blocking cells | Click **Manage → Workspace Trust** and trust the course folder. |

Still stuck? Post your question in the course Q&A with the **error message** (never your API key) and the notebook name.
