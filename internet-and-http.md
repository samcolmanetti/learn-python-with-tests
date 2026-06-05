# Internet and HTTP calls

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/internet_http)**

We want to call an HTTP endpoint that returns JSON and hand back the parsed data, using nothing
but the standard library. The catch is the one every networking chapter trips on: a test that
actually hits the network is slow, flaky, and offline-hostile. So the real lesson here isn't
`urllib`, it's how to write the function so the network is something you can swap out.

## Write the test first

Here's the function we want. `fetch_json(url)` makes a GET request and returns the decoded JSON.
In production the request goes out through `urllib.request.urlopen`. But if our test calls the
real `urlopen`, it talks to a real server, and now our suite depends on the internet being up and
some endpoint behaving. That's not a test, that's a weather report.

The fix is to let the caller pass in the thing that opens the URL. We give `fetch_json` an
`opener` parameter that defaults to the real `urlopen`. Real callers ignore it; tests pass a fake.

So before we write a line of the implementation, we write the fake. `urlopen` returns an object
you use as a context manager, and you call `.read()` on it to get the response body as `bytes`.
We only need to imitate that shape.

```python
from __future__ import annotations

from .http_client import fetch_json


class FakeResponse:
    """Stand-in for what urlopen returns: a context manager with .read() -> bytes."""

    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def read(self) -> bytes:
        return self.body


def fake_opener(body: bytes):
    def opener(url: str) -> FakeResponse:
        return FakeResponse(body)

    return opener


def test_fetch_json_parses_object():
    opener = fake_opener(b'{"id": 1, "name": "Ada"}')
    assert fetch_json("http://example.test/u/1", opener=opener) == {"id": 1, "name": "Ada"}
```

The body is `bytes` (note the `b` prefix), because that's what a socket gives you. The test never
touches a network card. It hands `fetch_json` a canned response and checks that we parsed it.

## Try to run the test

`http_client.py` doesn't define `fetch_json` yet, so the import is the first thing to break:

```
ImportError: cannot import name 'fetch_json' from 'internet_http.http_client'
```

Nothing to import means nothing to test. The error is pointing us at the first thing to write.

## Write the minimal amount of code for the test to run and check the failing test output

Give `fetch_json` a body that returns `None`. It runs, it takes the right arguments, and it
returns the wrong thing on purpose. I know hard-coding `None` feels pointless, but we want to see
the test fail on the *value*, which proves the test is actually checking what we think it is.

```python
from __future__ import annotations


def fetch_json(url, opener=None):
    return None
```

Run `uv run pytest`:

```
    def test_fetch_json_parses_object():
        opener = fake_opener(b'{"id": 1, "name": "Ada"}')
>       assert fetch_json("http://example.test/u/1", opener=opener) == {"id": 1, "name": "Ada"}
E       AssertionError: assert None == {'id': 1, 'name': 'Ada'}
E        +  where None = fetch_json('http://example.test/u/1', opener=<function fake_opener.<locals>.opener at 0x10891baf0>)
```

The test runs and fails on the value, not on a missing name. That's the signal we wanted before
writing anything real.

## Write enough code to make it pass

Now the real thing. Open the URL through `opener`, read the bytes, parse them with `json.loads`.
`json.loads` happily accepts `bytes`, so there's no decode step to write.

```python
from __future__ import annotations

import json
from typing import Any, Callable
from urllib.request import urlopen


def fetch_json(url: str, opener: Callable[[str], Any] | None = None) -> Any:
    if opener is None:
        opener = urlopen
    with opener(url) as response:
        body = response.read()
    return json.loads(body)
```

Run the tests again and they're green.

The `opener` parameter is the whole trick. We import the real `urlopen` and fall back to it when
nobody passes anything, so a real caller just writes `fetch_json("https://api.github.com/users/torvalds")`
and the request goes out for real. Passing a function in as an argument so you can swap it in a
test is called *dependency injection*. The dependency here is "the thing that talks to the
network", and we inject it instead of reaching for it directly.

### Why default to None instead of urlopen?

You might expect the signature to read `opener=urlopen` directly, and that does work for the fake
we pass by hand. But a default argument is evaluated **once, when the function is defined**, and
bound forever. If a test later tries to patch the module's `urlopen`, the default still points at
the original. Resolving `urlopen` inside the body with `if opener is None` means we look it up
fresh on every call, which is what makes patching work. We'll lean on that in a moment.

## Refactor

The function is five lines and already does one job, so there's nothing to tidy in the code. What's
worth tidying is the test file: one happy-path test doesn't pin much down. Let me add the cases
that actually earn their keep.

```python
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
```

`test_fetch_json_parses_list` proves we hand back whatever JSON shape comes down the wire, not
just objects. `test_fetch_json_raises_on_invalid_json` pins the failure mode: bad bytes raise
`json.JSONDecodeError`, and we don't swallow it.

