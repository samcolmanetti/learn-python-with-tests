from ._template import grid_dp


def test_grid_dp_counts_paths():
    # base = 1 on the first row/column, combine = up + left reproduces unique paths.
    dp = grid_dp(3, 7, lambda r, c: 1.0, lambda up, left, diag, here: up + left)
    assert dp[2][6] == 28


def test_grid_dp_fills_base_cases():
    dp = grid_dp(2, 2, lambda r, c: 5.0, lambda up, left, diag, here: 0.0)
    assert dp[0][0] == 5.0
    assert dp[0][1] == 5.0
    assert dp[1][0] == 5.0
