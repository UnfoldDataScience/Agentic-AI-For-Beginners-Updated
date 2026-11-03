# Call your own Langflow flow through its API.
# Settings come from the course .env file (see .env.example) - nothing is hard-coded here:
#   LANGFLOW_APPLICATION_TOKEN, LANGFLOW_ID, LANGFLOW_FLOW_ID and optionally LANGFLOW_BASE_URL.
# Find these values in Langflow: open your flow -> "API" (or "Share -> API access").
# Run from the course folder:  uv run python Part3/Langflow/TestMyAgent.py "What is 2+2?"

import argparse
import json
import os
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
from dotenv import load_dotenv
try:
    from langflow.load import upload_file
except ImportError:
    upload_file = None  # optional: only needed for --upload_file

load_dotenv()

BASE_API_URL = os.getenv("LANGFLOW_BASE_URL") or "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = os.getenv("LANGFLOW_ID", "")
FLOW_ID = os.getenv("LANGFLOW_FLOW_ID", "")
APPLICATION_TOKEN = os.getenv("LANGFLOW_APPLICATION_TOKEN", "")
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary, using the component IDs shown in
# your flow's API panel, e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers, timeout=120)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--application_token", type=str, default=APPLICATION_TOKEN, help="Application Token for authentication")
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    if not LANGFLOW_ID or not args.endpoint or not args.application_token:
        parser.error("Set LANGFLOW_ID, LANGFLOW_FLOW_ID and LANGFLOW_APPLICATION_TOKEN in your .env file.")
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=args.endpoint, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        application_token=args.application_token
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
