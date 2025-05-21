import traceback

import httpx

from arcade_aakeedo_kanji.config import aakeedo_config
from arcade_aakeedo_kanji.models.kanji_api_models import (KanjiDetailModel,
                                                          KanjiReading,
                                                          WordEntry)


async def fetch_kanji_details(kanji_char: str) -> KanjiDetailModel | None:
    """
    Fetches detailed information for a specific Japanese kanji character from the KanjiAPI.

    This function queries the configured KanjiAPI endpoint for a single kanji
    character. On success, it returns a `KanjiDetailModel` object containing
    various properties of the kanji, such as its readings (kun'yomi, on'yomi),
    meanings, stroke count, grade level, JLPT level, Unicode representation,
    and other related data as defined in `KanjiDetailModel`.

    Client-side validation ensures that the input `kanji_char` must be a single
    character string. If this validation fails, the function returns `None` without
    making an API call.

    If an API call is made, `None` is returned in several error scenarios:
    - HTTP errors (e.g., 404 Not Found if the kanji doesn't exist, 5xx server errors).
    - Network issues (e.g., `httpx.RequestError`, `httpx.TimeoutException`).
    - Problems parsing the API response (e.g., malformed JSON, or JSON structure
      that doesn't match `KanjiDetailModel`).

    Args:
        kanji_char: A single Japanese kanji character (e.g., "桜", "字") for
                    which details are to be fetched.

    Returns:
        An `Optional[KanjiDetailModel]` object. This will be an instance of
        `KanjiDetailModel` populated with the kanji's details if the API call
        is successful and the response is valid. Returns `None` if `kanji_char`
        is invalid, the kanji is not found, any network or API error occurs,
        or if the response data cannot be parsed into the model.
    """
    if not isinstance(kanji_char, str) or len(kanji_char) != 1:
        return None

    endpoint = f"/kanji/{kanji_char}"
    base_url_str = str(aakeedo_config.get_env_configs().kanji_api_base_url)

    async with httpx.AsyncClient(base_url=base_url_str) as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            return KanjiDetailModel(**response.json())
        except httpx.HTTPStatusError:
            return None
        except (httpx.RequestError, httpx.TimeoutException):
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_kanji_details:")
            print("  Function: fetch_kanji_details")
            print(f"  Input: kanji_char='{kanji_char}'")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None


async def fetch_joyo_kanji_list() -> list[str] | None:
    """
    Fetches the complete list of Jōyō (commonly used) kanji characters from the KanjiAPI.

    Jōyō kanji are those officially recognized for general use in contemporary
    Japanese. This function queries the KanjiAPI endpoint dedicated to providing
    this list.

    On success, it returns a list of strings, where each string is a single
    Jōyō kanji character.

    If the API call is unsuccessful or the response is not as expected, this
    function returns `None`. This can occur due to:
    - HTTP errors from the API (e.g., 404 if the endpoint changes, 5xx server errors).
    - Network issues (`httpx.RequestError`, `httpx.TimeoutException`).
    - The API response not being a valid JSON list of strings.

    Returns:
        An `Optional[List[str]]`. This will be a list of Jōyō kanji characters
        if the API call is successful and the response is a valid list of strings.
        Returns `None` if any error occurs during the API interaction or
        response processing.
    """
    endpoint = "/kanji/joyo"
    base_url_str = str(aakeedo_config.get_env_configs().kanji_api_base_url)

    async with httpx.AsyncClient(base_url=base_url_str) as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return data
            else:
                print("\nDEBUG: Unexpected data format in fetch_joyo_kanji_list.")
                print("  Function: fetch_joyo_kanji_list")
                print("  Expected: List of strings")
                print(f"  Received Type: {type(data).__name__}")
                return None
        except httpx.HTTPStatusError:
            return None
        except (httpx.RequestError, httpx.TimeoutException):
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_joyo_kanji_list:")
            print("  Function: fetch_joyo_kanji_list")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None


