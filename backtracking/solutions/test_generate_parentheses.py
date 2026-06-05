from .generate_parentheses import generate_parentheses


def test_n_zero():
    assert generate_parentheses(0) == [""]


def test_n_one():
    assert generate_parentheses(1) == ["()"]


def test_n_two():
    assert sorted(generate_parentheses(2)) == sorted(["(())", "()()"])


def test_n_three():
    expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert sorted(generate_parentheses(3)) == sorted(expected)


def test_count_is_catalan():
    # The number of valid strings for n pairs is the nth Catalan number: 1, 1, 2, 5, 14.
    assert len(generate_parentheses(4)) == 14
