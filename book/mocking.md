# Mocking

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/mocking)**

Some code talks to the outside world: a clock, a network, an email server, an environment variable. You can't let a unit test send a real email or wait for 9am to roll around, so you swap the real thing for a stand-in you control. That stand-in is a mock, and Python ships everything you need in `unittest.mock` plus pytest's `monkeypatch`.

We'll build a reminder service that only fires during working hours, drive it with fake clocks and a `Mock` notifier, read config from an environment variable with `monkeypatch`, and finish with `patch`. Along the way I'll be blunt about the part most tutorials skip: when *not* to mock.

## Write the test first

Our first requirement: a reminder sent at 10am, a working hour, should go out. The service shouldn't own a clock or a notification channel, because then a test couldn't see what it did. So we inject both.

The notifier is the thing we want to watch. Instead of writing a fake class with a `called` flag and a `last_message` attribute by hand, we hand the service a `Mock`. A `Mock` records every call made to it, and then lets us assert on those calls afterwards.

```python
from datetime import datetime
from unittest.mock import Mock

from reminders import ReminderService


def at(hour: int, minute: int = 0) -> datetime:
    """A fake clock value: a fixed datetime on a fixed day."""
    return datetime(2026, 6, 4, hour, minute)


def test_sends_during_working_hours():
    notifier = Mock()
    service = ReminderService(notifier=notifier, clock=lambda: at(10))

    sent = service.remind("stand up")

    assert sent is True
    notifier.assert_called_once_with("stand up")
```

The clock is just a `lambda` returning a fixed `datetime`. No mock needed there, a plain function is a fake clock. The notifier is a `Mock`, and `assert_called_once_with("stand up")` says: this was called exactly once, and with exactly that argument.

## Try to run the test

`ReminderService` doesn't exist yet, so the import is the first thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'ReminderService' from 'reminders'
```

Nothing to import. The error is telling us where to start: there's no class yet.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `ReminderService` that takes the two dependencies and a `remind` that always returns `False` and never notifies. It's deliberately wrong. We want to watch the test fail on behaviour, not on a missing name, which proves the test checks what we think it does.

```python
from __future__ import annotations


class ReminderService:
    def __init__(self, notifier, clock):
        self.notifier = notifier
        self.clock = clock

    def remind(self, message):
        return False
```

Run `uv run pytest`:

```
    def test_sends_during_working_hours():
        notifier = Mock()
        service = ReminderService(notifier=notifier, clock=lambda: at(10))
        sent = service.remind("stand up")
>       assert sent is True
E       assert False is True
```

It fails on the return value, exactly as it should. The `Mock` assertion never even gets a chance to run because `assert sent is True` blows up first. Good, the test is wired to the real behaviour.

## Write enough code to make it pass

Pull the current time from the injected clock, and if it falls inside working hours, call the notifier and report that we sent it.

```python
from __future__ import annotations

from datetime import time
from typing import Callable

Notifier = Callable[[str], None]
Clock = Callable[[], "datetime"]


class ReminderService:
    def __init__(self, notifier: Notifier, clock) -> None:
        self.notifier = notifier
        self.clock = clock

    def remind(self, message: str) -> bool:
        now = self.clock()
        if time(9, 0) <= now.time() < time(17, 0):
            self.notifier(message)
            return True
        return False
```

Run the tests and we're green.

Here's the thing the `Mock` bought us. We never wrote a fake notifier class. We passed `Mock()`, the service called it, and `assert_called_once_with("stand up")` checked both the count and the argument in one line. If the service had called `self.notifier("hello")` instead, that same assertion would tell us:

```
E           AssertionError: expected call not found.
E           Expected: mock('stand up')
E           Actual: mock('hello')
```

That `Expected` versus `Actual` is why we mock the notifier instead of just checking a return value. **A `Mock` lets you assert on the conversation your code has with its collaborator, not just the answer it returns.**

## Refactor

Let me clean up the types. The `clock` parameter has no annotation and the `Clock` alias is sitting unused. We pin them both down, and add `MagicMock` to our vocabulary while we're here: `Mock` and `MagicMock` are nearly the same, but `MagicMock` also supports magic methods (`__len__`, `__iter__`, `__enter__`), so it's the safe default when your code might do `len(x)` or `with x:` on the mock. We don't need that here, so plain `Mock` is honest about what we use.

```python
from __future__ import annotations

from datetime import datetime, time
from typing import Callable

