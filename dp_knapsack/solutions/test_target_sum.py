from .target_sum import find_target_sum_ways


def test_classic_example():
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5


def test_single_number_hits_target():
    assert find_target_sum_ways([1], 1) == 1


def test_target_out_of_reach():
    assert find_target_sum_ways([1, 2], 5) == 0


def test_zero_can_take_either_sign():
    # The 0 contributes a +0 or a -0, doubling every way to reach the target.
    assert find_target_sum_ways([0, 1], 1) == 2


def test_negative_target_is_symmetric():
    assert find_target_sum_ways([1, 1, 1, 1, 1], -3) == 5


def test_impossible_parity():
    # sum is 1, target 0: (0 + 1) is odd, so no subset split exists.
    assert find_target_sum_ways([1], 0) == 0
