import pytest
import os
from dotenv import load_dotenv

# Adjust import paths based on your actual project structure
from arcade_aakeedo_kanji.http_clients.wanikani_api_http_client import fetch_wanikani_user_info
from arcade_aakeedo_kanji.models.wanikani_api_models import UserData

# Load environment variables from .env file in the project root
# This assumes your tests are run from a context where the .env file is discoverable
# (e.g., project root, or the .env file is in the same directory as this test file)
# For more robust path handling, you might adjust the path to .env if needed.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env') # Assumes .env is in project root, tests in a subdir
if not os.path.exists(dotenv_path):
    # Fallback if tests are run from project root directly
    dotenv_path = os.path.join(os.getcwd(), '.env') 
load_dotenv(dotenv_path=dotenv_path, override=True)


# Retrieve the API token from environment variables
# The test will be skipped if the token is not found.
WANIKANI_API_TOKEN_FROM_ENV = os.getenv("WANIKANI_API_TOKEN")

@pytest.mark.skipif(not WANIKANI_API_TOKEN_FROM_ENV, reason="WANIKANI_API_TOKEN not found in environment variables or .env file.")
@pytest.mark.asyncio
async def test_fetch_wanikani_user_info_success_live():
    """
    Tests fetching user information against the live WaniKani API.
    Verifies that a UserData instance is returned with username and level.
    Requires WANIKANI_API_TOKEN to be set in the environment or a .env file.
    """
    assert WANIKANI_API_TOKEN_FROM_ENV is not None, "Test setup error: API token should be loaded."

    print(f"Attempting WaniKani API call with token: {'*' * (len(WANIKANI_API_TOKEN_FROM_ENV) - 4) + WANIKANI_API_TOKEN_FROM_ENV[-4:] if WANIKANI_API_TOKEN_FROM_ENV else 'None'}")

    result = await fetch_wanikani_user_info(api_token=WANIKANI_API_TOKEN_FROM_ENV)

    assert result is not None, \
        "API call returned None. Check debug logs from the client for connection or API errors."
    
    assert isinstance(result, UserData), \
        f"Result should be an instance of UserData. Got type: {type(result)}"
        
    assert isinstance(result.username, str) and len(result.username) > 0, \
        "UserData should have a non-empty username string."
        
    assert isinstance(result.level, int) and 1 <= result.level <= 60, \
        "UserData should have a level between 1 and 60 (inclusive)."

    print(f"Successfully fetched WaniKani user: {result.username}, Level: {result.level}")

