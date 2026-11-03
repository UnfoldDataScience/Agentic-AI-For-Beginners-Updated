# Streamlit chat UI for your AWS Bedrock Agent.
# Run from the course folder:  uv run streamlit run Part4/Call_AWS_Agent_through_UI.py
# Settings come from the course .env file (see .env.example): AWS_REGION,
# BEDROCK_AGENT_ID and BEDROCK_AGENT_ALIAS_ID. AWS credentials come from `aws configure`.
import os
import uuid

import boto3
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Your Agent ID and Alias ID (Bedrock console -> Agents -> your agent)
agent_id = os.getenv("BEDROCK_AGENT_ID")
agent_alias_id = os.getenv("BEDROCK_AGENT_ALIAS_ID")
region = os.getenv("AWS_REGION") or "us-east-1"

# Streamlit UI
st.title("Bedrock Agent Chat")

if not agent_id or not agent_alias_id:
    st.error("Set BEDROCK_AGENT_ID and BEDROCK_AGENT_ALIAS_ID in your .env file, then restart the app.")
    st.stop()

# Initialize Bedrock Agent Runtime client
bedrock_agent_runtime = boto3.client(service_name='bedrock-agent-runtime', region_name=region)

# Initialize session ID in session state
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat messages from history
for message in st.session_state['chat_history']:
    if message['role'] == 'user':
        st.text(f"You: {message['content']}")
    else:
        st.text(f"Agent: {message['content']}")

# Input field for user message
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    # Add user message to chat history
    st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
    try:
        # Invoke the agent
        response = bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            inputText=user_input,
            sessionId=st.session_state['session_id']
        )

        # Extract agent's response
        event_stream = response["completion"]
        full_response = ""

        for event in event_stream:
            if 'chunk' in event:
                full_response += event['chunk']['bytes'].decode('utf-8')
            elif 'trace' in event:
                trace_data = event['trace']
                if trace_data.get('traceType') == 'AGENT_ORCHESTRATION':
                    for step in trace_data.get('orchestrationSteps', []):
                        agent_action = step.get('agentAction', {})
                        if agent_action.get('agentActionType') == 'RETURN_FINAL_RESPONSE':
                            action_output = agent_action.get('agentActionOutput', {})
                            if 'finalResponse' in action_output:
                                full_response += action_output['finalResponse']
                            elif 'outputText' in action_output.get('invokeModelResponse', {}):
                                full_response += action_output['invokeModelResponse']['outputText']
        # Add agent's response to chat history
        st.session_state['chat_history'].append({'role': 'agent', 'content': full_response})
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state['chat_history'].append({'role': 'agent', 'content': f"Error: {e}"})
    # Rerun to update the chat display
    st.rerun()
