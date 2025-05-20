import logging
import pytest
from arcade.sdk.errors import ToolExecutionError
from arcade.sdk import tool, ToolContext

from arcade_aakeedo_kanji.tools.hello import say_hello
from arcade_aakeedo_kanji.tools.wakani_api_tools import get_user_information
from arcade_aakeedo_kanji.util import consts


def test_hello() -> None:
    assert say_hello("developer") == "Hello, developer!"

def test_hello_raises_error() -> None:
    with pytest.raises(ToolExecutionError):
        say_hello(1)

# @pytest.mark.asyncio
# async def test_hello_raises_errorss() -> None:
#     context = ToolContext()
#     context.set_secret(key=consts.WANIKANI_API_TOKEN_ARCADE_SECRET_ID, value="")
#     tst = await get_user_information(context, 1)
    
#     print(tst)
#     logging.error(tst)
    
#     assert True == True
