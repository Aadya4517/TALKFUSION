import unittest
from braille.encoder import UnsupportedCharacterError, text_to_braille


class TestTextToBraille(unittest.TestCase):
    def test_lowercase_alphabet(self):
        self.assertEqual(text_to_braille("abcdefghijklmnopqrstuvwxyz"),
                         "⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚⠅⠇⠍⠝⠕⠏⠟⠗⠎⠞⠥⠧⠺⠭⠽⠵")

    def test_capital_letters(self):
        self.assertEqual(text_to_braille("AbZ"), "⠠⠁⠃⠠⠵")

    def test_number_sequence(self):
        self.assertEqual(text_to_braille("204"), "⠼⠃⠚⠙")

    def test_letter_after_number_that_could_be_a_digit(self):
        self.assertEqual(text_to_braille("2b"), "⠼⠃⠰⠃")

    def test_basic_punctuation_and_space(self):
        self.assertEqual(text_to_braille("Hi!"), "⠠⠓⠊⠖")
        self.assertEqual(text_to_braille("a b"), "⠁⠀⠃")

    def test_unsupported_character_is_reported(self):
        with self.assertRaises(UnsupportedCharacterError):
            text_to_braille("café")

    def test_non_string_input_is_rejected(self):
        with self.assertRaises(TypeError):
            text_to_braille(None)

    def test_empty_input(self):
        self.assertEqual(text_to_braille(""), "")


if __name__ == "__main__":
    unittest.main()
