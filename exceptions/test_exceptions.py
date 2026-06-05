import pytest

from .exceptions import ValidationError, parse_age, parse_record


def test_parses_a_valid_age():
    assert parse_age("42") == 42


def test_rejects_non_numeric_age():
    with pytest.raises(ValidationError):
        parse_age("forty")


def test_rejects_age_above_maximum():
    with pytest.raises(ValidationError, match="above the maximum"):
        parse_age("200")


def test_validation_error_carries_the_field():
    with pytest.raises(ValidationError) as exc_info:
        parse_age("forty")
    assert exc_info.value.field == "age"


def test_record_logs_acceptance_then_done():
    audit: list[str] = []
    assert parse_record("30", audit) == 30
    assert audit == ["accepted 30", "done"]


def test_record_logs_rejection_then_done_and_reraises():
    audit: list[str] = []
    with pytest.raises(ValidationError):
        parse_record("nope", audit)
    assert audit == ["rejected 'nope': age", "done"]
