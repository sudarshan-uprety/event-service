import aiohttp

from utils.variables import LAMBDA_API, LAMBDA_API_KEY


async def call_lambda(data: dict):
    api_gateway_url = LAMBDA_API
    headers = {
        'X-API-KEY': LAMBDA_API_KEY,
        'Content-Type': 'application/json'
    }
    body = data
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_gateway_url, headers=headers, json=body) as response:
                if response.status == 200:
                    result = await response.text()
                    return result
                elif response.status == 400:
                    return None
                elif 400 < response.status < 500:
                    await response.raise_for_status()
                    return None
                else:
                    await response.raise_for_status()
                    return None
        except aiohttp.ClientResponseError as e:
            raise
        except aiohttp.ClientError as e:
            raise
        except Exception as e:
            raise
