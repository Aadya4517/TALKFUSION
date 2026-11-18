"""Braille conversion and optional device output."""
from .encoder import UnsupportedCharacterError, text_to_braille
__all__ = ["UnsupportedCharacterError", "text_to_braille"]
