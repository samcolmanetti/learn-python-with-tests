from .iteration import repeat


def test_repeats_a_character_five_times():
    assert repeat("a") == "aaaaa"
