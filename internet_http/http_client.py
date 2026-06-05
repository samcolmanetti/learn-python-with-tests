"""Fetching and parsing JSON over HTTP with only the standard library.

The real call goes out with ``urllib.request.urlopen``. The trick that keeps this testable is
that ``fetch_json`` takes the *opener* as a parameter. In production you let it default to the
real ``urlopen``; in a test you pass a fake that returns canned bytes, so the test never touches
the network. That parameter is *dependency injection*, and it's the whole lesson of this chapter.
"""

from __future__ import annotations

import json
from typing import Any, Callable
from urllib.request import urlopen


def fetch_json(url: str, opener: Callable[[str], Any] | None = None) -> Any:
    """Fetch ``url`` and parse the response body as JSON.

    ``opener`` is any callable that takes a URL and returns an object supporting the context
    manager protocol with a ``.read()`` returning ``bytes`` (exactly the shape of
    ``urllib.request.urlopen``). When it's left as ``None`` we look up ``urlopen`` at call time,
    so real callers write ``fetch_json(url)`` and tests write ``fetch_json(url, opener=fake)``
    (or patch the module-level ``urlopen``).
    """
    if opener is None:
        opener = urlopen
    with opener(url) as response:
        body = response.read()
    return json.loads(body)


def get_user_name(url: str, opener: Callable[[str], Any] | None = None) -> str:
    """Fetch a user payload and pull out its ``"name"`` field.

    A tiny example of building on ``fetch_json``: one network call, then a pure transformation of
    the decoded data. The transformation is trivial to test because the fetch is injectable.
    """
    data = fetch_json(url, opener=opener)
    return data["name"]
