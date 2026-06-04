from .iteration import repeat


def test_repeats_a_character_a_given_number_of_times():
    assert repeat("a", 5) == "aaaaa"


def test_repeats_zero_times_is_empty():
    assert repeat("a", 0) == ""
