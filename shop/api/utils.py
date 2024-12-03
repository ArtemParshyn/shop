from urllib.parse import urlencode

import requests
from django.conf import settings


def create_payment_address(callback_url, payout_address=3, confirmations=None):
    # Формируем тело запроса в формате JSON
    data = {
        "forwarding_address": "bc1qdhu5w865s0hcm4akzeqw3yxqlhf2l600y2ktkrmdeezvhcqjashs7p4h6j",
        "callback_link": "https://a57e-178-155-5-216.ngrok-free.app/topup/callback"
    }

    # Если количество подтверждений указано, добавляем его в данные
    if confirmations:
        data["confirmations"] = confirmations

    # API URL для создания адреса
    url = f"https://api.bitaps.com/btc/testnet/v1/create/payment/address"

    # Отправляем POST запрос с JSON данными
    response = requests.post(url, json=data)

    # Проверяем статус ответа
    if response.status_code == 200:
        return response.json()  # Возвращаем данные из ответа в формате JSON
    else:
        raise Exception(f"Error creating payment address: {response.text}")
