# 🚀 Agentic AI for Beginner – Code & Resources

Welcome! 👋

This repository contains all code samples, Jupyter notebooks, Python scripts, and reference materials for the Udemy course **“Agentic AI for Beginner”** by *Unfold Data Science*.  
It is designed to help beginners learn Agentic AI concepts in a practical, hands-on way.

---

## 📚 What You Will Find in This Repository

- 🧠 **Code examples** used in the course  
- 📓 **Jupyter notebooks** organized by module  
- 🗂️ **Supporting files** (JSON, sample prompts, reference docs)  
- 🤖 **Agent workflows** and Langflow examples  
- 🔑 Guides on using environment variables (`.env`) and API keys safely  
- 🛠️ Setup instructions for Python, Jupyter, and LLM integrations  

---

## ⚡ Quick Start

Everything runs on your own computer, in **one environment for the whole course**:

```bash
uv sync                      # installs Python 3.12 and every package into .venv
cp .env.example .env         # Windows PowerShell: Copy-Item .env.example .env  - then add your keys
```

Open any notebook, select the **`.venv`** kernel and run the cells from top to bottom.

- **New to coding?** Start with [`BEGINNER_SETUP.md`](BEGINNER_SETUP.md). It explains every step, from installing VS Code to running your first cell.
- **Comfortable with Python?** See [`LOCAL_SETUP.MD`](LOCAL_SETUP.MD).
- **Keeping your API keys safe:** [`Managing_Secrets.md`](Managing_Secrets.md).

---

## 🗺️ Course Map

| Part | Lesson notebooks and files | Framework | Keys |
|---|---|---|---|
| [Part 1](Part1/readme.md) | `Basic_Agent.ipynb` | LangChain | OpenAI (Tavily optional) |
| [Part 2](Part2/readme.md) | `First_Multi_Agent.ipynb`, `CustomerServiceMAS.ipynb` | CrewAI | OpenAI |
| [Part 3](Part3/readme.md) | `Investment_Analysis_Agentic_System.ipynb`, `MAS_Using_MSAutogen.ipynb`, `Langflow/TestMyAgent.py` | Agno, AutoGen, Langflow | OpenAI, Groq, Langflow |
| [Part 4](Part4/readme.md) | `Intro_to_AwsBedrock.ipynb`, `Running_first_AWS_BedrockAgent.ipynb`, Lambda and Streamlit files | AWS Bedrock | Your AWS account |

AI libraries change quickly. Each notebook starts with a short *Compatibility update* note wherever the code differs from the recorded video.

The `maintenance/` folder is for course maintainers. Students don't need it and can ignore it.

---

## 🤝 Stay Connected

If you enjoyed the course or used this repository, feel free to reach out, follow, or tag me — I’d love to know you learned from our work!

**📧 Email:** query.unfolddatascience@gmail.com  
**🔗 LinkedIn:** https://www.linkedin.com/in/aman-kumar-b4881440/  
**▶️ YouTube:** https://www.youtube.com/@UnfoldDataScience/videos  
**📸 Instagram:** unfold_data_science  
**🐦 Twitter (X):** @unfoldds

---

Happy learning!  
Let’s build powerful agentic systems together. ⚡
