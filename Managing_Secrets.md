## Keeping Your API Keys Safe

Don't put API keys directly in your code files. Anyone who sees the code can use your key, and the charges go to your account. In this course, keys go in a file called **`.env`** (short for "environment") in the course folder, and the notebooks read them from there.

### Part A: Create your OpenAI API key

1. Go to the [OpenAI Platform website](https://platform.openai.com/) and sign up or log in. You may need to verify your phone number.
2. Open the [API Keys page](https://platform.openai.com/api-keys).
3. Click **+ Create new secret key** and give it a name you'll recognize, such as `course-project-key`.
4. Copy the key straight into your `.env` file (see Part B). It's shown **only once**. If you lose it, create a new one.
5. In the **Billing** section, add a payment method. The key won't work without one. It's also worth setting a usage limit.

You create the other keys used in the course (Groq, Tavily, Langflow) in a similar way. Each Part's `readme.md` tells you where.

### Part B: Set up the `.env` file

1. In the **course folder** (the one that contains `.env.example`), copy `.env.example` and name the copy **`.env`**. Make sure it doesn't end in an extension like `.txt`.
   - macOS / Linux: `cp .env.example .env`
   - Windows PowerShell: `Copy-Item .env.example .env`

2. Open `.env` in a text editor and replace the placeholder after `=` with your key. Don't put quotes around it. Then save the file.

   ```
   OPENAI_API_KEY=paste-your-key-here
   ```

### How the notebooks load your key

Every notebook calls `load_dotenv()`, which looks for `.env` in the notebook's folder and then in each parent folder. Your `.env` is in the course folder, so all the Parts find it automatically and you don't need to write a file path.

```python
import os
from dotenv import load_dotenv

load_dotenv()  # finds the .env file in this folder or a parent folder

if os.getenv("OPENAI_API_KEY"):
    print("OpenAI API key loaded.")
else:
    print("Key not found. Check that the file is named .env and is in the course folder.")
```

### Keep it private

`.env` is listed in `.gitignore`, so Git won't commit it. Never paste your key into a notebook, screenshot, forum post or Q&A question.

### If a key leaks

Delete the key on the provider's website right away and create a new one. A leaked key keeps working until you delete it.
