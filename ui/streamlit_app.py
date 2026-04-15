
# # ui/streamlit_app.py
# import streamlit as st
# import sys
# import os
# import uuid

# sys.path.append(os.getcwd())

# from rag.retriever import search

# # Import all LLMs
# from llm.groq_llm import generate_answer as groq_generate
# from llm.openai_llm import generate_answer as openai_generate
# from llm.gemini_llm import generate_answer as gemini_generate
# from llm.ollama_llm import generate_answer as ollama_generate

# st.set_page_config(page_title="Jira AI Chatbot", layout="wide")

# # -------------------------------
# # Session state
# # -------------------------------
# if "chats" not in st.session_state:
#     st.session_state.chats = {}

# if "current_chat_id" not in st.session_state:
#     st.session_state.current_chat_id = None

# if "rename_chat_id" not in st.session_state:
#     st.session_state.rename_chat_id = None

# if "selected_model" not in st.session_state:
#     st.session_state.selected_model = "Groq"

# # -------------------------------
# # Helper functions
# # -------------------------------
# def create_new_chat():
#     chat_id = str(uuid.uuid4())
#     st.session_state.chats[chat_id] = {
#         "name": "New Chat",
#         "messages": []
#     }
#     st.session_state.current_chat_id = chat_id


# def delete_chat(chat_id):
#     if chat_id in st.session_state.chats:
#         del st.session_state.chats[chat_id]
#         if st.session_state.current_chat_id == chat_id:
#             st.session_state.current_chat_id = None


# # -------------------------------
# # Model Selector Function
# # -------------------------------
# def get_llm_response(query, context):
#     model = st.session_state.selected_model

#     if model == "Groq":
#         return groq_generate(query=query, context=context)
#     elif model == "OpenAI":
#         return openai_generate(query=query, context=context)
#     elif model == "Gemini":
#         return gemini_generate(query=query, context=context)
#     elif model == "Ollama":
#         return ollama_generate(query=query, context=context)
#     else:
#         return "Invalid model selected"


# st.title("Jira AI Chatbot 🤖")
# # -------------------------------
# # Sidebar
# # -------------------------------
# with st.sidebar:
#     st.title("💬 Chats")

#     # ➕ New Chat
#     if st.button("➕ New Chat"):
#         create_new_chat()
#         st.rerun()

#     st.divider()

#     # 🤖 Model selector
#     st.subheader("🤖 Select Model")
#     st.selectbox(
#         "Choose LLM",
#         ["Groq", "OpenAI", "Gemini", "Ollama"],
#         key="selected_model"
#     )

#     st.divider()

#     # Chat list
#     for chat_id, chat_data in list(st.session_state.chats.items()):
#         cols = st.columns([3, 1, 1])

#         if cols[0].button(chat_data["name"], key=f"open_{chat_id}"):
#             st.session_state.current_chat_id = chat_id

#         if cols[1].button("✏️", key=f"rename_{chat_id}"):
#             st.session_state.rename_chat_id = chat_id

#         if cols[2].button("🗑", key=f"delete_{chat_id}"):
#             delete_chat(chat_id)
#             st.rerun()

#     # Rename UI
#     if st.session_state.rename_chat_id:
#         st.divider()
#         st.subheader("✏️ Rename Chat")

#         chat_id = st.session_state.rename_chat_id
#         new_name = st.text_input("New name:", key="rename_input")

#         if st.button("Save Name"):
#             if new_name.strip():
#                 st.session_state.chats[chat_id]["name"] = new_name
#                 st.session_state.rename_chat_id = None
#                 st.rerun()
#             else:
#                 st.warning("Enter a valid name")

# # -------------------------------
# # Main UI
# # -------------------------------

# st.write(f"Model: **{st.session_state.selected_model}**")

# if st.session_state.current_chat_id is None:
#     st.info("Click 'New Chat' to start chatting")
# else:
#     chat = st.session_state.chats[st.session_state.current_chat_id]

#     st.subheader(f"Chat: {chat['name']}")

