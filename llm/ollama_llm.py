

# import requests

# def generate_answer(query, context):
#     prompt = f"""
#     Answer the question based on the context below.

#     Context:
#     {context}

#     Question:
#     {query}
#     """

#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={...},
#             timeout=60
#     )
#     except requests.exceptions.ConnectionError:
#         return "⚠️ Ollama is not running. Please start it using 'ollama serve'"



#     data = response.json()

#     # Safe extraction
#     if "response" in data:
#         return data["response"]

#     elif "message" in data:
#         return data["message"]["content"]

#     else:
#         return f"Unexpected response: {data}"










import requests


# -------------------------------
# 🛠 Helpers
# -------------------------------
def safe_str(value):
    if value is None:
        return ""
    return str(value)


def truncate(text, limit=300):
    if not text:
        return ""
    return str(text)[:limit]


def safe_join(values):
    """
    Handles list, set, dict safely
    """
    if not values:
        return ""

    # 🔥 FIX: convert set → list
    if isinstance(values, set):
        values = list(values)

    cleaned = []
    for v in values:
        if isinstance(v, dict):
            cleaned.append(str(v.get("name") or v.get("body") or v))
        else:
            cleaned.append(str(v))

    return ", ".join(cleaned)


def format_comments(comments):
    """
    Handles comments safely (dict/string/set)
    """
    if not comments:
        return ""

    # 🔥 FIX: convert set → list
    if isinstance(comments, set):
        comments = list(comments)

    cleaned = []

    # limit number of comments
    for c in comments[:3]:
        if isinstance(c, dict):
            text = str(c.get("body", ""))
        else:
            text = str(c)

        cleaned.append(text[:200])  # truncate each comment

    return " ".join(cleaned)


def convert_sets(obj):
    """
    🔥 GLOBAL FIX: convert all sets to lists (recursive)
    """
    if isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    elif isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, list):
        return [convert_sets(i) for i in obj]
    else:
        return obj


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
Components: {safe_join(item.get('components'))}
Labels: {safe_join(item.get('labels'))}
Comments: {truncate(format_comments(item.get('comments')), 300)}
"""


# -------------------------------
# 🚀 MAIN FUNCTION
# -------------------------------
def generate_answer(query, context):

    # 🔥 STEP 1: Fix JSON issue globally
    context = convert_sets(context)

    # 🔥 STEP 2: sort by relevance (if score exists)
    context = sorted(context, key=lambda x: x.get("score", 0), reverse=True)

    # 🔥 STEP 3: limit tickets (prevents token overflow)
    context = context[:3]

    # 🔥 STEP 4: build clean context
    context_text = "\n\n".join([format_issue(item) for item in context])

    # 🔥 STEP 5: prompt
    prompt = f"""
You are a Jira assistant.
Answer ONLY from the context.
If not found, say: "I could not find the answer in the Jira data."

Context:
{context_text}

Question:
{query}

Answer:
"""

    # -------------------------------
    # 📡 API CALL (OLLAMA)
    # -------------------------------
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = response.json()

        if "response" in data:
            return data["response"]

        elif "message" in data:
            return data["message"].get("content", "")

        else:
            return f"Unexpected response: {data}"

    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama is not running. Start it using: `ollama serve`"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"