import unittest

from mpmath.libmp import isprime


class TestIsPrime(unittest.TestCase):
    def test_small_numbers(self):
        self.assertFalse(isprime(0))
        self.assertTrue(isprime(2))
        self.assertTrue(isprime(3))

    def test_primes(self):
        self.assertTrue(isprime(5))
        self.assertTrue(isprime(13))
        self.assertTrue(isprime(97))

    def test_non_primes(self):
        self.assertFalse(isprime(4))
        self.assertFalse(isprime(9))
        self.assertFalse(isprime(100))

    def test_large_prime(self):
        self.assertTrue(isprime(7919))  # простое число

    def test_large_composite(self):
        self.assertFalse(isprime(8000))

if __name__ == '__main__':
    unittest.main()