#     # Show messages
#     for msg in chat["messages"]:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Input
#     query = st.chat_input("Ask something about Jira...")

#     if query:
#         # Auto-title
#         if chat["name"] == "New Chat":
#             chat["name"] = query[:30]

#         chat["messages"].append({"role": "user", "content": query})

#         with st.chat_message("user"):
#             st.markdown(query)

#         # Retrieve data
#         with st.spinner("Searching relevant issues..."):
#             results = search(query)

#         with st.expander("🔎 Retrieved Jira Data"):
#             st.write(results)

#         # Context
#         conversation_context = ""
#         for msg in chat["messages"][-6:]:
#             conversation_context += f"{msg['role']}: {msg['content']}\n"

#         final_query = f"""
# You are a helpful Jira assistant.

# Conversation so far:
# {conversation_context}

# User question:
# {query}
# """

#         # 🔥 Use selected model
#         with st.spinner(f"{st.session_state.selected_model} is thinking..."):
#             answer = get_llm_response(query=final_query, context=results)

#         chat["messages"].append({"role": "assistant", "content": answer})

#         with st.chat_message("assistant"):
#             st.markdown(answer)





# ui/streamlit_app.py
import streamlit as st
import sys
import os
import uuid

sys.path.append(os.getcwd())

from rag.retriever import search

# LLM imports
from llm.groq_llm import generate_answer as groq_generate
from llm.openai_llm import generate_answer as openai_generate
from llm.gemini_llm import generate_answer as gemini_generate
from llm.ollama_llm import generate_answer as ollama_generate

st.set_page_config(page_title="InsightBot", layout="wide")

# -------------------------------
# Session state
# -------------------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "rename_chat_id" not in st.session_state:
    st.session_state.rename_chat_id = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Groq"

# -------------------------------
# Helper functions
# -------------------------------
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "name": "New Chat",
        "messages": []
    }
    st.session_state.current_chat_id = chat_id


def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None


def get_llm_response(query, context):
    model = st.session_state.selected_model

    if model == "Groq":
        return groq_generate(query=query, context=context)
    elif model == "OpenAI":
        return openai_generate(query=query, context=context)
    elif model == "Gemini":
        return gemini_generate(query=query, context=context)
    elif model == "Ollama":
        return ollama_generate(query=query, context=context)
    else:
        return "Invalid model selected"


# -------------------------------
# 🔥 FORMAT JIRA RESULTS (NEW)
# -------------------------------
def format_jira_results(results):
    formatted = []

    for item in results:
        try:
            key = item.get("key", "N/A")
            summary = item.get("summary", "")
            status = item.get("status", "")
            assignee = item.get("assignee", "Unassigned")

            formatted.append(
                f"### 🔹 {key}\n"
                f"**Summary:** {summary}\n\n"
                f"**Status:** {status} | **Assignee:** {assignee}\n"
            )
        except:
            continue

    return formatted


# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.title("💬 Chats")

    if st.button("➕ New Chat"):
        create_new_chat()
        st.rerun()

    st.divider()

    # Model selector
    st.subheader("🤖 Select Model")
    st.selectbox(
        "Choose LLM",
        ["Groq", "OpenAI", "Gemini", "Ollama"],
        key="selected_model"
    )

    st.divider()

    # Chat list
    for chat_id, chat_data in list(st.session_state.chats.items()):
        cols = st.columns([3, 1, 1])

        if cols[0].button(chat_data["name"], key=f"open_{chat_id}"):
            st.session_state.current_chat_id = chat_id

        if cols[1].button("✏️", key=f"rename_{chat_id}"):
            st.session_state.rename_chat_id = chat_id

        if cols[2].button("🗑", key=f"delete_{chat_id}"):
            delete_chat(chat_id)
            st.rerun()

    # Rename UI
    if st.session_state.rename_chat_id:
        st.divider()
        st.subheader("✏️ Rename Chat")

        chat_id = st.session_state.rename_chat_id
        new_name = st.text_input("New name:", key="rename_input")

        if st.button("Save Name"):
            if new_name.strip():
                st.session_state.chats[chat_id]["name"] = new_name
                st.session_state.rename_chat_id = None
                st.rerun()
            else:
                st.warning("Enter a valid name")

