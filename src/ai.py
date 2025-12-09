import openai
from helpers import exception

#Ai func
max_token_count = 4096
messages = [
    {
        "role": "system",
        "content": "Im PupAI, assistant at uberpepolis channel"
    }
]

def update(messages, role, content):
    messages.append({"role": role, "content": content})

def reset_messages():
    messages.clear()
    messages.append({
        "role": "system", 
        "content": "Im PupAI, assistant at uberpepolis channel"
    })

async def pupai(message):
    try:
        update(messages, 'user', message.text)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            max_tokens=max_token_count,
        )

        if response['usage']['total_tokens'] >= max_token_count:
            await message.answer(
                f'В данный момент вы использовали максимум токенов в рамках контекста: {response["usage"]["total_tokens"]}, будет произведена очистка памяти')

            reset_messages()

        await message.answer(response['choices'][0]['message']['content'], parse_mode="HTML")
    
    except Exception as e:
        await exception()