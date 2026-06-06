from pathlib import Path

from file_handling import (
    count_words_in_file,
    read_lines,
    working_directory,
    write_lines,
)


def test_write_then_read_round_trips(tmp_path):
    target = tmp_path / "notes.txt"
    write_lines(target, ["first", "second", "third"])
    assert read_lines(target) == ["first", "second", "third"]


def test_write_lines_creates_a_real_file(tmp_path):
    target = tmp_path / "out.txt"
    write_lines(target, ["only line"])
    assert target.read_text(encoding="utf-8") == "only line\n"


def test_read_lines_of_empty_file(tmp_path):
    target = tmp_path / "empty.txt"
    target.write_text("", encoding="utf-8")
    assert read_lines(target) == []


def test_count_words_in_file(tmp_path):
    target = tmp_path / "poem.txt"
    write_lines(target, ["the quick brown fox", "jumps over", "the lazy dog"])
    assert count_words_in_file(target) == 9


def test_count_words_in_empty_file(tmp_path):
    target = tmp_path / "blank.txt"
    target.write_text("", encoding="utf-8")
    assert count_words_in_file(target) == 0


def test_count_words_ignores_extra_whitespace(tmp_path):
    target = tmp_path / "spaced.txt"
    target.write_text("  one   two  \n\n   three   \n", encoding="utf-8")
    assert count_words_in_file(target) == 3


def test_working_directory_changes_then_restores(tmp_path):
    start = Path.cwd()
    with working_directory(tmp_path):
        # Inside the block we're in tmp_path. resolve() handles symlinked temp dirs.
        assert Path.cwd().resolve() == tmp_path.resolve()
    assert Path.cwd() == start


def test_working_directory_restores_on_exception(tmp_path):
    start = Path.cwd()
    try:
        with working_directory(tmp_path):
            raise ValueError("boom")
    except ValueError:
        pass
    assert Path.cwd() == start
