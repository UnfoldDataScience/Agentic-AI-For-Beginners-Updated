# Part 4 - AI Agents on AWS Bedrock

Call a Bedrock foundation model from Python, build a Bedrock Agent with Lambda action groups, and chat with it from a Streamlit app.

> **Costs:** Bedrock, Lambda and agent calls are billed to **your** AWS account. Delete resources you no longer need.

---

# Files

| File | Purpose |
|---|---|
| `Intro_to_AwsBedrock.ipynb` | Call a Bedrock foundation model with `boto3` |
| `MyAgentDetails.txt` | Instructions to paste into your Bedrock Agent |
| `MapCourseRecommendationFunction.py` | Lambda function for the first action group (recommends a course) |
| `ProvideCourseReasoningPythonFunction.py` | Lambda function for the second action group (explains the recommendation) |
| `AssumeRolepolicy.json.txt` | Trust policy for the IAM role used to invoke the agent (replace the placeholders, then paste the whole file as the role's custom trust policy) |
| `CallingAgentInlinePolicy.json.txt` | Permissions policy for that role (replace the placeholders; `YOUR_REGION` must be the region of your agent, the same as `AWS_REGION`) |
| `Running_first_AWS_BedrockAgent.ipynb` | Invoke your agent from Python by assuming that role |
| `Basic_SL.py` | A first Streamlit app |
| `Call_AWS_Agent_through_UI.py` | A Streamlit chat UI for your agent |

---

# Prerequisites

1. An AWS account.
2. The AWS CLI installed: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
3. Sign in with **your own** IAM user: `aws configure`. Give the user only what it needs (for example the `AmazonBedrockFullAccess` managed policy) rather than administrator access.
4. In the Bedrock console, enable access to the model you want to use, in your region.

Your AWS credentials stay in the AWS CLI configuration. They are never written in the notebooks or in `.env`.

---

# Settings (`.env` in the course folder)

| Setting | Used by | Value |
|---|---|---|
| `AWS_REGION` | All | Your region, e.g. `us-east-1` |
| `BEDROCK_MODEL_ID` | `Intro_to_AwsBedrock.ipynb` | Optional, default `amazon.titan-text-express-v1` |
| `BEDROCK_AGENT_ID` | Agent notebook, Streamlit UI | Bedrock console → Agents → your agent |
| `BEDROCK_AGENT_ALIAS_ID` | Agent notebook, Streamlit UI | Your agent → Aliases |
| `BEDROCK_INVOKE_ROLE_ARN` | Agent notebook | IAM → Roles → the role created with the two policy files |

---

# Run

1. Set up the course environment once (see `LOCAL_SETUP.MD` in the course folder, or `BEGINNER_SETUP.md` if you are new to coding): `uv sync`
2. Copy `.env.example` to `.env` in the course folder and fill in the Part 4 settings.
3. Notebooks: open them and select the **`.venv`** kernel (Python 3.12).
4. Streamlit apps, from the course folder:

```bash
uv run streamlit run Part4/Basic_SL.py
uv run streamlit run Part4/Call_AWS_Agent_through_UI.py
```

---

# Differences from the Recorded Lesson

* The instructor's role ARN, agent ID and alias ID were removed. Your own values come from `.env`.
* `Intro_to_AwsBedrock.ipynb` uses Bedrock's **Converse API**, which works with any Bedrock text model. The default is still Titan Text Express.
* The Lambda functions accept non-numeric "years of experience" without crashing.
* The Streamlit chat UI no longer calls the agent when you click *Send* with an empty message.

---

# Tested Environment

Last updated: November 2026 - Python 3.12, boto3, Streamlit. Live AWS calls must be tested in your own account.
