import pandas as pd
import uuid
import json
from config import HISTORY_DB_PATH
import os


def create_conversation_id():
    return str(uuid.uuid1())

def store_history(message,db_path):
    if message != []:
        with open(db_path, "w",encoding='utf-8') as f:
            json.dump(message, f,ensure_ascii=False, indent=4)
        
def load_history():
    chat_history = []
    for dir,_,f_list in os.walk(HISTORY_DB_PATH):
        for f in f_list:
            with open(os.path.join(dir,f),"r",encoding='utf-8') as file:
                chat_history.append((f.replace('.json',''),json.load(file)))
    return chat_history
                
def get_button_label(history):
    if len(history)>=1:
        return f"{history[-1].get('content','Chat History')[:10]}..."
    return "Chat History"


if __name__ == '__main__':
    chat_history = load_history()
    print(chat_history)