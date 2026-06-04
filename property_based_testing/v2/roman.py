"""Convert between integers and Roman numerals — now both directions.

See v1 for the value/symbol table rationale. ``from_roman`` greedily matches the same pairs
from the front of the string, which is the natural inverse of ``to_roman``.
"""

from __future__ import annotations

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


def from_roman(numeral: str) -> int:
    total = 0
    index = 0
    for value, symbol in ROMAN_NUMERALS:
        while numeral[index : index + len(symbol)] == symbol:
            total += value
            index += len(symbol)
    if index != len(numeral):
        raise ValueError(f"not a valid Roman numeral: {numeral!r}")
    return total