Notifier = Callable[[str], None]
Clock = Callable[[], datetime]


class ReminderService:
    def __init__(self, notifier: Notifier, clock: Clock) -> None:
        self.notifier = notifier
        self.clock = clock

    def remind(self, message: str) -> bool:
        now = self.clock()
        if time(9, 0) <= now.time() < time(17, 0):
            self.notifier(message)
            return True
        return False
```

Re-run the tests, still green. Before we move on, let's add the two boundary cases that pin the working-hours rule down, since "9 to 5" is exactly the kind of thing that's off by a minute in real code:

```python
def test_suppresses_before_nine():
    notifier = Mock()
    service = ReminderService(notifier=notifier, clock=lambda: at(8, 59))

    sent = service.remind("too early")

    assert sent is False
    notifier.assert_not_called()


def test_suppresses_at_five_pm_exactly():
    notifier = Mock()
    service = ReminderService(notifier=notifier, clock=lambda: at(17))

    sent = service.remind("home time")

    assert sent is False
    notifier.assert_not_called()
```

`assert_not_called()` is the mirror of `assert_called_once_with`: it asserts the notifier stayed silent. Both pass, because 5pm is `< time(17, 0)` is false, so the reminder is correctly suppressed.

## Repeat for new requirements

A `lambda` is a fine fake clock, but sometimes you want to assert that your code *called* the clock, and how. That's a job for a `Mock` again, this time on the clock side.

### Write the test first

A `Mock` with `return_value=` set will return that value every time it's called, and still record the call. So we can use one mock to feed the time in and to check it was read exactly once.

```python
def test_clock_can_be_a_mock_too():
    notifier = Mock()
    clock = Mock(return_value=at(12))
    service = ReminderService(notifier=notifier, clock=clock)

    service.remind("lunch")

    clock.assert_called_once_with()
    notifier.assert_called_once_with("lunch")
```

`clock.assert_called_once_with()` (empty parentheses) asserts the clock was called once with no arguments, which is how `self.clock()` calls it.

### Try to run the test

This one passes immediately, and that's fine. The implementation already calls `self.clock()` once with no arguments, so there's nothing to fail. **Not every new test needs new code. Sometimes a test exists to lock in behaviour you already have so a later change can't break it silently.**

### Refactor

Nothing to change in the code. The lesson is in the test: `Mock(return_value=...)` gives you a fake that feeds a value *and* records how it was used, which a bare `lambda` can't do.

## Repeat for new requirements

Reminders go to a channel, and the channel name comes from an environment variable so ops can change it without a code change. We can't have the test depend on whatever is actually set on the machine running it, so we set the variable for the duration of the test and tear it down after. That's exactly what pytest's `monkeypatch` fixture does.

### Write the test first

Ask for the `monkeypatch` fixture by putting it in the test's parameter list. `monkeypatch.setenv` sets an environment variable and, importantly, undoes it automatically when the test finishes, so tests can't leak state into each other.

```python
def test_default_channel_reads_env(monkeypatch):
    monkeypatch.setenv("REMINDER_CHANNEL", "alerts")
    assert default_channel() == "alerts"


def test_default_channel_falls_back(monkeypatch):
    monkeypatch.delenv("REMINDER_CHANNEL", raising=False)
    assert default_channel() == "general"
```

The second test uses `monkeypatch.delenv(..., raising=False)` to guarantee the variable is *absent*, so we can check the fallback. `raising=False` means "don't error if it wasn't set in the first place".

### Try to run the test

`default_channel` doesn't exist, so the import fails:

```
ImportError: cannot import name 'default_channel' from 'reminders'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return the fallback unconditionally. That makes the fallback test pass by luck and the read-from-env test fail, which is what we want to see.

```python
def default_channel() -> str:
    return "general"
```

Run `uv run pytest`:

```
    def test_default_channel_reads_env(monkeypatch):
        monkeypatch.setenv("REMINDER_CHANNEL", "alerts")
>       assert default_channel() == "alerts"
E       AssertionError: assert 'general' == 'alerts'
E         - alerts
E         + general
```

The stub ignores the environment entirely, so the value we set with `monkeypatch.setenv` doesn't reach it. Failing for the right reason.

### Write enough code to make it pass

Read the variable, fall back to `"general"` when it's missing.

```python
import os


def default_channel() -> str:
    return os.environ.get("REMINDER_CHANNEL", "general")
```

