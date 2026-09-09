import unittest
from p5_Majcherek_Joseph import caesar_cipher, caesar_decipher, letter_frequency

class TestCaesarFunctions(unittest.TestCase):

    def test_caesar_cipher(self):
        self.assertEqual(
            caesar_cipher("Hello World!", 3),
            "Khoor Zruog!"
        )

    def test_caesar_cipher_wraps_letters(self):
        self.assertEqual(caesar_cipher("Zz", 1), "Aa")

    def test_caesar_decipher(self):
        self.assertEqual(
            caesar_decipher("Khoor Zruog!", 3),
            "Hello World!"
        )

    def test_letter_frequency(self):
        self.assertEqual(
            letter_frequency("Hello World!"),
            {
                "h": 1,
                "e": 1,
                "l": 3,
                "o": 2,
                "w": 1,
                "r": 1,
                "d": 1,
            }
        )

    def test_letter_frequency_ignores_spaces_and_punctuation(self):
        self.assertEqual(
            letter_frequency("A, a! B?"),
            {"a": 2, "b": 1}
        )

if __name__ == "__main__":
    unittest.main()