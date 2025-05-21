import json
from typing import Annotated

from arcade.sdk import tool
from arcade.sdk.errors import RetryableToolError, ToolExecutionError

from arcade_aakeedo_kanji.http_clients.kanji_api_http_client import (
    fetch_joyo_kanji_list, fetch_kanji_by_reading, fetch_kanji_details,
    fetch_kanji_list, fetch_words_for_kanji)


@tool()
async def get_kanji_details(
    kanji_char: Annotated[str, "A single Japanese kanji character (e.g., '桜', '字')."],
) -> Annotated[
    str,
    "A JSON string with kanji details (see docstring for structure), or an error is raised.",
]:
    """
    Fetches detailed information for a specific Japanese kanji character.

    Args:
        kanji_char: The single Japanese kanji character to look up.

    Returns:
        A JSON string representing an object with detailed kanji information.
        Raises ToolExecutionError if the kanji is not found, input is invalid, or an API error occurs.
        (Schema details from original docstring remain applicable for the success case JSON).
    """
    cleaned_kanji_char = kanji_char.strip() if isinstance(kanji_char, str) else ""
    if not cleaned_kanji_char or len(cleaned_kanji_char) != 1:
        raise RetryableToolError(
            f"Please provide a single, valid Japanese kanji character. The input '{kanji_char}' is not suitable.",
            developer_message=f"Invalid input for get_kanji_details: kanji_char must be a single non-whitespace string character. Received: '{kanji_char}', Cleaned: '{cleaned_kanji_char}'",
            additional_prompt_content="The provided input for the kanji character was invalid. Please ask the user for a single, specific kanji character.",
        )

    result_model = await fetch_kanji_details(cleaned_kanji_char)

    if result_model:
        return json.dumps(result_model.model_dump(exclude_none=True))
    else:
        raise ToolExecutionError(
            f"I couldn't find detailed information for the kanji '{cleaned_kanji_char}'. Please ensure it's a recognized Japanese kanji character.",
        )


@tool()
async def list_joyo_kanji() -> Annotated[
    str, "A JSON string array of Jōyō kanji characters, or an error is raised."
]:
    """
    Fetches the complete list of Jōyō (commonly used) kanji characters.
    Jōyō kanji are officially recognized for general use in contemporary Japanese.

    Returns:
        A JSON string representing an array of Jōyō kanji characters (strings).
        Raises ToolExecutionError if an API error occurs or the data format is unexpected.
    """
    joyo_list = await fetch_joyo_kanji_list()
    if joyo_list is not None:
        return json.dumps(joyo_list)
    else:
        raise ToolExecutionError(
            "Sorry, I was unable to retrieve the list of Jōyō kanji at this time. There might have been an issue communicating with the Kanji API.",
        )


@tool()
async def get_kanji_list_by_category(
    list_name: Annotated[
        str, "Category name (e.g., 'joyo', 'jinmeiyo', 'grade-1', 'jlpt-n1', 'all')."
    ],
) -> Annotated[str, "A JSON string array of kanji for the category, or an error is raised."]:
    """
    Fetches a list of kanji by a specified category name from the KanjiAPI.
    Valid list_name values include: 'joyo', 'jinmeiyo', 'heisig', 'kyouiku',
    'grade-1' through 'grade-6', 'grade-8', 'jlpt-n5' through 'jlpt-n1', 'all'.

    Args:
        list_name: The category name of the kanji list to fetch.

    Returns:
        A JSON string representing an array of kanji characters (strings) for the category.
        Raises ToolExecutionError if the category is not found, input is invalid, or an API error occurs.
    """
    cleaned_list_name = list_name.strip().lower() if isinstance(list_name, str) else ""
    if not cleaned_list_name:
        raise RetryableToolError(
            f"Please provide a valid category name for the kanji list. The input '{list_name}' is empty or invalid.",
            developer_message=f"Invalid input for get_kanji_list_by_category: list_name cannot be empty. Received: '{list_name}'",
            additional_prompt_content="A category name for the kanji list was not provided or was invalid. Please ask the user for a specific category (e.g., 'joyo', 'grade-1', 'jlpt-n3').",
        )

    kanji_list = await fetch_kanji_list(cleaned_list_name)
    if kanji_list is not None:
        return json.dumps(kanji_list)
    else:
        raise ToolExecutionError(
            f"I couldn't retrieve the kanji list for the category '{cleaned_list_name}'. Please ensure it's a recognized category name (like 'joyo', 'grade-1', 'jlpt-n3').",
        )


@tool()
async def get_kanji_by_reading(
    reading_value: Annotated[
        str, "Japanese reading in hiragana or katakana (e.g., 'みつ', 'ニチ')."
    ],
) -> Annotated[str, "A JSON string with kanji for the reading, or an error is raised."]:
    """
    Fetches lists of kanji associated with the supplied Japanese reading (kana).

    Args:
        reading_value: The reading in hiragana or katakana.

    Returns:
        A JSON string representing an object containing the reading and associated kanji lists.
        Raises ToolExecutionError if the reading is not found or an API error occurs.
        (Schema details from original docstring remain applicable for the success case JSON).
    """
    cleaned_reading_value = reading_value.strip() if isinstance(reading_value, str) else ""
    if not cleaned_reading_value:
        raise RetryableToolError(
            f"Please provide a Japanese reading (in hiragana or katakana) to search for. The input '{reading_value}' is empty or invalid.",
            developer_message=f"Invalid input for get_kanji_by_reading: reading_value cannot be empty. Received: '{reading_value}'",
            additional_prompt_content="A Japanese reading was not provided or was invalid. Please ask the user for a specific reading in kana.",
        )

    result_model = await fetch_kanji_by_reading(cleaned_reading_value)
    if result_model:
        return json.dumps(result_model.model_dump(exclude_none=True))
    else:
        raise ToolExecutionError(
            f"I couldn't find any kanji associated with the reading '{cleaned_reading_value}'. Please check the reading or try a different one.",
        )


@tool()
async def get_words_for_kanji(
    kanji_char: Annotated[str, "A single Japanese kanji character (e.g., '蜜', '食')."],
) -> Annotated[str, "A JSON string array of word entries for the kanji, or an error is raised."]:
    """
    Fetches a list of dictionary word entries associated with the supplied kanji character.

    Args:
        kanji_char: A single kanji character.

    Returns:
        A JSON string representing an array of word entry objects.
        Raises ToolExecutionError if the kanji is not found, input is invalid, or an API error occurs.
        (Schema details from original docstring remain applicable for the success case JSON).
    """
    cleaned_kanji_char = kanji_char.strip() if isinstance(kanji_char, str) else ""
    if not cleaned_kanji_char or len(cleaned_kanji_char) != 1:
        raise RetryableToolError(
            f"Please provide a single, valid Japanese kanji character to find words for. Input '{kanji_char}' is not suitable.",
            developer_message=f"Invalid input for get_words_for_kanji: kanji_char must be a single non-whitespace string character. Received: '{kanji_char}', Cleaned: '{cleaned_kanji_char}'",
            additional_prompt_content="The provided input for the kanji character was invalid. Please ask the user for a single, specific kanji character to search words for.",
        )

    result_models = await fetch_words_for_kanji(cleaned_kanji_char)
    if result_models is not None:
        dict_list = [entry.model_dump(exclude_none=True) for entry in result_models]
        return json.dumps(dict_list)
    else:
        raise ToolExecutionError(
            f"I couldn't retrieve words for the kanji '{cleaned_kanji_char}'. This might mean no words are listed for this kanji, or there was an issue fetching the data.",
        )
