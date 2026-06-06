from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


def write_lines(path: Path, lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def read_lines(path: Path) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def count_words_in_file(path: Path) -> int:
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
    return total


@contextmanager
def working_directory(path: Path) -> Iterator[Path]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)
