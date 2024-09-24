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
                    print(f"Lambda function called successfully. Status code: {response.status}")
                    return result
                elif response.status == 400:
                    error_body = await response.text()
                    print(f"Bad Request error from Lambda function. Status code: {response.status}. Response: {error_body}")
                    return None  # or handle the error as appropriate for your use case
                elif 400 < response.status < 500:
                    print(f"Client error occurred while calling Lambda function. Status code: {response.status}")
                    await response.raise_for_status()
                else:
                    print(f"Server error occurred. Lambda function was not consumed. Status code: {response.status}")
                    await response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            print(f"Client response error occurred while calling Lambda function: {str(e)}")
            raise
        except aiohttp.ClientError as e:
            print(f"Network error occurred while calling Lambda function: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error occurred while calling Lambda function: {str(e)}")
            raise