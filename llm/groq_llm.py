from dotenv import load_dotenv
from groq import Groq
import os 


# load_dotenv()
load_dotenv(dotenv_path="../.env")  # go up one folder

client = Groq(
    api_key= os.getenv("GROQ_API_KEY")
)
# print("Loaded key:", os.getenv("GROQ_API_KEY")) 

# def generate_answer(query, context):

#     # context_text = "\n".join([item["text"] for item in context])
#     context_text = "\n".join([
#     f"{item['id']}: {item['summary']} - {item['description']}"
#     for item in context ])


#     prompt = f"""
# Answer the question based on the Jira context.

# Context:
# {context_text}

# Question:
# {query}

# Answer:
# """

#     response = client.chat.completions.create(
#         # model="qwen/qwen3-32b",
#         model = "openai/gpt-oss-120b",
#         messages=[
#             {"role": "system", "content": "You are a Jira assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.3
#     )

#     return response.choices[0].message.content


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
You are a Jira assistant.

Answer the question based on the Jira context.

Context:
{context_text}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a Jira assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content



# Answer ONLY from the given Jira context.
# If the answer is not present, say:
# "I could not find the answer in the Jira data."