# -------------------------------
# Main UI
# -------------------------------
st.title("InsightBot 🤖")
st.write(f"Model: **{st.session_state.selected_model}**")

if st.session_state.current_chat_id is None:
    st.info("Click 'New Chat' to start chatting")
else:
    chat = st.session_state.chats[st.session_state.current_chat_id]

    st.subheader(f"Chat: {chat['name']}")

    # Show messages
    for msg in chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    query = st.chat_input("Ask something about Jira...")

    if query:
        # Auto-title
        if chat["name"] == "New Chat":
            chat["name"] = query[:30]

        chat["messages"].append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        # -------------------------------
        # Retrieve data
        # -------------------------------
        with st.spinner("Searching relevant issues..."):
            results = search(query)

        # -------------------------------
        # ✅ CLEAN UI (NO JSON)
        # -------------------------------
        with st.expander("🔎 Retrieved Jira Context"):
            formatted_results = format_jira_results(results)

            if formatted_results:
                for res in formatted_results:
                    st.markdown(res)
            else:
                st.info("No relevant Jira issues found.")

        # -------------------------------
        # Context
        # -------------------------------
        conversation_context = ""
        for msg in chat["messages"][-6:]:
            conversation_context += f"{msg['role']}: {msg['content']}\n"

        final_query = f"""
 You are a helpful Jira assistant.

Conversation so far:
{conversation_context}

User question:
{query}
"""

        # -------------------------------
        # LLM response
        # -------------------------------
        with st.spinner(f"{st.session_state.selected_model} is thinking..."):
            answer = get_llm_response(query=final_query, context=results)

        chat["messages"].append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)





# Answer any questions asked.
# You are a Jira assistant.








# # ui/streamlit_app.py
# import streamlit as st
# import sys
# import os
# import uuid

# sys.path.append(os.getcwd())

# from rag.retriever import search

# # LLM imports
# from llm.groq_llm import generate_answer as groq_generate
# from llm.openai_llm import generate_answer as openai_generate
# from llm.gemini_llm import generate_answer as gemini_generate
# from llm.ollama_llm import generate_answer as ollama_generate

# st.set_page_config(page_title="Jira AI Chatbot", layout="wide")

# # -------------------------------
# # Session state
# # -------------------------------
# if "chats" not in st.session_state:
#     st.session_state.chats = {}

# if "current_chat_id" not in st.session_state:
#     st.session_state.current_chat_id = None

# if "rename_chat_id" not in st.session_state:
#     st.session_state.rename_chat_id = None

# if "selected_model" not in st.session_state:
#     st.session_state.selected_model = "Groq"

# # -------------------------------
# # Helper functions
# # -------------------------------
# def create_new_chat():
#     chat_id = str(uuid.uuid4())
#     st.session_state.chats[chat_id] = {
#         "name": "New Chat",
#         "messages": []
#     }
#     st.session_state.current_chat_id = chat_id


# def delete_chat(chat_id):
#     if chat_id in st.session_state.chats:
#         del st.session_state.chats[chat_id]
#         if st.session_state.current_chat_id == chat_id:
#             st.session_state.current_chat_id = None


# def get_llm_response(query, context):
#     model = st.session_state.selected_model

#     if model == "Groq":
#         return groq_generate(query=query, context=context)
#     elif model == "OpenAI":
#         return openai_generate(query=query, context=context)
#     elif model == "Gemini":
#         return gemini_generate(query=query, context=context)
#     elif model == "Ollama":
#         return ollama_generate(query=query, context=context)
#     else:
#         return "Invalid model selected"


