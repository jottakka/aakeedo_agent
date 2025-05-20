import pytest

# Module to be tested - ensure these paths match your project structure
from arcade_aakeedo_kanji.http_clients.kanji_api_http_client import (
    fetch_kanji_details,
    fetch_joyo_kanji_list,
    fetch_kanji_list,
    fetch_kanji_by_reading,
    fetch_words_for_kanji,
)
from arcade_aakeedo_kanji.models.kanji_api_models import (
    KanjiDetailModel,
    KanjiReading,
    WordEntry,
)

# --- Test Input Data for Live API Calls ---
KANJI_FOR_DETAILS = "学"  # "study" - common, stable, has grade & JLPT
KANJI_FOR_WORDS = "食"    # "eat" - has common words
KANJI_FOR_FEW_WORDS = "璽" # "emperor's seal" - likely few/no common dictionary words, good for testing empty list success

KANJI_LIST_NAME_GRADE_1 = "grade-1"
KANJI_LIST_NAME_JLPT_N5 = "jlpt-5" # jlpt-N5, N4 etc. are valid per new API docs

READING_FOR_KANJI = "しょく" # Reading for "食"
READING_FOR_KANJI_KAI = "かい"   # Common reading for 会, 海 etc.


# --- Integration Tests: Success Cases Only (Live API Calls) ---

@pytest.mark.asyncio
async def test_fetch_kanji_details_success():
    """
    Tests fetching details for a known Kanji ("学") against the live KanjiAPI.
    Verifies that a KanjiDetailModel instance is returned with expected basic data.
    """
    result = await fetch_kanji_details(KANJI_FOR_DETAILS)

    assert isinstance(result, KanjiDetailModel), f"Result for '{KANJI_FOR_DETAILS}' should be a KanjiDetailModel instance."
    assert result.kanji == KANJI_FOR_DETAILS
    assert isinstance(result.stroke_count, int) and result.stroke_count > 0
    assert isinstance(result.meanings, list) and len(result.meanings) > 0
    assert result.unicode is not None
    assert result.grade is not None, f"Kanji '{KANJI_FOR_DETAILS}' should have a grade."
    assert result.jlpt is not None, f"Kanji '{KANJI_FOR_DETAILS}' should have a JLPT level."
    assert any("study" in m.lower() or "learn" in m.lower() for m in result.meanings), "Meanings should relate to 'study' or 'learn'."

@pytest.mark.asyncio
async def test_fetch_joyo_kanji_list_success():
    """
    Tests fetching the complete list of Jōyō kanji against the live KanjiAPI.
    Verifies that a non-empty list of single-character strings is returned.
    """
    result = await fetch_joyo_kanji_list()

    assert isinstance(result, list), "Jōyō kanji result should be a list."
    assert len(result) > 2000, f"Jōyō list should contain over 2000 kanji, got {len(result)}."
    assert all(isinstance(kanji, str) for kanji in result), "All items in the Jōyō list should be strings."
    assert all(len(kanji) == 1 for kanji in result if kanji), "All kanji strings in the Jōyō list should be single characters."
    assert "学" in result, "Common Jōyō kanji '学' should be in the list."

@pytest.mark.asyncio
async def test_fetch_kanji_list_success_grade1():
    """
    Tests fetching a specific list of kanji (Grade 1) against the live KanjiAPI.
    Verifies a non-empty list of single-character strings is returned.
    """
    result = await fetch_kanji_list(KANJI_LIST_NAME_GRADE_1)

    assert isinstance(result, list), f"Result for kanji list '{KANJI_LIST_NAME_GRADE_1}' should be a list."
    assert len(result) > 0, f"Kanji list '{KANJI_LIST_NAME_GRADE_1}' should not be empty."
    assert all(isinstance(kanji, str) for kanji in result), f"All items in kanji list '{KANJI_LIST_NAME_GRADE_1}' should be strings."
    assert all(len(kanji) == 1 for kanji in result if kanji), f"All kanji in list '{KANJI_LIST_NAME_GRADE_1}' should be single characters."
    assert "一" in result, "Kanji '一' should be in the Grade 1 list." # Grade 1 contains "一"

@pytest.mark.asyncio
async def test_fetch_words_for_kanji_success_with_words():
    """
    Tests fetching dictionary word entries for a common kanji ("食") against the live KanjiAPI.
    Verifies a non-empty list of WordEntry objects is returned.
    """
    result = await fetch_words_for_kanji(KANJI_FOR_WORDS)

    assert isinstance(result, list), f"Result for words of kanji '{KANJI_FOR_WORDS}' should be a list."
    assert len(result) > 0, f"Word list for '{KANJI_FOR_WORDS}' should not be empty."
    assert all(isinstance(entry, WordEntry) for entry in result), f"All items for words of kanji '{KANJI_FOR_WORDS}' should be WordEntry instances."
    
    # Check for a common word "食べる" (taberu)
    found_taberu = False
    for entry in result:
        for variant in entry.variants:
            if variant.written == "食べる" and variant.pronounced == "たべる":
                found_taberu = True
                break
        if found_taberu:
            break
    assert found_taberu, f"Expected word '食べる' (たべる) not found for kanji '{KANJI_FOR_WORDS}'."

@pytest.mark.asyncio
async def test_fetch_words_for_kanji_success_empty_or_few_words():
    """
    Tests fetching dictionary word entries for a less common kanji ("璽") against the live KanjiAPI.
    Verifies a list (which might be empty) of WordEntry objects is returned.
    An empty list is a valid successful response.
    """
    result = await fetch_words_for_kanji(KANJI_FOR_FEW_WORDS)

    assert isinstance(result, list), f"Result for words of kanji '{KANJI_FOR_FEW_WORDS}' should be a list (can be empty)."
    if result: # If the list is not empty, check contents
        assert all(isinstance(entry, WordEntry) for entry in result), f"All items for words of kanji '{KANJI_FOR_FEW_WORDS}' should be WordEntry instances."
        
@pytest.mark.asyncio
async def test_fetch_kanji_by_reading_success():
    """
    Tests fetching kanji associated with a specific reading ("しょく") against the live KanjiAPI.
    Verifies a KanjiReading object is returned with expected data.
    """
    result = await fetch_kanji_by_reading(READING_FOR_KANJI)

    assert isinstance(result, KanjiReading), f"Result for reading 'たべる' should be a KanjiReading instance."
