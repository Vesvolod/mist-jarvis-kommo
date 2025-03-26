from fastapi import FastAPI, Request
import openai
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Подгружаем ключи и токены из переменных окружения Railway
openai.api_key = os.getenv('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')
KOMMO_WHATSAPP_URL = os.getenv('KOMMO_WHATSAPP_URL')
KOMMO_WHATSAPP_TOKEN = os.getenv('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6Ijk0NmM4YjI4NjY5MmU2NTA2YzBmYWUyNzM4MGJkZWI3OGQwMjVjNmRjODIzNWI5ZjdlNzNiZTJjZDJiMWU0NGMxMGQ1YjcyYWM3Nzc4ZTRiIn0.eyJhdWQiOiJmMzczYWU0NS0zZmJhLTQ2YzAtYjg3MS05NTc2Y2Y3NDU0NGQiLCJqdGkiOiI5NDZjOGIyODY2OTJlNjUwNmMwZmFlMjczODBiZGViNzhkMDI1YzZkYzgyMzViOWY3ZTczYmUyY2QyYjFlNDRjMTBkNWI3MmFjNzc3OGU0YiIsImlhdCI6MTc0Mjk2NzYwNCwibmJmIjoxNzQyOTY3NjA0LCJleHAiOjE3NTQwOTI4MDAsInN1YiI6IjEyMzg1ODkxIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMzODc5NzQ3LCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZjE1NzIwN2UtZjRiNC00MmIxLWI0YjUtNWE2NDRlYTkxMjlmIiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.fwjRKAk8mpJ9u8eVWsHofHLYrjyDru2wZuN2RQNy6M-6aQkEK9xmfcDYYXsyWj4QxLYq1hFfbPDGc5sztNh9r0g6dAP6rGFzwCNjWh49b-8RQFTvT0UOiXq4kmJIoAA3hFpVAZDXVjS5lbxYiYucpjuoAb2b-fszXP0zaf9vpl5zVesUU9JmVojYO8onxozQQ3-b-L04QR_0NnhGqeeioHj8IRldIRlvxZDI2xt5i-9sXcBQeMn7lha1gqrxxfvl99kK6J2Rz18xEgzDaVPC3ev7tifj0h6pskJjRED9x7FQoC6vjLw0JH-V9DbeR1GwGehCsnwSxei_4EMfNjMR4A')

@app.get("/")
async def home():
    return {"status": "Mist Jarvis активен и готов продавать!"}

@app.post("/kommo-webhook")
async def kommo_webhook(request: Request):
    data = await request.json()

    # Безопасная проверка webhook данных
    try:
        message_text = data['message']['text']
        chat_id = data['message']['chat_id']
    except KeyError:
        return {"status": "ignored", "reason": "Неправильная структура webhook"}

    # Отправляем запрос в ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты менеджер компании Mist System, продаёшь системы туманообразования. Общайся дружелюбно, кратко, выводи клиента к встрече или покупке."},
            {"role": "user", "content": message_text}
        ],
        temperature=0.7,
        max_tokens=200
    )

    reply = response.choices[0].message.content.strip()

    # Отправка ответа клиенту через KommoCRM (WhatsApp)
    headers = {
        "Authorization": f"Bearer {KOMMO_WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "chat_id": chat_id,
        "text": reply
    }

    send_response = requests.post(KOMMO_WHATSAPP_URL, json=payload, headers=headers)

    return {"status": "sent", "reply": reply, "kommo_response": send_response.json()}