# # -------------------------------
# # FORMAT JIRA RESULTS
# # -------------------------------
# def format_jira_results(results):
#     if not results:
#         return None
#     item = results[0]  # Only top 1 result
#     try:
#         key = item.get("key", "N/A")
#         summary = item.get("summary", "")
#         status = item.get("status", "")
#         assignee = item.get("assignee", "Unassigned")

#         formatted = (
#             f"### 🔹 {key}\n"
#             f"**Summary:** {summary}\n\n"
#             f"**Status:** {status} | **Assignee:** {assignee}\n"
#         )
#         return formatted
#     except:
#         return None


# # -------------------------------
# # Sidebar
# # -------------------------------
# with st.sidebar:
#     st.title("💬 Chats")

#     if st.button("➕ New Chat"):
#         create_new_chat()
#         st.rerun()

#     st.divider()

#     # Model selector
#     st.subheader("🤖 Select Model")
#     st.selectbox(
#         "Choose LLM",
#         ["Groq", "OpenAI", "Gemini", "Ollama"],
#         key="selected_model"
#     )

#     st.divider()

#     # Chat list
#     for chat_id, chat_data in list(st.session_state.chats.items()):
#         cols = st.columns([3, 1, 1])

#         if cols[0].button(chat_data["name"], key=f"open_{chat_id}"):
#             st.session_state.current_chat_id = chat_id

#         if cols[1].button("✏️", key=f"rename_{chat_id}"):
#             st.session_state.rename_chat_id = chat_id

#         if cols[2].button("🗑", key=f"delete_{chat_id}"):
#             delete_chat(chat_id)
#             st.rerun()

#     # Rename UI
#     if st.session_state.rename_chat_id:
#         st.divider()
#         st.subheader("✏️ Rename Chat")

#         chat_id = st.session_state.rename_chat_id
#         new_name = st.text_input("New name:", key="rename_input")

#         if st.button("Save Name"):
#             if new_name.strip():
#                 st.session_state.chats[chat_id]["name"] = new_name
#                 st.session_state.rename_chat_id = None
#                 st.rerun()
#             else:
#                 st.warning("Enter a valid name")

# # -------------------------------
# # Main UI
# # -------------------------------
# st.title("Jira AI Chatbot 🤖")
# st.write(f"Model: **{st.session_state.selected_model}**")

# if st.session_state.current_chat_id is None:
#     st.info("Click 'New Chat' to start chatting")
# else:
#     chat = st.session_state.chats[st.session_state.current_chat_id]

#     st.subheader(f"Chat: {chat['name']}")

#     # Show messages
#     for msg in chat["messages"]:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Input
#     query = st.chat_input("Ask something about Jira...")

#     if query:
#         # Auto-title
#         if chat["name"] == "New Chat":
#             chat["name"] = query[:30]

#         chat["messages"].append({"role": "user", "content": query})

#         with st.chat_message("user"):
#             st.markdown(query)

#         # -------------------------------
#         # Retrieve Jira data
#         # -------------------------------
#         with st.spinner("Searching relevant issues..."):
#             results = search(query)

#         # -------------------------------
#         # Display only most relevant ticket
#         # -------------------------------
#         with st.expander("🔎 Most Relevant Jira Ticket"):
#             formatted_result = format_jira_results(results)

#             if formatted_result:
#                 st.markdown(formatted_result)
#             else:
#                 st.info("No relevant Jira issues found.")

#         # -------------------------------
#         # Prepare conversation context
#         # -------------------------------
#         conversation_context = ""
#         for msg in chat["messages"][-6:]:
#             conversation_context += f"{msg['role']}: {msg['content']}\n"

#         final_query = f"""
# You are a helpful Jira assistant.

# Conversation so far:
# {conversation_context}

# User question:
# {query}
# """

#         # -------------------------------
#         # Generate LLM response
#         # -------------------------------
#         with st.spinner(f"{st.session_state.selected_model} is thinking..."):
#             answer = get_llm_response(query=final_query, context=results)

#         chat["messages"].append({"role": "assistant", "content": answer})

#         with st.chat_message("assistant"):
#             st.markdown(answer)