The interesting one is `test_fetch_json_passes_the_url_through`. We want to assert that the URL we
were given is the URL we opened. A fake that only returns a body can't tell us that, so we upgrade
`fake_opener` to record its calls:

```python
def fake_opener(body: bytes):
    calls: list[str] = []

    def opener(url: str) -> FakeResponse:
        calls.append(url)
        return FakeResponse(body)

    opener.calls = calls
    return opener
```

This is the second thing a fake buys you: not just canned answers, but a record of how it was
called. We can now assert on *inputs* (which URL did you request?), not only outputs. Add `import
json` and `import pytest` at the top, run `uv run pytest`, and the new tests are green.

## Repeat for new requirements

A raw blob of JSON is rarely what a caller wants. Usually you fetch a payload and pull one field
out of it. Let's add `get_user_name(url)`: fetch a user object, return its `"name"`.

The point of this second function is to show that once the network call is injectable, everything
built on top of it inherits the testability for free.

### Write the test first

```python
from .http_client import get_user_name


def test_get_user_name_extracts_the_field():
    opener = fake_opener(b'{"id": 7, "name": "Grace"}')
    assert get_user_name("http://example.test/u/7", opener=opener) == "Grace"
```

Same fake opener, same canned bytes, no network. We're testing "fetch then transform" without ever
proving `urllib` works, because that's not our code to test.

### Try to run the test

`get_user_name` doesn't exist yet:

```
ImportError: cannot import name 'get_user_name' from 'internet_http.http_client'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty string so the test runs and fails on the value:

```python
def get_user_name(url, opener=None):
    return ""
```

Run `uv run pytest`:

```
    def test_get_user_name_extracts_the_field():
        opener = fake_opener(b'{"id": 7, "name": "Grace"}')
>       assert get_user_name("http://example.test/u/7", opener=opener) == "Grace"
E       AssertionError: assert '' == 'Grace'
E         
E         - Grace
```

Failing on the value, exactly as designed.

### Write enough code to make it pass

Reuse `fetch_json` and index into the result. We thread the `opener` straight through, so the
injection point survives one layer up.

```python
def get_user_name(url: str, opener: Callable[[str], Any] | None = None) -> str:
    data = fetch_json(url, opener=opener)
    return data["name"]
```

Green. `get_user_name` does no networking of its own. It leans entirely on `fetch_json`, and
because that one is injectable, so is this one. That's the payoff: build on a testable seam and
the testability propagates.

### Refactor

Nothing to restructure. But we've been passing fakes by hand all chapter, and there's a second way
to swap the network out that's worth knowing: `unittest.mock.patch`. Instead of threading an
`opener` argument through, you replace the module-level `urlopen` for the duration of a `with`
block.

```python
from unittest.mock import patch


def test_fetch_json_with_patched_urlopen():
    with patch("internet_http.http_client.urlopen") as mock_urlopen:
        mock_urlopen.return_value = FakeResponse(b'{"ok": true}')
        assert fetch_json("http://example.test/ok") == {"ok": True}
        mock_urlopen.assert_called_once_with("http://example.test/ok")
```

Notice we call `fetch_json` with no `opener` here, so it falls back to the module's `urlopen`,
which `patch` has swapped for a mock. This is exactly why we resolved `urlopen` inside the body
instead of binding it as a default: a default would have captured the real function before `patch`
ever ran. The mock also lets us assert it was *called once with the right URL*, the same
input-checking the recording fake gave us, with less code.

Two styles, one idea. Explicit injection (the `opener` parameter) makes the seam visible in the
signature and is my default. `patch` is handy when you can't change the signature or when the
dependency is buried deeper. Run `uv run pytest` and the whole file is green.

## Wrapping up

- **`urllib.request.urlopen` plus `json.loads` is all you need** to fetch and parse JSON from the
  standard library. The response is a context manager whose `.read()` gives you `bytes`, and
  `json.loads` takes `bytes` directly.
- **Inject the network, don't reach for it.** An `opener` parameter that defaults to the real
  `urlopen` lets tests pass a fake that returns canned bytes, so the suite never touches the
  network and never flakes.
- **A fake can do more than return canned data.** Have it record the URLs it was called with, and
  you can assert on inputs, not just outputs.
- **Resolve the default at call time** (`if opener is None: opener = urlopen`), not as a default
  argument value, or `unittest.mock.patch` of the module-level name won't take effect.
- **Testability propagates.** Build on an injectable seam and everything above it (`get_user_name`)
  is testable for free.

Next: [Mocking](mocking.md), which takes the swap-out-the-dependency idea and goes deeper on fakes,
stubs, spies, and when each one is the right call.
