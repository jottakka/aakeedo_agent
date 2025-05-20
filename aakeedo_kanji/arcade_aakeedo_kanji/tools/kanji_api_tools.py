import json
from typing import Annotated, Optional

from arcade.sdk import tool

from arcade_aakeedo_kanji.http_clients.kanji_api_http_client import (
    fetch_kanji_details,
    fetch_joyo_kanji_list,
    fetch_kanji_list,
    fetch_kanji_by_reading,
    fetch_words_for_kanji
)

@tool()
async def get_kanji_details(
    kanji_char: Annotated[str, "A single Japanese kanji character (e.g., '桜', '字')."]
) -> Annotated[Optional[str], "A JSON string with kanji details (see docstring for structure), or None on error."]:
    """
    Fetches detailed information for a specific Japanese kanji character.

    Args:
        kanji_char: The single Japanese kanji character to look up.

    Returns:
        Optional[str]: A JSON string representing an object with detailed kanji information,
        or None if the kanji is not found, input is invalid, or an API error occurs.
        The JSON object includes the following fields:
        - 'kanji': str (The kanji character itself)
        - 'grade': Optional[int] (Official grade: 1-6 Kyōiku, 8 Jōyō, 9 Jinmeiyō)
        - 'stroke_count': int (Total number of strokes)
        - 'meanings': List[str] (English meanings)
        - 'kun_readings': List[str] (Kun'yomi readings, typically hiragana)
        - 'on_readings': List[str] (On'yomi readings, typically katakana)
        - 'name_readings': List[str] (Special readings for names - nanori)
        - 'jlpt': Optional[int] (Former JLPT level: 1-4)
        - 'unicode': str (Unicode codepoint, e.g., '871c')
        - 'heisig_en': Optional[str] (Heisig keyword from 'Remembering the Kanji')
        - 'freq_mainichi_shinbun': Optional[int] (Frequency rank in Mainichi Shinbun newspaper)
        - 'unihan_cjk_compatibility_variant': Optional[str] (Unified version if a compatibility variant)
        - 'notes': List[str] (Any miscellaneous notes about the kanji)
    """
    result_model = await fetch_kanji_details(kanji_char)
    if result_model:
        return json.dumps(result_model.model_dump(exclude_none=True))
    return None

@tool()
async def list_joyo_kanji(
) -> Annotated[Optional[str], "A JSON string array of Jōyō kanji characters, or None on error."]:
    """
    Fetches the complete list of Jōyō (commonly used) kanji characters.
    Jōyō kanji are officially recognized for general use in contemporary Japanese.

    Returns:
        Optional[str]: A JSON string representing an array of Jōyō kanji characters (strings).
        Returns None if an API error occurs or the data format is unexpected.
    """
    joyo_list = await fetch_joyo_kanji_list()
    if joyo_list is not None:
        return json.dumps(joyo_list)
    return None

@tool()
async def get_kanji_list_by_category(
    list_name: Annotated[str, "Category name (e.g., 'joyo', 'jinmeiyo', 'grade-1', 'jlpt-n1', 'all')."]
) -> Annotated[Optional[str], "A JSON string array of kanji for the category (see docstring), or None on error."]:
    """
    Fetches a list of kanji by a specified category name from the KanjiAPI.

    Valid list_name values include: 'joyo', 'jinmeiyo', 'heisig', 'kyouiku',
    'grade-1' through 'grade-6', 'grade-8', 'jlpt-5' through 'jlpt-1', 'all'.

    Args:
        list_name: The category name of the kanji list to fetch.

    Returns:
        Optional[str]: A JSON string representing an array of kanji characters (strings)
        for the specified category. Returns None if the category is not found,
        the input is invalid, or an API error occurs.
    """
    kanji_list = await fetch_kanji_list(list_name)
    if kanji_list is not None:
        return json.dumps(kanji_list)
    return None

@tool()
async def get_kanji_by_reading(
    reading_value: Annotated[str, "Japanese reading in hiragana or katakana (e.g., 'みつ', 'ニチ')."]
) -> Annotated[Optional[str], "A JSON string with kanji for the reading (see docstring for structure), or None on error."]:
    """
    Fetches lists of kanji associated with the supplied Japanese reading (kana).

    Args:
        reading_value: The reading in hiragana or katakana.

    Returns:
        Optional[str]: A JSON string representing an object containing the reading and
        associated kanji lists, or None if the reading is not found or an error occurs.
        The JSON object includes the following fields:
        - 'reading': str (The reading itself, e.g., 'みつ')
        - 'main_kanji': List[str] (Kanji characters that commonly use this reading)
        - 'name_kanji': List[str] (Kanji characters that use this reading primarily in names)
    """
    result_model = await fetch_kanji_by_reading(reading_value)
    if result_model:
        return json.dumps(result_model.model_dump(exclude_none=True))
    return None

@tool()
async def get_words_for_kanji(
    kanji_char: Annotated[str, "A single Japanese kanji character (e.g., '蜜', '食')."]
) -> Annotated[Optional[str], "A JSON string array of word entries for the kanji (see docstring for structure), or None on error."]:
    """
    Fetches a list of dictionary word entries associated with the supplied kanji character.

    Args:
        kanji_char: A single kanji character.

    Returns:
        Optional[str]: A JSON string representing an array of word entry objects, or None
        if the kanji is not found, input is invalid, or an API error occurs.
        Each word entry object in the JSON array has the following structure:
        - 'meanings': List of meaning objects. Each meaning object contains:
            - 'glosses': List[str] (English equivalent terms or explanations)
        - 'variants': List of variant objects. Each variant object contains:
            - 'written': str (The written form of the variant, e.g., '食べる')
            - 'pronounced': Optional[str] (The pronounced form in kana, e.g., 'たべる')
            - 'priorities': List[str] (Frequency or usage list tags, e.g., 'ichi1', 'news1')
    """
    result_models = await fetch_words_for_kanji(kanji_char)
    if result_models:
        dict_list = [entry.model_dump(exclude_none=True) for entry in result_models]
        return json.dumps(dict_list)
    return None
