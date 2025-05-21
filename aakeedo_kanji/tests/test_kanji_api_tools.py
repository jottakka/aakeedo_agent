import pytest
import json
from unittest.mock import AsyncMock

from arcade_aakeedo_kanji.tools.kanji_api_tools import (
    get_kanji_details,
    list_joyo_kanji,
    get_kanji_list_by_category,
    get_kanji_by_reading,
    get_words_for_kanji
)
from arcade.sdk.errors import ToolExecutionError, RetryableToolError

PATCH_PREFIX = "arcade_aakeedo_kanji.tools.kanji_api_tools"

def create_mock_model(mocker, dump_data=None):
    mock_instance = mocker.MagicMock()
    mock_instance.model_dump.return_value = dump_data if dump_data is not None else {}
    return mock_instance

# --- Tests for get_kanji_details ---

@pytest.mark.asyncio
async def test_get_kanji_details_success(mocker):
    """Tests get_kanji_details successfully returns JSON when client provides data."""
    mock_data = {"kanji": "猫", "meanings": ["cat"], "stroke_count": 11}
    mock_model_instance = create_mock_model(mocker, dump_data=mock_data)
    
    mock_fetch = AsyncMock(return_value=mock_model_instance)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_details", new=mock_fetch)

    result = await get_kanji_details("猫")
    
    assert json.loads(result) == mock_data
    mock_fetch.assert_called_once_with("猫")
    mock_model_instance.model_dump.assert_called_once_with(exclude_none=True)

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_input, expected_msg_part", [
    ("", "provide a single, valid Japanese kanji character"),
    ("猫犬", "provide a single, valid Japanese kanji character"),
    (" ", "provide a single, valid Japanese kanji character"), 
    (None, "provide a single, valid Japanese kanji character"),
])
async def test_get_kanji_details_invalid_input(invalid_input, expected_msg_part):
    """Tests get_kanji_details raises RetryableToolError for invalid tool-level input."""
    with pytest.raises(RetryableToolError) as exc_info: # Expect RetryableToolError
        await get_kanji_details(invalid_input)
    assert expected_msg_part in str(exc_info.value) # Use str(exc_info.value)
    # For RetryableToolError, you also set developer_message and additional_prompt_content
    if hasattr(exc_info.value, 'developer_message'): # Check if attribute exists
        assert "Invalid input for get_kanji_details" in exc_info.value.developer_message
    if hasattr(exc_info.value, 'additional_prompt_content'):
        assert "ask the user for a single, specific kanji character" in exc_info.value.additional_prompt_content


@pytest.mark.asyncio
async def test_get_kanji_details_client_returns_none(mocker):
    """Tests get_kanji_details raises ToolExecutionError when client returns None."""
    valid_kanji_char_for_test = "字" # Use a valid single character to pass tool's input validation
    mock_fetch = AsyncMock(return_value=None)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_details", new=mock_fetch)

    with pytest.raises(ToolExecutionError) as exc_info:
        await get_kanji_details(valid_kanji_char_for_test) 
    
    expected_error_message = f"I couldn't find detailed information for the kanji '{valid_kanji_char_for_test}'. Please ensure it's a recognized Japanese kanji character."
    assert str(exc_info.value) == expected_error_message
    mock_fetch.assert_called_once_with(valid_kanji_char_for_test)


# --- Tests for list_joyo_kanji ---

@pytest.mark.asyncio
async def test_list_joyo_kanji_success(mocker):
    """Tests list_joyo_kanji successfully returns JSON when client provides data."""
    mock_list_data = ["一", "二", "三"]
    mock_fetch = AsyncMock(return_value=mock_list_data)
    mocker.patch(f"{PATCH_PREFIX}.fetch_joyo_kanji_list", new=mock_fetch)

    result = await list_joyo_kanji()
    
    assert json.loads(result) == mock_list_data
    mock_fetch.assert_called_once()

@pytest.mark.asyncio
async def test_list_joyo_kanji_client_returns_none(mocker):
    """Tests list_joyo_kanji raises ToolExecutionError when client returns None."""
    mock_fetch = AsyncMock(return_value=None)
    mocker.patch(f"{PATCH_PREFIX}.fetch_joyo_kanji_list", new=mock_fetch)

    with pytest.raises(ToolExecutionError) as exc_info:
        await list_joyo_kanji()
    
    expected_error_message = "Sorry, I was unable to retrieve the list of Jōyō kanji at this time. There might have been an issue communicating with the Kanji API."
    assert str(exc_info.value) == expected_error_message
    mock_fetch.assert_called_once()


