from datetime import datetime
from unittest.mock import Mock, patch

from reminders import (
    ReminderService,
    default_channel,
    describe_channel,
)


def at(hour: int, minute: int = 0) -> datetime:
    """A fake clock value: a fixed datetime on a fixed day."""
    return datetime(2026, 6, 4, hour, minute)


def test_sends_during_working_hours():
    notifier = Mock()
    service = ReminderService(notifier=notifier, clock=lambda: at(10))

    sent = service.remind("stand up")

    assert sent is True
    notifier.assert_called_once_with("stand up")


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


def test_clock_can_be_a_mock_too():
    notifier = Mock()
    clock = Mock(return_value=at(12))
    service = ReminderService(notifier=notifier, clock=clock)

    service.remind("lunch")

    clock.assert_called_once_with()
    notifier.assert_called_once_with("lunch")


def test_default_channel_reads_env(monkeypatch):
    monkeypatch.setenv("REMINDER_CHANNEL", "alerts")
    assert default_channel() == "alerts"


def test_default_channel_falls_back(monkeypatch):
    monkeypatch.delenv("REMINDER_CHANNEL", raising=False)
    assert default_channel() == "general"


def test_describe_channel_with_patch():
    with patch("reminders.default_channel", return_value="ops"):
        assert describe_channel() == "reminders go to #ops"


@patch("reminders.default_channel", return_value="ops")
def test_describe_channel_decorated(mock_channel):
    assert describe_channel() == "reminders go to #ops"
