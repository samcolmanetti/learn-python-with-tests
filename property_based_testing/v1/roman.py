"""Convert between integers and Roman numerals.

Roman numerals are written largest-to-smallest, with six subtractive pairs (IV, IX, XL, XC,
CD, CM). The trick that makes both directions short: list the value/symbol pairs *including*
the subtractive ones, in descending order, and greedily consume them.
"""

from __future__ import annotations

# Descending value/symbol pairs, subtractive forms included.
ROMAN_NUMERALS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def to_roman(number: int) -> str:
    if not 1 <= number <= 3999:
        raise ValueError("Roman numerals represent 1..3999")
    result = []
    for value, symbol in ROMAN_NUMERALS:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)
