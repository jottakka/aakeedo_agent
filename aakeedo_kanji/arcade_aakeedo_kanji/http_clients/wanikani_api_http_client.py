import traceback

import httpx

from arcade_aakeedo_kanji.config.aakeedo_config import get_env_configs
from arcade_aakeedo_kanji.models.wanikani_api_models import (UserData,
                                                             UserResponse)


async def fetch_wanikani_user_info(api_token: str) -> UserData | None:
    """
    Fetches user information (username and level) from the WaniKani API.

    This function makes an authenticated GET request to the /user endpoint of the
    WaniKani API v2. It requires a valid API token for authorization.

    Args:
        api_token: The WaniKani API v2 personal access token. This token should have
                   permissions to read user data.

    Returns:
        A `UserData` Pydantic model instance containing the user's username and level
        if the API call is successful and the response is valid.
        Returns `None` if the API token is not provided, if any network or HTTP error
        occurs (e.g., 401 Unauthorized, 403 Forbidden, 404 Not Found, 5xx server errors),
        or if the API response cannot be parsed into the expected model structure.
    """
    if not api_token:
        print("DEBUG CLIENT (fetch_wanikani_user_info): API token is missing. Cannot proceed.")
        return None

    config = get_env_configs()
    base_url_str = str(config.wanikani_api_base_url).rstrip("/")
    endpoint = "user"
    url = f"{base_url_str}/{endpoint}"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Wanikani-Revision": config.wanikani_api_revision,  # This comes from WaniKaniApiConfig
    }

    print(f"DEBUG CLIENT (fetch_wanikani_user_info): Requesting URL: '{url}'")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)

            response.raise_for_status()  # Raises HTTPStatusError for 4xx or 5xx responses

            response_json = response.json()
            user_response_model = UserResponse(**response_json)

            return user_response_model.data

        except httpx.HTTPStatusError as e_http:
            print("\nDEBUG: HTTPStatusError in fetch_wanikani_user_info:")
            print("  Function: fetch_wanikani_user_info")
            print(f"  URL: {e_http.request.url}")
            print(f"  Status Code: {e_http.response.status_code}")
            try:
                error_details = e_http.response.json()
                print(f"  API Error Details: {error_details}")
            except Exception:
                print(
                    f"  Response Body (text, could not parse as JSON): {e_http.response.text[:500]}..."
                )
            return None
        except (httpx.RequestError, httpx.TimeoutException) as e_req:
            print("\nDEBUG: RequestError/TimeoutException in fetch_wanikani_user_info:")
            print("  Function: fetch_wanikani_user_info")
            print(
                f"  URL: {e_req.request.url if hasattr(e_req, 'request') and e_req.request else 'N/A'}"
            )
            print(f"  Exception Type: {type(e_req).__name__}")
            print(f"  Exception Args: {e_req.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_wanikani_user_info:")
            print("  Function: fetch_wanikani_user_info")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None
