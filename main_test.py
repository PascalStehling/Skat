import main
import unittest

class TestHelloWorld(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(main.hello_world(), "Hello World")

if __name__ == "__main__":
    unittest.main()
