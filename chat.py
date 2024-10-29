import requests
import json
import time
from typing import Dict,List
from config import SLEEP_TIME

def smooth_print(text:str):
    for char in text:
        yield char
        time.sleep(SLEEP_TIME)
        
def request_test(config:Dict):
    model = config.get("model","")
    url = config.get("url","")
    payload = {
        "model": model,
        "messages": "Hi",
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        return True
    except requests.exceptions.RequestException as e:
        #print("error requesting")
        return False
    
def llm_chat(message:List,config:Dict,options:Dict = {}):
    model = config.get("name", "llama3.2:1b")
    url = config.get("url", "http://127.0.0.1:11433/api/chat")
    payload = {
        "model": model,
        "messages": message,
        "stream": True
    }
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ""
    all_answer = ''
    try:
        for line in response.iter_content(None, decode_unicode=True):
            if line:
                resp = json.loads(line)
                answer = resp.get('message', {}).get("content", "")
                for char in answer:
                    yield char
    except json.JSONDecodeError:
        print("\nError: Failed to decode the response.")
        return all_answer
    
def chat_nonstream(message:List,config:Dict):
    model = config.get("name","qwen2.5-coder:1.5b")
    url = config.get("url", "http://127.0.0.1:11433/api/chat")
    payload = {
        "model":model,
        "messages":message,
        "stream":False
    }
    try:
        response = requests.post(url,json=payload,stream=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return ""
    return response.json().get('message').get('content')

if __name__ == '__main__':
    message = [
        {'role':'user','content':'write a simple python code'}
    ]
    x = chat_nonstream(message,{})
    print(x)