## Securely Managing API Keys

It is crucial **never to save your secret API key directly in your code files**. We store keys in a file called **`.env`** (for "environment") in the course folder. The notebooks read the keys from there, so you never type a key into a notebook.

### Part A: Generate Your OpenAI API Key

1.  **Create an Account:**
    * Go to the **[OpenAI Platform website](https://platform.openai.com/)** and sign up or log in. You may need to verify your phone number.
2.  **Navigate to API Keys:**
    * Open the **[API Keys page](https://platform.openai.com/api-keys)**.
3.  **Create a New Key:**
    * Click **"+ Create new secret key"** and give it a descriptive name (e.g., `course-project-key`).
4.  **Copy and Save Immediately:**
    * Your key is displayed **only once**. Copy it straight into your `.env` file (Part B). If you lose it, create a new one.
5.  **Add Billing (Required for Usage):**
    * The key will not work until you have a payment method on file. In the **Billing** section, add a payment method and **set a usage limit** (recommended for safety).

Other keys used in the course (Groq, Tavily, Langflow) are created the same way - each Part's `readme.md` links to the right page.

### Part B: The `.env` File

1.  **Create the `.env` File:**
    * In the **course folder** (the folder that contains `.env.example`), copy `.env.example` and name the copy **`.env`** - no extension like `.txt`.
      * macOS / Linux: `cp .env.example .env`
      * Windows PowerShell: `Copy-Item .env.example .env`

2.  **Add Your API Key:**
    * Open `.env` in a text editor and replace the placeholder after `=` with your key, for example:

    ```
    OPENAI_API_KEY=paste-your-key-here
    ```
    * **Do not use quotes** around the value. Save the file.

3.  **How the Notebooks Load It:**
    * Every notebook calls `load_dotenv()`, which looks for `.env` in the notebook's folder and then in each parent folder. Because your `.env` is in the course folder, all Parts find it automatically - **you never need to write a file path**.

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()  # finds the .env file in this folder or a parent folder

    if os.getenv("OPENAI_API_KEY"):
        print("Success! Your OpenAI API key was loaded.")
    else:
        print("Failure! The key was NOT loaded. Check that the file is named .env and is in the course folder.")
    ```

4.  **Keep It Private:**
    * `.env` is listed in `.gitignore`, so Git will not commit it. Never paste your key into a notebook, screenshot, forum post or Q&A question.

### If a Key Leaks

Delete (revoke) the key immediately on the provider's website and create a new one. Revoking is the only way to make a leaked key safe.
