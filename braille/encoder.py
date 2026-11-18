"""Basic uncontracted English-to-Braille conversion.

This is a deliberately limited prototype, not a complete Unified English Braille
(UEB) transcriber.
"""
from __future__ import annotations

LETTER_CELLS = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑",
    "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕",
    "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",
}
NUMBER_CELLS = {
    "1": "⠁", "2": "⠃", "3": "⠉", "4": "⠙", "5": "⠑",
    "6": "⠋", "7": "⠛", "8": "⠓", "9": "⠊", "0": "⠚",
}
PUNCTUATION_CELLS = {
    ",": "⠂", ";": "⠆", ":": "⠒", ".": "⠲", "?": "⠦",
    "!": "⠖", "'": "⠄", "-": "⠤", "(": "⠐⠣", ")": "⠐⠜",
}
CAPITAL_INDICATOR = "⠠"
NUMBER_INDICATOR = "⠼"
LETTER_INDICATOR = "⠰"
BLANK_CELL = "⠀"


class UnsupportedCharacterError(ValueError):
    """Raised when the selected basic Braille mapping cannot encode a character."""


def text_to_braille(text: str) -> str:
    """Convert basic English text to Braille Unicode cells."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    output: list[str] = []
    numeric_mode = False
    for index, character in enumerate(text):
        if character in NUMBER_CELLS:
            if not numeric_mode:
                output.append(NUMBER_INDICATOR)
                numeric_mode = True
            output.append(NUMBER_CELLS[character])
            continue
        if character.isalpha() and character.lower() in LETTER_CELLS:
            letter = character.lower()
            if numeric_mode and letter in "abcdefghij":
                output.append(LETTER_INDICATOR)
            numeric_mode = False
            if character.isupper():
                output.append(CAPITAL_INDICATOR)
            output.append(LETTER_CELLS[letter])
            continue
        if character in PUNCTUATION_CELLS:
            output.append(PUNCTUATION_CELLS[character])
            if character in "-!?;()'":
                numeric_mode = False
            continue
        if character == " ":
            output.append(BLANK_CELL)
            numeric_mode = False
            continue
        if character in "\r\n\t":
            output.append("\n" if character in "\r\n" else BLANK_CELL * 4)
            numeric_mode = False
            continue
        raise UnsupportedCharacterError(
            f"Unsupported character {character!r} at position {index + 1}. "
            "Supported: basic English letters, digits, common punctuation, spaces and line breaks."
        )
    return "".join(output)
