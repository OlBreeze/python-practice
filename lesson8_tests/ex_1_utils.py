import unittest
from example_1 import factorial

class TestFactorial(unittest.TestCase):
    def test_factorial_one(self):
        self.assertEqual(factorial(0), 1)

    def test_factorial_positive(self):
        self.assertEqual(factorial(5), 120)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-3)

if __name__ == '__main__':
    unittest.main()