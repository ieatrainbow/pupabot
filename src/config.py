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

#environment variables
tb_token = os.getenv("TB_TOKEN")
major_id = os.getenv("MAJOR_ID")
wiz_id = os.getenv("WIZ_ID")
pupa_id = os.getenv("PUPA_ID")
nick_id = os.getenv("NICK_ID")
test_chat_id = os.getenv("TEST_CHAT_ID")
test_chat_id_2 = os.getenv("TEST_CHAT_ID_2")
uberpepolis_chat_id = os.getenv("UBERPEPOLIS_CHAT_ID")
openai_token = os.getenv("OPENAI_TOKEN")

data_folder = os.getenv("DATA_FOLDER")