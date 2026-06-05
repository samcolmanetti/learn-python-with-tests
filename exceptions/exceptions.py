"""Validate and parse user input by raising on bad data.

The chapter builds these up one failing test at a time: a ``parse_age`` that raises a custom
``ValidationError`` on anything that isn't a sensible age, and a ``parse_record`` that wraps the
parse in ``try``/``except``/``else``/``finally`` and records every attempt in an audit log.
"""

from __future__ import annotations

MAX_AGE = 150


class ValidationError(Exception):
    """Raised when input fails validation. ``field`` names which input was bad."""

    def __init__(self, message: str, field: str) -> None:
        super().__init__(message)
        self.field = field


def parse_age(raw: str) -> int:
    """Turn a raw age string into an ``int``, or raise ``ValidationError``.

    Rejects non-numeric strings, negatives, and anything above ``MAX_AGE``.
    """
    if not raw.isdigit():
        raise ValidationError(f"age must be digits, got {raw!r}", field="age")
    age = int(raw)
    if age > MAX_AGE:
        raise ValidationError(f"age {age} is above the maximum of {MAX_AGE}", field="age")
    return age


def parse_record(raw: str, audit: list[str]) -> int:
    """Parse one age, append an audit line whether it succeeds or fails, and re-raise on failure.

    ``else`` runs only when no exception was raised; ``finally`` runs no matter what.
    """
    try:
        age = parse_age(raw)
    except ValidationError as err:
        audit.append(f"rejected {raw!r}: {err.field}")
        raise
    else:
        audit.append(f"accepted {age}")
        return age
    finally:
        audit.append("done")
