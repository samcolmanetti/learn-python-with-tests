from ._template import bottom_up


def test_returns_base_case_directly():
    assert bottom_up(0, base=[1, 1], transition=lambda dp, i: dp[i - 1] + dp[i - 2]) == 1
    assert bottom_up(1, base=[1, 1], transition=lambda dp, i: dp[i - 1] + dp[i - 2]) == 1


def test_fibonacci_transition():
    fib = bottom_up(6, base=[1, 1], transition=lambda dp, i: dp[i - 1] + dp[i - 2])
    assert fib == 13
