

import requests

def generate_answer(query, context):
    prompt = f"""
    Answer the question based on the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",   # or whatever model you're using
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    # Safe extraction
    if "response" in data:
        return data["response"]

    elif "message" in data:
        return data["message"]["content"]

    else:
        return f"Unexpected response: {data}"