Both tests pass. And here's the payoff of `monkeypatch`: after each test, your real environment is untouched. We never wrote teardown code, the fixture handled it. **Use `monkeypatch` for environment variables, attributes, and `sys.path`, because it restores the original automatically when the test ends.**

### Refactor

Nothing to tidy in a one-liner. Move the `import os` to the top of the module with the other imports where it belongs, re-run, still green.

## Repeat for new requirements

One more tool, and then the part everyone gets wrong. Say we have a function that *uses* `default_channel` internally rather than taking it as an argument:

```python
def describe_channel() -> str:
    return "reminders go to #" + default_channel()
```

We don't want to set an environment variable just to test the string formatting here. We want to replace `default_channel` with something that returns a known value for one test. That's `unittest.mock.patch`.

### Write the test first

`patch` as a context manager replaces a name with a `Mock` for the duration of the `with` block, then restores it. The string you pass is the *full path to where the name is looked up*, not where it's defined.

```python
from unittest.mock import patch


def test_describe_channel_with_patch():
    with patch("reminders.default_channel", return_value="ops"):
        assert describe_channel() == "reminders go to #ops"
```

That `return_value="ops"` makes the patched `default_channel` return `"ops"` whenever it's called inside the block.

### Try to run the test

`describe_channel` isn't defined yet:

```
ImportError: cannot import name 'describe_channel' from 'reminders'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty string so the test runs and fails on the value:

```python
def describe_channel() -> str:
    return ""
```

Run `uv run pytest`:

```
    def test_describe_channel_with_patch():
        with patch("reminders.default_channel", return_value="ops"):
>           assert describe_channel() == "reminders go to #ops"
E           AssertionError: assert '' == 'reminders go to #ops'
E             - reminders go to #ops
```

The patch is working (no error about the path), the stub just returns the wrong thing. Exactly the failure we wanted.

### Write enough code to make it pass

```python
def describe_channel() -> str:
    return "reminders go to #" + default_channel()
```

Green. The same `patch` works as a decorator if you prefer, and then the mock is injected as an argument:

```python
@patch("reminders.default_channel", return_value="ops")
def test_describe_channel_decorated(mock_channel):
    assert describe_channel() == "reminders go to #ops"
```

The one trap with `patch` is the path. You patch `reminders.default_channel`, the name as `describe_channel` sees it, not `reminders.default_channel` based on where you imported it in the test. **Patch where the name is used, not where it's defined.** Get this wrong and your "mock" silently does nothing while the real function runs.

### Refactor

Nothing to change in the code. The point of this cycle is the tool and its one sharp edge.

### But isn't mocking evil?

You've now got three ways to replace a dependency, so the dangerous question is *when*. Here's my flat opinion, and it's the most useful thing in this chapter.

**Mock at the boundaries of your system, not inside your own logic.** A clock, the network, the filesystem, the environment, a third-party API: these are boundaries, and faking them is what makes a test fast and deterministic. Look back at what we mocked: the notifier (a network boundary) and the clock (the system clock). Both are things a unit test genuinely cannot run for real.

What we did *not* do is mock the working-hours check. We let the real `if time(9, 0) <= now.time() < time(17, 0)` run, and we tested it through its boundaries by feeding fake times in. That logic is the thing under test. If you mock your own logic, your test asserts that your code calls the functions you think it calls, which tells you nothing about whether it's correct. Worse, every refactor breaks a wall of mocks even when the behaviour never changed.

So before you reach for `patch`, ask: is this a boundary, or is it my own code? If it's a boundary, fake it. If it's your own code, call it for real and test the result. **A test full of mocks of your own functions is a test that's coupled to your implementation and blind to your bugs.**

## Wrapping up

- **`Mock` records calls** so you can assert on the conversation, not just the return value: `assert_called_once_with`, `assert_not_called`, and `return_value` for what the mock hands back.
- **`MagicMock`** is `Mock` plus magic methods (`__len__`, `__enter__`, ...). Reach for it when your code treats the mock as a container or context manager.
- **`monkeypatch`** sets environment variables and attributes for one test and restores them automatically. Use it for env vars and `sys`-level state.
- **`patch`** swaps a name for a mock as a context manager or a decorator. Patch the name *where it's used*, not where it's defined.
- **Mock the boundaries** (clock, network, filesystem, env), never your own logic. Inject dependencies so the seams exist before you need them.

Next: [Property-Based Testing](property-based-testing.md), where instead of picking example inputs by hand, we let the tool generate hundreds of them and hunt for the one that breaks us.
