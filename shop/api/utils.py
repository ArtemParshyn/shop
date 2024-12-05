import requests


def create_payment_address(confirmations=None):
    data = {
        "forwarding_address": "0x8BF1DB45Dcf0CA738D599b8e6b9906ABE9634118",
        "callback_link": "https://ebbd-178-155-5-216.ngrok-free.app/topup/callback"
    }

    if confirmations:
        data["confirmations"] = confirmations

    url = f"https://api.bitaps.com/eth/testnet/v1/create/payment/address"

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error creating payment address: {response.text}")
