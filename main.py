import streamlit as st
from chat import llm_chat,request_test
from config import MODEL_CONFIGS,HISTORY_DB_PATH
from history import create_conversation_id,store_history,load_history,get_button_label
import numpy as np
import json
import os
import uuid

if __name__ == '__main__':
    model_name_list = [m.get("model").get("name") for m in MODEL_CONFIGS]
    model_config_list = [m.get("model") for m in MODEL_CONFIGS]
    with st.sidebar:
        current_model_name = st.selectbox('Select your model',model_name_list)
       # temperature = st.slider("Creativity", 0.0, 1.5, 0.95, step=0.01)
        choose=st.radio("***Creativity***",("Low","***Neutral***",":rainbow[High]"),horizontal=True)
    if choose == "Low":
        temperature=0.05
    elif choose == "High":
        temperature=0.95
    else:
        temperature=0.5
    model_options = {"temperature":temperature,}
    model_config = model_config_list[model_name_list.index(current_model_name)]
    
    #######################################################################
    st.title(f"🤖{model_config.get('name','Chatbot')}")
    if "conversation_id" not in st.session_state:
        st.session_state["conversation_id"] = create_conversation_id()
    db_path = os.path.join(HISTORY_DB_PATH,st.session_state["conversation_id"]+'.json')
    #######################################################################
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    if st.sidebar.button('***New chat***', type="primary", use_container_width=True):
        st.session_state["messages"] = [] 
        st.session_state["conversation_id"] = create_conversation_id() 

    history_list = load_history() # load history
    
    if len(history_list) != 0:  # if I have history
        for c_id, history in history_list:  
            button_label = get_button_label(history)    #display history button
            if st.sidebar.button(button_label, key=c_id, use_container_width=True):
                st.session_state["conversation_id"] = c_id # restore id and history
                st.session_state["messages"] = history

                          
    #print(st.session_state.messages)
    # display history content in the main page
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"]) 
                      
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            response = st.write_stream(llm_chat(st.session_state.messages, model_config, model_options))
        st.session_state.messages.append({"role": "assistant", "content": response})
        store_history(st.session_state.messages, db_path)  # Store the updated messages

    #if "messages" in st.session_state and len(st.session_state["messages"]) != 0:
    #   store_history(st.session_state.messages,db_path)
