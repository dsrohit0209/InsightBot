from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load env
load_dotenv(dotenv_path="../.env")

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


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

    # Build context
    context_text = "\n\n".join([format_issue(item) for item in context])

    prompt = f"""
You are a Jira assistant.
Answer the question based on the Jira context.


Context:
{context_text}

Question:
{query}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text