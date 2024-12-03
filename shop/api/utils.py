import requests


def create_payment_address(callback_url, payout_address=3, confirmations=None):
    data = {
        "forwarding_address": "bc1qdhu5w865s0hcm4akzeqw3yxqlhf2l600y2ktkrmdeezvhcqjashs7p4h6j",
        "callback_link": "https://a57e-178-155-5-216.ngrok-free.app/topup/callback"
    }

    if confirmations:
        data["confirmations"] = confirmations

    url = f"https://api.bitaps.com/btc/testnet/v1/create/payment/address"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error creating payment address: {response.text}")
