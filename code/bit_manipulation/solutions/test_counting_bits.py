from .counting_bits import count_bits


def test_zero():
    assert count_bits(0) == [0]


def test_up_to_two():
    assert count_bits(2) == [0, 1, 1]


def test_up_to_five():
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]


def test_length_matches_n_plus_one():
    assert len(count_bits(10)) == 11


def test_matches_naive_count():
    expected = [bin(i).count("1") for i in range(16)]
    assert count_bits(15) == expected
