import streamlit as st
from chat import llm_chat,request_test
from config import MODEL_CONFIGS,HISTORY_DB_PATH
from history import create_conversation_id,store_history,load_history,get_button_label
import numpy as np
import json
import os
import uuid
import streamlit as st

st.title("ChatGPT-like clone")


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream((llm_chat(st.session_state.messages, {})))
    st.session_state.messages.append({"role": "assistant", "content": response})