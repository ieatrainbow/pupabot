import asyncio
from ai import pupai

async def test():
    print("Отправка запроса в GLM...")
    # Имитируем запрос от юзера с ID 123
    response = await pupai("Привет! Ты работаешь?", 123)
    print(f"Ответ нейросети: {response}")

if __name__ == "__main__":
    asyncio.run(test())