async def fetch_kanji_list(list_name: str) -> list[str] | None:
    """
    Fetches a list of kanji by a specified category name from the KanjiAPI.

    Valid list_name values include: 'joyo', 'jinmeiyo', 'heisig', 'kyouiku',
    'grade-1' through 'grade-6', 'grade-8', 'jlpt-5' through 'jlpt-1', 'all'.

    Args:
        list_name: The category name of the kanji list to fetch (e.g., "jinmeiyo", "grade-1").

    Returns:
        A list of kanji characters if successful, otherwise None.
    """
    if not list_name:
        return None

    endpoint = f"/kanji/{list_name}"
    base_url_str = str(aakeedo_config.get_env_configs().kanji_api_base_url)

    async with httpx.AsyncClient(base_url=base_url_str) as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return data
            else:
                print("\nDEBUG: Unexpected data format in fetch_kanji_list.")
                print("  Function: fetch_kanji_list")
                print(f"  Input: list_name='{list_name}'")
                print("  Expected: List of strings")
                print(f"  Received Type: {type(data).__name__}")
                return None
        except httpx.HTTPStatusError:
            return None
        except (httpx.RequestError, httpx.TimeoutException):
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_kanji_list:")
            print("  Function: fetch_kanji_list")
            print(f"  Input: list_name='{list_name}'")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None


async def fetch_kanji_by_reading(reading_value: str) -> KanjiReading | None:
    """
    Fetches lists of kanji associated with the supplied reading (kana).

    Args:
        reading_value: The reading in hiragana or katakana (e.g., "みつ", "ニチ").

    Returns:
        A KanjiReading object containing the reading and associated kanji lists
        if successful, otherwise None.
    """
    if not reading_value:
        return None

    endpoint = f"/reading/{reading_value}"
    base_url_str = str(aakeedo_config.get_env_configs().kanji_api_base_url)

    async with httpx.AsyncClient(base_url=base_url_str) as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            return KanjiReading(**response.json())
        except httpx.HTTPStatusError:
            return None
        except (httpx.RequestError, httpx.TimeoutException):
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_kanji_by_reading:")
            print("  Function: fetch_kanji_by_reading")
            print(f"  Input: reading_value='{reading_value}'")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None


async def fetch_words_for_kanji(kanji_char: str) -> list[WordEntry] | None:
    """
    Fetches a list of dictionary word entries associated with the supplied kanji character.

    Args:
        kanji_char: A single kanji character (e.g., "蜜", "食").

    Returns:
        A list of WordEntry objects if successful, otherwise None.
    """
    if not isinstance(kanji_char, str) or len(kanji_char) != 1:
        return None

    endpoint = f"/words/{kanji_char}"
    base_url_str = str(aakeedo_config.get_env_configs().kanji_api_base_url)

    async with httpx.AsyncClient(base_url=base_url_str) as client:
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            response_data = response.json()
            if isinstance(response_data, list):
                # This list comprehension can raise Pydantic ValidationError if an item is malformed
                return [WordEntry(**item) for item in response_data]
            else:
                print("\nDEBUG: Unexpected data format in fetch_words_for_kanji.")
                print("  Function: fetch_words_for_kanji")
                print(f"  Input: kanji_char='{kanji_char}'")
                print("  Expected: List of word entry objects")
                print(f"  Received Type: {type(response_data).__name__}")
                return None
        except httpx.HTTPStatusError:
            return None
        except (httpx.RequestError, httpx.TimeoutException):
            return None
        except Exception as e:
            print("\nDEBUG: Unexpected error in fetch_words_for_kanji:")
            print("  Function: fetch_words_for_kanji")
            print(f"  Input: kanji_char='{kanji_char}'")
            print(f"  Exception Type: {type(e).__name__}")
            print(f"  Exception Args: {e.args}")
            print("  Traceback:")
            traceback.print_exc()
            return None
