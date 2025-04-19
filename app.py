import streamlit as st
import openai
import os
from dotenv import load_dotenv

import dummy


st.title("MOH Bot")

st.write("### Welcome to the AI Chatbot demo!")
st.write("Please ask the assistant any question related to خدمات الهيئة الطبية العامة بجدة")

# Initialize an OpenAI thread id for the chat
if "client" not in st.session_state:
    load_dotenv()
    st.session_state.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    st.session_state.assistant_id = os.environ.get("ASSISTANT_ID")

if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages with roles
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"{message['role'].title()}: {message['content']}")


# React to user input
if query := st.chat_input("Type your question here..."):

    # Display the user message
    with st.chat_message("user"):
        st.markdown(f"User: {query}")

    # Add the user's query to the chat history
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    # Display a funny GIF while the model is thinking
    loading_placeholder = st.empty()
    loading_placeholder.markdown("Assistant is thinking of a response...")

    # Get the assistant's reponse
    response = dummy.get_response(query, st.session_state.thread_id,
                                  st.session_state.assistant_id,
                                  st.session_state.client)

    # Remove the placeholder GIF
    loading_placeholder.empty()

    # Display the assistant's reply
    with st.chat_message("assistant"):
        st.markdown(f"Assistant: {response}")

    # Add the assistant's response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )


