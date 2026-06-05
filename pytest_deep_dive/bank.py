"""A tiny bank account, just enough behaviour to exercise pytest's core features."""

from __future__ import annotations


class InsufficientFunds(Exception):
    """Raised when a withdrawal would overdraw the account."""


class Account:
    def __init__(self, balance: int = 0) -> None:
        if balance < 0:
            raise ValueError("opening balance cannot be negative")
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"cannot withdraw {amount} from balance {self.balance}")
        self.balance -= amount
