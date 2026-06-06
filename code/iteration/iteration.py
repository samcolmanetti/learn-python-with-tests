def repeat(character, count):
    # In Python, `str * int` repeats the string. The explicit loop in v1/v2 was a good
    # starting point, but with passing tests as a safety net we can refactor to the
    # idiomatic one-liner with confidence.
    return character * count