# --- Tests for get_kanji_list_by_category ---

@pytest.mark.asyncio
async def test_get_kanji_list_by_category_success(mocker):
    """Tests get_kanji_list_by_category successfully returns JSON."""
    list_name = "grade-1"
    mock_list_data = ["日", "月", "火"]
    mock_fetch = AsyncMock(return_value=mock_list_data)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_list", new=mock_fetch)

    result = await get_kanji_list_by_category(list_name)

    assert json.loads(result) == mock_list_data
    mock_fetch.assert_called_once_with(list_name) 

@pytest.mark.asyncio
async def test_get_kanji_list_by_category_empty_list_success(mocker):
    """Tests get_kanji_list_by_category returns JSON for an empty list from client."""
    list_name = "rare-category"
    mock_list_data = [] 
    mock_fetch = AsyncMock(return_value=mock_list_data)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_list", new=mock_fetch)

    result = await get_kanji_list_by_category(list_name)
    assert json.loads(result) == []
    mock_fetch.assert_called_once_with(list_name)


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_input, expected_msg_part", [
    ("", "provide a valid category name"),
    (None, "provide a valid category name"),
])
async def test_get_kanji_list_by_category_invalid_input(invalid_input, expected_msg_part):
    """Tests get_kanji_list_by_category raises RetryableToolError for invalid tool-level input."""
    with pytest.raises(RetryableToolError) as exc_info: 
        await get_kanji_list_by_category(invalid_input)
    assert expected_msg_part in str(exc_info.value) 
    if hasattr(exc_info.value, 'developer_message'):
        assert "Invalid input for get_kanji_list_by_category" in exc_info.value.developer_message
    if hasattr(exc_info.value, 'additional_prompt_content'):
        assert "ask the user for a specific category" in exc_info.value.additional_prompt_content


@pytest.mark.asyncio
async def test_get_kanji_list_by_category_client_returns_none(mocker):
    """Tests get_kanji_list_by_category raises ToolExecutionError when client returns None."""
    list_name = "NonExistent-Category " 
    cleaned_list_name = "nonexistent-category"
    mock_fetch = AsyncMock(return_value=None)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_list", new=mock_fetch)

    with pytest.raises(ToolExecutionError) as exc_info:
        await get_kanji_list_by_category(list_name)
    
    expected_error_message = f"I couldn't retrieve the kanji list for the category '{cleaned_list_name}'. Please ensure it's a recognized category name (like 'joyo', 'grade-1', 'jlpt-n3')."
    assert str(exc_info.value) == expected_error_message
    mock_fetch.assert_called_once_with(cleaned_list_name)


# --- Tests for get_kanji_by_reading ---

@pytest.mark.asyncio
async def test_get_kanji_by_reading_success(mocker):
    """Tests get_kanji_by_reading successfully returns JSON."""
    reading_value = "みつ"
    mock_data = {"reading": "みつ", "main_kanji": ["蜜"]}
    mock_model_instance = create_mock_model(mocker, dump_data=mock_data)
    mock_fetch = AsyncMock(return_value=mock_model_instance)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_by_reading", new=mock_fetch)

    result = await get_kanji_by_reading(reading_value)

    assert json.loads(result) == mock_data
    mock_fetch.assert_called_once_with(reading_value)
    mock_model_instance.model_dump.assert_called_once_with(exclude_none=True)

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_input, expected_msg_part", [
    ("", "provide a Japanese reading"),
    (None, "provide a Japanese reading"),
])
async def test_get_kanji_by_reading_invalid_input(invalid_input, expected_msg_part):
    """Tests get_kanji_by_reading raises RetryableToolError for invalid tool-level input."""
    with pytest.raises(RetryableToolError) as exc_info: 
        await get_kanji_by_reading(invalid_input)
    assert expected_msg_part in str(exc_info.value) 
    if hasattr(exc_info.value, 'developer_message'):
        assert "Invalid input for get_kanji_by_reading" in exc_info.value.developer_message
    if hasattr(exc_info.value, 'additional_prompt_content'):
        assert "ask the user for a specific reading in kana" in exc_info.value.additional_prompt_content

