from yookassa import Configuration, Payment

from config import YOU_MONYE_API_KEY, SHOP_ID


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
            "return_url": "http://127.0.0.1:8000/payment/success"
        },
        "capture": True,
        "description": description,
        "metadata": {
            "order_id": payment_id
        }
    })  
    
    payment_url = payment.confirmation.confirmation_url
    
    return payment_url