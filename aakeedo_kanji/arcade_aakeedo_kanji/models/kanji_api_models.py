from pydantic import BaseModel, Field


class KanjiDetailModel(BaseModel):
    """
    Represents detailed information about a Kanji character.
    Updated with all fields from the provided schema.
    """

    kanji: str = Field(..., description="The kanji character itself (e.g., '蜜').")
    grade: int | None = Field(
        None,
        description="The official grade of the kanji (1-6 for Kyōiku kanji, "
        "8 for other Jōyō kanji, 9 for Jinmeiyō kanji). Null if not applicable.",
    )
    stroke_count: int = Field(
        ..., description="The total number of strokes required to write the kanji."
    )
    meanings: list[str] = Field(
        ..., description="A list of English meanings associated with the kanji."
    )
    kun_readings: list[str] = Field(
        default_factory=list,
        description="A list of Kun'yomi (native Japanese) readings for the kanji, typically in hiragana.",
    )
    on_readings: list[str] = Field(
        default_factory=list,
        description="A list of On'yomi (Sino-Japanese) readings for the kanji, typically in katakana.",
    )
    name_readings: list[str] = Field(
        default_factory=list,
        description="A list of special readings (nanori) used primarily in names.",
    )
    jlpt: int | None = Field(
        None,
        description="The former Japanese Language Proficiency Test (JLPT) level for the kanji (levels 1-4). "
        "Null if the kanji is not part of such a JLPT level listing.",
    )
    unicode: str = Field(
        ..., description="The Unicode codepoint for the kanji character (e.g., '871c')."
    )
    heisig_en: str | None = Field(
        None,
        description="The English keyword for the kanji according to James Heisig's 'Remembering the Kanji' method. "
        "Null if not applicable.",
    )
    freq_mainichi_shinbun: int | None = Field(  # New field
        None,
        alias="freq_mainichi_shinbun",
        description="A relative frequency ranking from an analysis of Mainichi Shinbun newspaper articles. "
        "The 2,501 most-used characters received a ranking. Null if not ranked.",
    )
    unihan_cjk_compatibility_variant: str | None = Field(  # New field
        None,
        alias="unihan_cjk_compatibility_variant",
        description="If the kanji is a compatibility variant character, this field shows the unified version. "
        "Otherwise, null or undefined.",
    )
    notes: list[str] = Field(  # New field
        default_factory=list, description="Any notes about the kanji or its fields."
    )


class KanjiReading(BaseModel):
    """
    Represents kanji associated with a specific reading.
    Corresponds to the response from GET /v1/reading/{reading}.
    """

    reading: str = Field(..., description="The reading itself (e.g., 'みつ', 'ニチ').")
    main_kanji: list[str] = Field(
        ..., description="A list of kanji characters that commonly use this reading."
    )
    name_kanji: list[str] = Field(
        ...,
        description="A list of kanji characters that use this reading primarily or exclusively in names.",
    )


class Meaning(BaseModel):
    """
    Represents a distinct meaning of a word, including its English glosses.
    """

    glosses: list[str] = Field(
        ...,
        description="A list of English equivalent terms or explanations for this particular meaning.",
    )


class Variant(BaseModel):
    """
    Represents a written and pronounced variation of a word entry.
    """

    written: str = Field(
        ..., description="The written form of the variant (e.g., '食べる', '喰べる')."
    )
    pronounced: str | None = Field(  # Marked Optional for robustness, though schema implies string
        None, description="The pronounced form of the variant, typically in kana (e.g., 'たべる')."
    )
    priorities: list[str] = Field(
        default_factory=list,
        description="A list of strings designating frequency or usage lists in which this variant appears (e.g., 'ichi1', 'news1').",
    )


class WordEntry(BaseModel):
    """
    Represents a dictionary entry for a word, typically associated with a kanji.
    Corresponds to an item in the list from GET /v1/words/{character}.
    """

    meanings: list[Meaning] = Field(
        ..., description="A list of distinct meanings that the word entry has."
    )
    variants: list[Variant] = Field(
        ..., description="A list of written and pronounced variations for the word entry."
    )
