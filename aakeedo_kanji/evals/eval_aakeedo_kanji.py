from arcade.sdk import ToolCatalog
from arcade.sdk.eval import (EvalRubric, EvalSuite, ExpectedToolCall,
                             SimilarityCritic, tool_eval)

from arcade_aakeedo_kanji.tools import kanji_api_tools
from arcade_aakeedo_kanji.tools.kanji_api_tools import (
    get_kanji_by_reading, get_kanji_details, get_kanji_list_by_category,
    get_words_for_kanji, list_joyo_kanji)

default_rubric = EvalRubric(
    fail_threshold=0.80,
    warn_threshold=0.90,
)

kanji_tool_catalog = ToolCatalog()
kanji_tool_catalog.add_module(kanji_api_tools)


# --- Evaluation Suite Definition ---
@tool_eval()
def kanji_tools_evaluation_suite() -> EvalSuite:
    """
    Defines the evaluation suite for the Kanji API tools.
    """
    suite = EvalSuite(
        name="Kanji Tools Evaluation Suite",
        system_message=(
            "You are a helpful AI assistant with access to a comprehensive set of Kanji tools. "
            "Use these tools to answer user questions about Japanese Kanji characters, lists, "
            "readings, and words. Be precise with Kanji characters and readings."
        ),
        catalog=kanji_tool_catalog,
        rubric=default_rubric,
    )

    suite.add_case(
        name="Get details for a specific Kanji (e.g., '水' - water)",
        user_message="Can you tell me about the kanji for water? I think it looks like 水.",
        expected_tool_calls=[ExpectedToolCall(func=get_kanji_details, args={"kanji_char": "水"})],
    )

    # --- Test Case 2: List Jōyō Kanji ---
    suite.add_case(
        name="List all Jōyō Kanji",
        user_message="Please show me the list of all Jōyō kanji.",
        expected_tool_calls=[
            ExpectedToolCall(func=list_joyo_kanji, args={})  # No arguments for this tool
        ],
    )

    # --- Test Case 3: Get Kanji List by Category (Grade) ---
    suite.add_case(
        name="Get Kanji list by category (Grade 1)",
        user_message="Which kanji are taught in the first grade of elementary school?",
        expected_tool_calls=[
            ExpectedToolCall(func=get_kanji_list_by_category, args={"list_name": "grade-1"})
        ],
        critics=[
            SimilarityCritic(
                critic_field="list_name", weight=0.7
            ),  # Allows for variations like "1st grade" vs "grade-1"
        ],
    )

    # --- Test Case 4: Get Kanji List by Category (JLPT Level) ---
    suite.add_case(
        name="Get Kanji list by category (JLPT N4)",
        user_message="I'm studying for JLPT N4, can you list the N4 kanji for me?",
        expected_tool_calls=[
            ExpectedToolCall(func=get_kanji_list_by_category, args={"list_name": "jlpt-n4"})
        ],
        critics=[
            SimilarityCritic(critic_field="list_name", weight=0.7),
        ],
    )

    # --- Test Case 5: Get Kanji by Reading ---
    suite.add_case(
        name="Get Kanji by a specific reading (e.g., 'かわ' - kawa)",
        user_message="What kanji can be read as 'kawa'?",
        expected_tool_calls=[
            ExpectedToolCall(func=get_kanji_by_reading, args={"reading_value": "かわ"})
        ],
    )

    # --- Test Case 6: Get Kanji by another reading (On'yomi example) ---
    suite.add_case(
        name="Get Kanji by a specific On'yomi reading (e.g., 'ガク' - gaku)",
        user_message="Find kanji with the on'yomi reading 'gaku', like in 'student'.",
        expected_tool_calls=[
            ExpectedToolCall(
                func=get_kanji_by_reading, args={"reading_value": "ガク"}
            )  # Katakana for On'yomi
        ],
    )

    # --- Test Case 7: Get Words for a specific Kanji ---
    suite.add_case(
        name="Get words using a specific Kanji (e.g., '道' - road/way)",
        user_message="Show me some vocabulary words that use the kanji for 'road', which is 道.",
        expected_tool_calls=[ExpectedToolCall(func=get_words_for_kanji, args={"kanji_char": "道"})],
    )

    return suite
