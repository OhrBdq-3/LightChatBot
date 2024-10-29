import os
import re
import io
import contextlib
from chat import chat_nonstream,llm_chat
import subprocess
from typing import Dict,List
from config import DEFAULT_MODEL

def extract_python_code(text):
    # Regular expression to match Python code blocks
    pattern = r'```python\n(.*?)\n```'
    
    # Use re.DOTALL to allow '.' to match newlines
    matches = re.findall(pattern, text, re.DOTALL)
    
    return matches

def verify_python(code_string:str):
    try:
        compile(code_string,'<string>','exec')
        return True
    except SyntaxError:
        return False
def run_python(code_string:str):
    output = io.StringIO()
    err_output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(err_output):
        exec(code_string)
    if err_output.getvalue().strip():
        print(err_output.getvalue())
    return output.getvalue()
    
def save_python_and_run(code_string):
    with open('tmp.py','w',encoding='utf-8') as f:
        f.write(code_string)
    result = subprocess.run(['python', 'tmp.py'], capture_output=True, text=True)
    print("Output:", result.stdout)
    print("Error (if any):", result.stderr)    
    
def code_agent(prompt,config:Dict=DEFAULT_MODEL):
    message = [
        {'role':'system','content':"You are a helpful assistant.\nDecide if user's question can be resolved by a python code, or user asked you to write some python code. If yes, say `yes`. If no, say `no`."},
        {'role':'user','content':prompt}
        ]
    text = chat_nonstream(message,config)
    if 'yes' in text:
        print('yes')
    else:
        print('no')    
if __name__ == '__main__':
    prompt = "Help me write a python code to find the sum of two numbers"
    code_agent(prompt)