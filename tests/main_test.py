import sys
sys.path.insert(0, r"C:/Users/Pascal/Desktop/Skat")

import main
import unittest


class Test_create_players(unittest.TestCase):

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            main.create_players("hello")
    
    def test_wrong_value_amount(self):
        with self.assertRaises(ValueError):
            main.create_players(["hello", "world"])

    def test_wrong_value_type(self):
        with self.assertRaises(TypeError):
            main.create_players(["hi", "test", {"1":"2"}])

    def test_none(self):
        self.assertEqual(main.create_players()[0]["name"], "Player 1")

    def test_names(self):
        self.assertEqual(main.create_players(["1", "2", "3"])[1]["name"], "2")


class Test_create_settings(unittest.TestCase):

    def test_wrong_language_type(self):
        with self.assertRaises(TypeError):
            main.create_settings(5)
    
    def test_wrong_language_value(self):
        with self.assertRaises(ValueError):
            main.create_settings('it')
    
    def test_right_values(self):
        self.assertDictEqual(main.create_settings('de')["suit_dict"], {"Kr": 12, "P": 11, "H": 10, "Ka": 9})

if __name__ == "__main__":
    unittest.main()
