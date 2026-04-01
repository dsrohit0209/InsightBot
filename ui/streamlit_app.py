# ui/streamlit_app.py
import streamlit as st
import sys
import os

# Add project root to sys.path for proper imports
sys.path.append(os.getcwd())

from rag.retriever import search       # your FAISS retriever function
# from llm.ollama_llm import generate_answer  # your LLM function
# from llm.groq_llm import  generate_answer # Groq LLM function
# from llm.openai_llm  import  generate_answer # Openai LLM function
from llm.gemini_llm  import  generate_answer # Gemini LLM function

# Streamlit UI
st.title("Jira AI Chatbot 🤖")

st.write("Ask me anything about your Jira issues!")

# Input box
query = st.text_input("Your question:")

if query:
    with st.spinner("Searching relevant issues..."):
        results = search(query)  # returns top chunks from FAISS

    st.write("**Relevant Jira chunks:**")
    for i, r in enumerate(results, 1):
        st.write(f"**Chunk {i}:** {r}")

    with st.spinner("Generating answer..."):
        answer = generate_answer(query, results)

    st.write("**AI Answer:**")
    st.info(answer)