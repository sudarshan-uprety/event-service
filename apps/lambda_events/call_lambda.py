import requests
import json

from utils.variables import LAMBDA_API, LAMBDA_API_KEY


def call_lambda(data: dict, ch, method):
    try:
        api_gateway_url = LAMBDA_API
        headers = {
            'X-API-KEY': LAMBDA_API_KEY,
            'Content-Type': 'application/json'
        }
        body = data

        response = requests.post(api_gateway_url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            # acknowledge the message from queue
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Message {method.delivery_tag} acknowledged.")
        else:
            print(f"Failed to process message {method.delivery_tag}. Response code: {response.status_code}")
    except Exception as e:
        print(f"Failed to process message {method.delivery_tag}. Response code: {e}")
