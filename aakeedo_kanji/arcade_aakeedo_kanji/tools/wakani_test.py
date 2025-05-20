import json
from typing import Annotated

from arcade.sdk import tool, ToolContext
from arcade_aakeedo_kanji.util import consts
import httpx

BASE_URL = "https://api.wanikani.com/v2/"

@tool(requires_secrets=[consts.WANIKANI_API_TOKEN_ARCADE_SECRET_ID])
async def get_user_information(context: ToolContext, name: Annotated[str, "nothing"]) -> str:
    "Gets wanikani users information"
    headers = {
        "Authorization": f"Bearer {context.get_secret(consts.WANIKANI_API_TOKEN_ARCADE_SECRET_ID)}",
        "Wanikani-Revision": "20170710"
    }
    
    
    url = f"{BASE_URL}user"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)

            # Log status and headers
            print(f"Status code: {response.status_code}")
            print(f"Headers: {response.headers}")

            # Log response body (text or json)
            print(f"Response body:\n{response.text}")
            return response.text

        except httpx.HTTPStatusError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.text}")
        except httpx.RequestError as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
    return ""