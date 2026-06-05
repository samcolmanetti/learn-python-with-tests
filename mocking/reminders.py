"""A reminder service with injected dependencies, plus a config reader.

The point of this module is testability. ``ReminderService`` doesn't reach out to a real clock
or a real notification channel. It takes both as constructor arguments, so a test can hand it a
fake clock and a fake notifier and assert exactly what it did. That's dependency injection, and
it's what makes mocking pleasant instead of painful.

``default_channel`` reads an environment variable. We test it with ``monkeypatch`` so the test
never depends on the machine it runs on.
"""

from __future__ import annotations

import os
from datetime import datetime, time
from typing import Callable

# A notifier is anything callable that takes a message string and sends it somewhere.
Notifier = Callable[[str], None]
# A clock is anything callable that returns the current time. ``datetime.now`` fits.
Clock = Callable[[], datetime]


class ReminderService:
    """Sends reminders, but only during working hours.

    The clock and the notifier are injected. In production you'd pass ``datetime.now`` and a
    function that posts to Slack or sends an email. In a test you pass fakes.
    """

    def __init__(self, notifier: Notifier, clock: Clock) -> None:
        self.notifier = notifier
        self.clock = clock

    def remind(self, message: str) -> bool:
        """Send ``message`` if it's a working hour, otherwise drop it.

        Returns ``True`` if the reminder went out, ``False`` if it was suppressed.
        """
        now = self.clock()
        if time(9, 0) <= now.time() < time(17, 0):
            self.notifier(message)
            return True
        return False


def default_channel() -> str:
    """The channel reminders go to, from the ``REMINDER_CHANNEL`` env var.

    Falls back to ``"general"`` when the variable isn't set.
    """
    return os.environ.get("REMINDER_CHANNEL", "general")


def describe_channel() -> str:
    """A tiny function that *calls* ``default_channel``, to show ``patch`` in a test.

    Patching is for replacing a collaborator you don't want to run for real. Here the collaborator
    is ``default_channel`` (it reads the environment); ``patch`` lets a test pin its return value
    without touching ``os.environ``.
    """
    return "reminders go to #" + default_channel()
