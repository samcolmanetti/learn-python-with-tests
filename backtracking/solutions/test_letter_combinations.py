from .letter_combinations import letter_combinations


def test_empty_returns_empty_list():
    assert letter_combinations("") == []


def test_single_digit():
    assert letter_combinations("2") == ["a", "b", "c"]


def test_two_digits():
    expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert letter_combinations("23") == expected


def test_digit_with_four_letters():
    assert letter_combinations("7") == ["p", "q", "r", "s"]


def test_count_is_product_of_branching():
    # "79" has 4 letters then 4 letters, so 4 * 4 = 16 combinations.
    assert len(letter_combinations("79")) == 16
