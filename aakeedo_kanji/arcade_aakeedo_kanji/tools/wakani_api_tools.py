from arcade.sdk import ToolContext, tool

from arcade_aakeedo_kanji.http_clients.wanikani_api_http_client import \
    fetch_wanikani_user_info
from arcade_aakeedo_kanji.models.wanikani_api_models import UserData
from arcade_aakeedo_kanji.util import consts


@tool(requires_secrets=[consts.WANIKANI_API_TOKEN_ARCADE_SECRET_ID])
async def get_user_information(context: ToolContext) -> str:
    """
    Gets WaniKani user's information (username and current WaniKani level).
    Returns a string with the username, numerical level, and the level represented in Japanese.
    This information can give an indication of the user's progress and familiarity with
    Kanjis as per the WaniKani system. If the API token is missing or an error occurs
    during fetching, an appropriate message is returned.
    """
    api_token = context.get_secret(consts.WANIKANI_API_TOKEN_ARCADE_SECRET_ID)

    if not api_token:
        return "No WaniKani API token provided, so no user information can be fetched."

    user_data: UserData | None = await fetch_wanikani_user_info(api_token)

    if user_data:
        return user_data.model_dump_json()
    else:
        return "Could not retrieve WaniKani user information due to an API error, invalid data, or token issue."
