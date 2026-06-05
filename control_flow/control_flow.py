"""Two small functions built test-first to exercise Python's control flow.

``fizzbuzz`` walks ``if``/``elif``/``else``, a ``for`` loop, and the modulo test. ``grade_classifier``
adds boundary-driven branching, ``while`` with ``break``/``continue``, truthiness, and the ternary.
"""

from __future__ import annotations


def fizzbuzz(n: int) -> list[str]:
    """Return the FizzBuzz line for each number from 1 to ``n`` inclusive.

    Multiples of 15 are ``"FizzBuzz"``, of 3 ``"Fizz"``, of 5 ``"Buzz"``, otherwise the number as a
    string. The 15 case is checked first because it's the most specific.
    """
    lines = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            lines.append("FizzBuzz")
        elif i % 3 == 0:
            lines.append("Fizz")
        elif i % 5 == 0:
            lines.append("Buzz")
        else:
            lines.append(str(i))
    return lines


def grade_classifier(score: int) -> str:
    """Map a 0-to-100 ``score`` to a letter grade, raising on out-of-range input.

    The bands are A (90+), B (80-89), C (70-79), D (60-69), F below 60. Checking from the top down
    means each ``elif`` only has to test the lower bound of its band.
    """
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def first_passing(scores: list[int]) -> str:
    """Return the grade of the first passing score (60+), or ``"none"`` if there isn't one.

    This one's here to show ``while``, ``continue`` (skip the empty-ish junk), and ``break`` (stop at
    the first hit). A real codebase would write it with ``for``, but the loop keywords are the point.
    """
    i = 0
    answer = "none"
    while i < len(scores):
        score = scores[i]
        i += 1
        if not (0 <= score <= 100):
            continue
        grade = grade_classifier(score)
        if grade != "F":
            answer = grade
            break
    return answer
