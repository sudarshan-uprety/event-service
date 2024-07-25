import requests

api_gateway_url = 'https://your-api-id.execute-api.your-region.amazonaws.com/prod/your-endpoint'
headers = {
    'x-api-key': 'your-api-key'
}

response = requests.post(api_gateway_url, json={'key': 'value'}, headers=headers)
print(response.json())
