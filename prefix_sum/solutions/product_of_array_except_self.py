"""Product of Array Except Self.

Return ``output`` where ``output[i]`` is the product of every element except ``nums[i]``, with
no division (division breaks on a zero in the array). This is the prefix-sum idea with
multiplication: ``output[i]`` is the product of everything to the left of ``i`` times the
product of everything to the right. Two passes, no extra arrays beyond the output.
"""

from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    output = [1] * n

    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output
