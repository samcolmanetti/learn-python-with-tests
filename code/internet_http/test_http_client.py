from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from http_client import fetch_json, get_user_name


class FakeResponse:
    """Stand-in for what ``urlopen`` returns: a context manager with ``.read()`` -> bytes."""

    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def read(self) -> bytes:
        return self.body


def fake_opener(body: bytes):
    """Build a fake opener that records the URL it was called with and returns ``body``."""
    calls: list[str] = []

    def opener(url: str) -> FakeResponse:
        calls.append(url)
        return FakeResponse(body)

    opener.calls = calls  # type: ignore[attr-defined]
    return opener


def test_fetch_json_parses_object():
    opener = fake_opener(b'{"id": 1, "name": "Ada"}')
    assert fetch_json("http://example.test/u/1", opener=opener) == {"id": 1, "name": "Ada"}


def test_fetch_json_parses_list():
    opener = fake_opener(b"[1, 2, 3]")
    assert fetch_json("http://example.test/nums", opener=opener) == [1, 2, 3]


def test_fetch_json_passes_the_url_through():
    opener = fake_opener(b"{}")
    fetch_json("http://example.test/thing", opener=opener)
    assert opener.calls == ["http://example.test/thing"]


def test_fetch_json_raises_on_invalid_json():
    opener = fake_opener(b"not json at all")
    with pytest.raises(json.JSONDecodeError):
        fetch_json("http://example.test/bad", opener=opener)


def test_get_user_name_extracts_the_field():
    opener = fake_opener(b'{"id": 7, "name": "Grace"}')
    assert get_user_name("http://example.test/u/7", opener=opener) == "Grace"


def test_fetch_json_with_patched_urlopen():
    # Same idea as the fake opener, but using unittest.mock to replace the default urlopen.
    with patch("http_client.urlopen") as mock_urlopen:
        mock_urlopen.return_value = FakeResponse(b'{"ok": true}')
        assert fetch_json("http://example.test/ok") == {"ok": True}
        mock_urlopen.assert_called_once_with("http://example.test/ok")
