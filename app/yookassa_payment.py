from yookassa import Configuration, Payment

from config import YOU_MONYE_API_KEY, SHOP_ID, CHANNEL_ID


Configuration.secret_key = YOU_MONYE_API_KEY
Configuration.account_id  = SHOP_ID

async def yookassa_payment(payment_id: str, amount: int, description: str):
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/<имя бота>?start=payment_success"
        },
        "capture": True,
        "description": description,
        "metadata": {
            "order_id": payment_id
        }
    })  
    
    payment_url = payment.confirmation.confirmation_url
    
    return payment_url
