# from dotenv import load_dotenv
# from groq import Groq
# import os 


# # load_dotenv()
# load_dotenv(dotenv_path="../.env")  # go up one folder

# client = Groq(
#     api_key= os.getenv("GROQ_API_KEY")
# )
# # print("Loaded key:", os.getenv("GROQ_API_KEY")) 

# # def generate_answer(query, context):

# #     # context_text = "\n".join([item["text"] for item in context])
# #     context_text = "\n".join([
# #     f"{item['id']}: {item['summary']} - {item['description']}"
# #     for item in context ])


# #     prompt = f"""
# # Answer the question based on the Jira context.

# # Context:
# # {context_text}

# # Question:
# # {query}

# # Answer:
# # """

# #     response = client.chat.completions.create(
# #         # model="qwen/qwen3-32b",
# #         model = "openai/gpt-oss-120b",
# #         messages=[
# #             {"role": "system", "content": "You are a Jira assistant."},
# #             {"role": "user", "content": prompt}
# #         ],
# #         temperature=0.3
# #     )

# #     return response.choices[0].message.content


# def generate_answer(query, context):

#     def format_issue(item):
#         return f"""
# Issue ID: {item.get('key', '')}
# Project: {item.get('project', '')}
# Type: {item.get('issuetype', '')}
# Summary: {item.get('summary', '')}
# Description: {item.get('description', '')}
# Status: {item.get('status', '')}
# Priority: {item.get('priority', '')}
# Assignee: {item.get('assignee', '')}
# Reporter: {item.get('reporter', '')}
# Components: {", ".join(item.get('components', []))}
# Labels: {", ".join(item.get('labels', []))}
# Fix Versions: {", ".join(item.get('fixVersions', []))}
# Due Date: {item.get('duedate', '')}
# Comments: {" ".join(item.get('comments', []))}
# """
    
#     # 🔥 Build rich context
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

#     response = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[
#             {"role": "system", "content": "You are a Jira assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content



# # Answer ONLY from the given Jira context.
# # If the answer is not present, say:
# # "I could not find the answer in the Jira data."







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
#                 cleaned.append(str(v.get("name") or v.get("body") or v))
#             else:
#                 cleaned.append(str(v))

#         return ", ".join(cleaned)

#     def format_comments(comments):
#         """
#         Handle comments safely (dict or string)
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

#     response = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[
#             {"role": "system", "content": "You are a Jira assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content









from dotenv import load_dotenv
from groq import Groq
import os

# -------------------------------
# 🔐 Load environment
# -------------------------------
load_dotenv(dotenv_path="../.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -------------------------------
# 🛠 Helpers
# -------------------------------
def safe_str(value):
    if value is None:
        return ""
    return str(value)


def truncate(text, limit=1000):
    """
    Prevent token explosion
    """
    if not text:
        return ""
    return str(text)[:limit]


def safe_join(values):
    """
    Handles list of strings OR list of dicts
    """
    if not values:
        return ""

    cleaned = []
    for v in values:
        if isinstance(v, dict):
            cleaned.append(str(v.get("name") or v.get("body") or v))
        else:
            cleaned.append(str(v))

    return ", ".join(cleaned)


def format_comments(comments):
    """
    🔥 MOST IMPORTANT: control comment size
    """
    if not comments:
        return ""

    cleaned = []

    # ✅ limit number of comments
    for c in comments[:3]:
        if isinstance(c, dict):
            text = str(c.get("body", ""))
        else:
            text = str(c)

        # ✅ truncate each comment
        cleaned.append(text[:200])

    return " ".join(cleaned)


# -------------------------------
# 🧠 Format Jira issue
# -------------------------------
def format_issue(item):
    return f"""
Issue: {safe_str(item.get('key'))}
Summary: {truncate(item.get('summary'), 200)}
Description: {truncate(item.get('description'), 300)}
Status: {safe_str(item.get('status'))}
Priority: {safe_str(item.get('priority'))}
Assignee: {safe_str(item.get('assignee'))}
Comments: {truncate(format_comments(item.get('comments')), 300)}
"""


# -------------------------------
# 🚀 Main function
# -------------------------------
def generate_answer(query, context):

    # 🔥 STEP 1: sort by relevance (if FAISS score exists)
    context = sorted(context, key=lambda x: x.get("score", 0), reverse=True)

    # 🔥 STEP 2: limit number of tickets (CRITICAL FIX)
    context = context[:len(context)]

    # 🔥 STEP 3: build context safely
    context_text = "\n\n".join([format_issue(item) for item in context])

    # 🔥 STEP 4: short prompt (reduce tokens)
    prompt = f"""
You are a Jira assistant.

Context:
{context_text}

Question:
{query}

Answer:
"""

    # -------------------------------
    # 📡 API Call
    # -------------------------------
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a Jira assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2   # 🔥 reduce hallucination
    )

    return response.choices[0].message.content