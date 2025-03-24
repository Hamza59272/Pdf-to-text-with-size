from mollie.api.client import Client
import os
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

MOLLIE_API_KEY = os.getenv("MOLLIE_API_KEY")

if not MOLLIE_API_KEY:
    raise ValueError("MOLLIE_API_KEY is not set. Please set it in your environment variables.")

mollie_client = Client()
mollie_client.set_api_key(MOLLIE_API_KEY)

class PaymentRequest(BaseModel):
    amount: float
    description: str
    redirect_url: str  # Redirect after payment

def create_mollie_payment(payment: PaymentRequest):
    try:
        # print("Got MOLLIE_API_KEY " , MOLLIE_API_KEY)
        payment_response = mollie_client.payments.create({
            "amount": {"currency": "EUR", "value": f"{payment.amount:.2f}"},
            "description": payment.description,
            "redirectUrl": payment.redirect_url,
        })
        return {"payment_id": payment_response["id"], "checkout_url": payment_response["_links"]["checkout"]["href"]}
    except Exception as e:
        return {"error": str(e)}
