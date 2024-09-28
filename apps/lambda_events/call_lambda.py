import httpx

from utils.variables import LAMBDA_API, LAMBDA_API_KEY


async def call_lambda(data: dict):
    api_gateway_url = LAMBDA_API
    headers = {
        'X-API-KEY': LAMBDA_API_KEY,
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_gateway_url, headers=headers, json=data)
            response.raise_for_status()

            if response.status_code == 200:
                return response.text
            elif response.status_code == 400:
                return None
            else:
                return None
        except httpx.HTTPStatusError as e:
            if 400 < e.response.status_code < 500:
                return None
            else:
                raise
        except httpx.RequestError as e:
            raise
        except Exception as e:
            raise