from openai import AsyncOpenAI
import config
import os
import json
from config import data_folder

PROMPT_PATH = f'{data_folder}/ai/prompts.json'

client = AsyncOpenAI(
    api_key=config.ai_token, 
    base_url="https://api.z.ai/api/paas/v4/"    
)

def load_system_prompt():
    if os.path.exists(PROMPT_PATH):
        try:
            with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("pupa")
        except Exception as e:
            print(f"Ошибка чтения JSON: {e}")
    
    return "Ты пожилой глэк. Пиши капсом и с ошибками."

SYSTEM_CONTENT = load_system_prompt()
SYSTEM_PROMPT = {"role": "system", "content": SYSTEM_CONTENT}
user_contexts = {}

def get_user_context(user_id):
    if user_id not in user_contexts:
        user_contexts[user_id] = [SYSTEM_PROMPT]
    return user_contexts[user_id]

async def pupai(message_text, user_id):
    clean_text = message_text.strip()
    if not clean_text:
        return "каво"
    
    context = get_user_context(user_id)
    
    if context[-1]["role"] == "user":
        context[-1]["content"] = clean_text
    else:
        context.append({"role": "user", "content": clean_text})

    response = None
    try:
        response = await client.chat.completions.create(
            model="glm-4.7-flash",
            messages=context,
            temperature=1.1,
            max_tokens=4096,
            presence_penalty=1.0 
        )

        answer = response.choices[0].message.content # Для GLM-4 часто работает индекс [0]
        
        context.append({"role": "assistant", "content": answer})
        
        if len(user_contexts[user_id]) > 11:
            user_contexts[user_id] = [SYSTEM_PROMPT] + user_contexts[user_id][-10:]

        return answer

    except Exception as e:
        if response:
            print(f"DEBUG FULL RESPONSE: {response}")
        print(f"Я УСТАЛ: {e}")
        return f"❌ Я УСТАЛ: {str(e)}"
