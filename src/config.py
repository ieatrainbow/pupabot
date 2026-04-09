import os
import sys 

def check_env():
    required = ['TB_TOKEN', 'DATA_FOLDER']
    
    for var in required:
        if not os.getenv(var):
            print(f"{var} is missing")
            print(f"check .env")
            sys.exit(1)
    
    print("env is ok")

check_env()

#ai config envs
AI_ENABLED = os.getenv('AI_ENABLED', 'false').lower() == 'true'
ai_token = os.getenv("AI_TOKEN")
ai_model = os.getenv("AI_MODEL")
ai_max_tokens = int(os.getenv("AI_MAX_TOKENS", "4096"))
ai_temperature = float(os.getenv("AI_TEMPERATURE", "1.1"))
ai_presence_penalty = float(os.getenv("AI_PRESENCE_PENALTY", "1.0"))

#telegram config envs
tb_token = os.getenv("TB_TOKEN")
major_id = os.getenv("MAJOR_ID")
wiz_id = os.getenv("WIZ_ID")
pupa_id = os.getenv("PUPA_ID")
nick_id = os.getenv("NICK_ID")
test_chat_id = os.getenv("TEST_CHAT_ID")
test_chat_id_2 = os.getenv("TEST_CHAT_ID_2")
uberpepolis_chat_id = os.getenv("UBERPEPOLIS_CHAT_ID")
debug_chat = os.getenv("DEBUG_CHAT_ID")

#bot envs
data_folder = os.getenv("DATA_FOLDER")