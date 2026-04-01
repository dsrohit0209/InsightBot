from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from .env
load_dotenv(dotenv_path="../.env")

api = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api)


# print("Loaded key:", os.getenv("OPENAI_API_KEY"))  



def generate_answer(query, context):

    def format_issue(item):
        return f"""
Issue ID: {item.get('key', '')}
Project: {item.get('project', '')}
Type: {item.get('issuetype', '')}
Summary: {item.get('summary', '')}
Description: {item.get('description', '')}
Status: {item.get('status', '')}
Priority: {item.get('priority', '')}
Assignee: {item.get('assignee', '')}
Reporter: {item.get('reporter', '')}
Components: {", ".join(item.get('components', []))}
Labels: {", ".join(item.get('labels', []))}
Fix Versions: {", ".join(item.get('fixVersions', []))}
Due Date: {item.get('duedate', '')}
Comments: {" ".join(item.get('comments', []))}
"""
    
    # 🔥 Build rich context
    context_text = "\n\n".join([format_issue(item) for item in context])

    prompt = f"""
Answer the question based on the Jira context.

Context:
{context_text}

Question:
{query}

Answer:
"""

    # Create a chat completion using OpenAI
    response = client.chat.completions.create(
        model="gpt-5.4",  # or "gpt-5-mini" etc.
        messages=[
            {"role": "system", "content": "You are a Jira assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    # Extract the assistant’s reply
    return response.choices[0].message.content