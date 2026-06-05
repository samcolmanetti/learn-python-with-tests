from .number_of_1_bits import hamming_weight


def test_zero_has_no_set_bits():
    assert hamming_weight(0) == 0


def test_one_set_bit():
    assert hamming_weight(8) == 1


def test_all_set_bits():
    assert hamming_weight(0b1111) == 4


def test_mixed_bits():
    assert hamming_weight(0b1011) == 3


def test_large_value():
    assert hamming_weight(0xFFFFFFFF) == 32
