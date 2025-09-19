import pytest
from mpmath.libmp import isprime

@pytest.mark.parametrize("n,expected", [
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (9, False),
    (13, True),
    (97, True),
    (100, False),
    (7919, True),
    (8000, False),
])
def test_is_prime(n, expected):
    assert isprime(n) == expected
