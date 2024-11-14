from fastapi import FastAPI, Request
import os
import requests
from telegram import Bot

app = FastAPI()

# Configurações do Telegram e Mercado Pago
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MERCADO_PAGO_ACCESS_TOKEN = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

@app.post("/webhook")
async def mercado_pago_webhook(request: Request):
    data = await request.json()

    # Verifica se é uma notificação de pagamento aprovado
    if data.get("type") == "payment" and data.get("action") == "payment.updated":
        payment_id = data["data"]["id"]
        
        # Busca detalhes do pagamento
        headers = {"Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}"}
        response = requests.get(f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers)
        
        if response.status_code == 200:
            payment_info = response.json()
            status = payment_info.get("status")
            
            # Se o pagamento foi aprovado
            if status == "approved":
                bot.send_message(chat_id=CHAT_ID, text="Pagamento aprovado! Liberando acesso.")
                return {"status": "success"}

    return {"status": "ignored"}
