from .gcd import gcd


def test_shared_factor():
    assert gcd(12, 18) == 6


def test_coprime():
    assert gcd(17, 5) == 1


def test_one_divides_the_other():
    assert gcd(48, 12) == 12


def test_zero_operand():
    assert gcd(0, 9) == 9
    assert gcd(9, 0) == 9
    assert gcd(0, 0) == 0


def test_negative_operands():
    assert gcd(-12, 18) == 6
    assert gcd(-12, -18) == 6
