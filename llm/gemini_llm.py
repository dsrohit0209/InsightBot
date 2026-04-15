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











# from dotenv import load_dotenv
# import google.generativeai as genai
# import os

# # Load env
# load_dotenv(dotenv_path="../.env")

# # Configure API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Load model
# model = genai.GenerativeModel("gemini-2.5-flash")


# def generate_answer(query, context):

#     # -------------------------------
#     # 🛠 Helpers (robust conversion)
#     # -------------------------------
#     def safe_str(value):
#         if value is None:
#             return ""
#         return str(value)

#     def safe_join(values):
#         """
#         Handles list of strings OR list of dicts safely
#         """
#         if not values:
#             return ""

#         cleaned = []
#         for v in values:
#             if isinstance(v, dict):
#                 # try common fields
#                 cleaned.append(str(v.get("name") or v.get("body") or v))
#             else:
#                 cleaned.append(str(v))

#         return ", ".join(cleaned)

#     def format_comments(comments):
#         """
#         Specifically handle comments safely
#         """
#         if not comments:
#             return ""

#         cleaned = []
#         for c in comments:
#             if isinstance(c, dict):
#                 cleaned.append(str(c.get("body", "")))
#             else:
#                 cleaned.append(str(c))

#         return " ".join(cleaned)

#     # -------------------------------
#     # 🧠 Format each issue
#     # -------------------------------
#     def format_issue(item):
#         return f"""
# Issue ID: {safe_str(item.get('key'))}
# Project: {safe_str(item.get('project'))}
# Type: {safe_str(item.get('issuetype'))}
# Summary: {safe_str(item.get('summary'))}
# Description: {safe_str(item.get('description'))}
# Status: {safe_str(item.get('status'))}
# Priority: {safe_str(item.get('priority'))}
# Assignee: {safe_str(item.get('assignee'))}
# Reporter: {safe_str(item.get('reporter'))}
# Components: {safe_join(item.get('components'))}
# Labels: {safe_join(item.get('labels'))}
# Fix Versions: {safe_join(item.get('fixVersions'))}
# Due Date: {safe_str(item.get('duedate'))}
# Comments: {format_comments(item.get('comments'))}
# """

#     # -------------------------------
#     # 📦 Build context
#     # -------------------------------
#     context_text = "\n\n".join([format_issue(item) for item in context])

#     prompt = f"""
# You are a Jira assistant.
# Answer the question based on the Jira context.

# Context:
# {context_text}

# Question:
# {query}

# Answer:
# """

#     response = model.generate_content(prompt)

#     return response.text
