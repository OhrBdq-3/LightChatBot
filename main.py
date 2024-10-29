import streamlit as st
from chat import llm_chat
from config import MODEL_CONFIGS,HISTORY_DB_PATH
from history import create_conversation_id,store_history,load_history,get_button_label
import os
import random
#import emoji

if __name__ == '__main__':
    
    model_name_list = [m.get("model").get("name") for m in MODEL_CONFIGS]
    model_config_list = [m.get("model") for m in MODEL_CONFIGS]
    if "creativity" not in st.session_state:
        st.session_state["creativity"] = False
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = 0.05   
    with st.sidebar:
        current_model_name = st.selectbox('Select your model',model_name_list)
        choose = st.radio("***Creativity***",("***Low***","***Neutral***",":rainbow[***High***]"),horizontal=True)
    if choose == "**Low**":
        st.session_state["temperature"] = 0.05
        st.session_state["creativity"] = False
    elif choose == ":rainbow[***High***]":
        st.session_state["temperature"] = 0.95
        st.session_state["creativity"] = True
    else:
        st.session_state["temperature"] = 0.5
        st.session_state["creativity"] = False
        
    model_options = {"temperature":st.session_state["temperature"]}
    model_config = model_config_list[model_name_list.index(current_model_name)]
    #all_emojis = list(emoji.EMOJI_DATA.keys())
    #if "emoji" not in st.session_state:
    #    st.session_state["emoji"] = random.choice(all_emojis)
    if st.session_state["creativity"]:
        llm_title = f"***:rainbow[{model_config.get('name','Chatbot')[0].upper()}{model_config.get('name','Chatbot')[1:]}]***"
    else:
        llm_title = f"***{model_config.get('name','Chatbot')[0].upper()}{model_config.get('name','Chatbot')[1:]}***"
    st.title(llm_title)
    st.markdown("***LLM can make mistakes. Check important info.***")
    if "conversation_id" not in st.session_state:
        st.session_state["conversation_id"] = create_conversation_id()
    db_path = os.path.join(HISTORY_DB_PATH,st.session_state["conversation_id"]+'.json')

    
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        
    if st.sidebar.button('***New chat***', type="primary", use_container_width=True):
        st.session_state["messages"] = [] 
        st.session_state["conversation_id"] = create_conversation_id() 

    history_list = load_history() 
    
    if len(history_list) != 0:  
        for c_id, history in history_list:  
            col1, col2 = st.sidebar.columns([5,1])
            button_label = get_button_label(history)   
            
            with col1:
                if st.button(button_label, key=c_id, use_container_width=True):
                    #st.session_state["emoji"] = random.choice(all_emojis)
                    st.session_state["conversation_id"] = c_id
                    st.session_state["messages"] = history

            with col2:
                if st.button("🗑️", key=f'delete_{c_id}'):
                    db_path = os.path.join(HISTORY_DB_PATH, f"{c_id}.json")
                    if os.path.exists(db_path):
                        os.remove(db_path)
                    st.rerun()
                    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"]) 
                      
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant"):
            response = st.write_stream(llm_chat(st.session_state.messages, model_config, model_options))
        st.session_state.messages.append({"role": "assistant", "content": response})
        store_history(st.session_state.messages, db_path)  
        st.rerun()