@pytest.mark.asyncio
async def test_get_kanji_by_reading_client_returns_none(mocker):
    """Tests get_kanji_by_reading raises ToolExecutionError when client returns None."""
    reading_value = " ヌル " 
    cleaned_reading_value = "ヌル"
    mock_fetch = AsyncMock(return_value=None)
    mocker.patch(f"{PATCH_PREFIX}.fetch_kanji_by_reading", new=mock_fetch)

    with pytest.raises(ToolExecutionError) as exc_info:
        await get_kanji_by_reading(reading_value)
    
    expected_error_message = f"I couldn't find any kanji associated with the reading '{cleaned_reading_value}'. Please check the reading or try a different one."
    assert str(exc_info.value) == expected_error_message
    mock_fetch.assert_called_once_with(cleaned_reading_value)


# --- Tests for get_words_for_kanji ---

@pytest.mark.asyncio
async def test_get_words_for_kanji_success(mocker):
    """Tests get_words_for_kanji successfully returns JSON list of word entries."""
    kanji_char = "食"
    mock_word_entry_data1 = {"variants": [{"written": "食べる"}], "meanings": [{"glosses": ["to eat"]}]}
    mock_word_entry_data2 = {"variants": [{"written": "食物"}], "meanings": [{"glosses": ["food"]}]}
    
    mock_model_instance1 = create_mock_model(mocker, dump_data=mock_word_entry_data1)
    mock_model_instance2 = create_mock_model(mocker, dump_data=mock_word_entry_data2)
    
    mock_fetch_result = [mock_model_instance1, mock_model_instance2]
    mock_fetch = AsyncMock(return_value=mock_fetch_result)
    mocker.patch(f"{PATCH_PREFIX}.fetch_words_for_kanji", new=mock_fetch)

    result = await get_words_for_kanji(kanji_char)

    expected_json_list = [mock_word_entry_data1, mock_word_entry_data2]
    assert json.loads(result) == expected_json_list
    mock_fetch.assert_called_once_with(kanji_char)
    mock_model_instance1.model_dump.assert_called_once_with(exclude_none=True)
    mock_model_instance2.model_dump.assert_called_once_with(exclude_none=True)

@pytest.mark.asyncio
async def test_get_words_for_kanji_success_empty_list(mocker):
    """Tests get_words_for_kanji returns JSON for an empty list from client (valid success)."""
    kanji_char = "謎" # Using a valid single character for input validation
    mock_fetch_result = [] 
    mock_fetch = AsyncMock(return_value=mock_fetch_result)
    mocker.patch(f"{PATCH_PREFIX}.fetch_words_for_kanji", new=mock_fetch)
    
    result = await get_words_for_kanji(kanji_char) 
    assert json.loads(result) == []
    mock_fetch.assert_called_once_with("謎") 


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_input, expected_msg_part", [
    ("", "provide a single, valid Japanese kanji character"),
    ("AB", "provide a single, valid Japanese kanji character"),
    (None, "provide a single, valid Japanese kanji character"),
])
async def test_get_words_for_kanji_invalid_input(invalid_input, expected_msg_part):
    """Tests get_words_for_kanji raises RetryableToolError for invalid tool-level input."""
    with pytest.raises(RetryableToolError) as exc_info: 
        await get_words_for_kanji(invalid_input)
    assert expected_msg_part in str(exc_info.value) 
    if hasattr(exc_info.value, 'developer_message'):
        assert "Invalid input for get_words_for_kanji" in exc_info.value.developer_message
    if hasattr(exc_info.value, 'additional_prompt_content'):
        assert "ask the user for a single, specific kanji character to search words for" in exc_info.value.additional_prompt_content


@pytest.mark.asyncio
async def test_get_words_for_kanji_client_returns_none(mocker):
    """Tests get_words_for_kanji raises ToolExecutionError when client returns None."""
    kanji_char = "謎"
    mock_fetch = AsyncMock(return_value=None)
    mocker.patch(f"{PATCH_PREFIX}.fetch_words_for_kanji", new=mock_fetch)

    with pytest.raises(ToolExecutionError) as exc_info:
        await get_words_for_kanji(kanji_char)
    
    expected_error_message = f"I couldn't retrieve words for the kanji '{kanji_char}'. This might mean no words are listed for this kanji, or there was an issue fetching the data."
    assert str(exc_info.value) == expected_error_message
    mock_fetch.assert_called_once_with(kanji_char)
