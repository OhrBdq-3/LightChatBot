import os
import json

with open("models.json", "r",encoding='utf-8') as f:
    MODEL_CONFIGS = json.load(f)

SLEEP_TIME = 0.05
DEFAULT_MODEL = {"name": "llama3.2:1b","url": "http://127.0.0.1:11433/api/chat"}
HISTORY_DB_PATH = "history"