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
        test_dict = {0:{"name": "Player 1","num": 0,"cards": [],"points": 0,"position": 0},
                    1: {"name": "Player 2","num": 1,"cards": [],"points": 0,"position": 1},
                    2: {"name": "Player 3","num": 2,"cards": [],"points": 0,"position": 2}}
        self.assertDictEqual(main.create_players(), test_dict)

    def test_names(self):
        test_dict = {0:{"name": "1","num": 0,"cards": [],"points": 0,"position": 0},
                    1: {"name": "2","num": 1,"cards": [],"points": 0,"position": 1},
                    2: {"name": "3","num": 2,"cards": [],"points": 0,"position": 2}}
        self.assertDictEqual(main.create_players(["1", "2", "3"]), test_dict)


class Test_create_settings(unittest.TestCase):

    def test_wrong_language_type(self):
        with self.assertRaises(TypeError):
            main.create_settings(5)
    
    def test_wrong_language_value(self):
        with self.assertRaises(ValueError):
            main.create_settings('it')
    
    def test_right_values(self):
        test_dict = {"value_dict": {'7': 0, '8': 0, '9': 0, '10': 10, 'B': 2, 'D': 3, 'K': 4, 'A': 11}, "suit_dict": {"Kr": 12, "P": 11, "H": 10, "Ka": 9}}
        self.assertDictEqual(main.create_settings('de'), test_dict)

if __name__ == "__main__":
    unittest.main()
