# Math

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/math_problems)**

Number theory shows up in interviews as small, self-contained puzzles: count the primes, reduce a
fraction, raise something to a huge power without overflowing. Each one has a clean trick, and like
the other pattern chapters this is a reusable [`math_problems/_template.py`](math_problems/_template.py)
plus worked problems in `math_problems/solutions/`, all built test-first.

One housekeeping note before we start. The folder is `math_problems`, not `math`, on purpose. A
local module called `math` would shadow the standard library `math` module, and the next person who
writes `import math` gets your file instead of `sqrt` and friends. **Never name a folder after a
stdlib module.**

## When to reach for number theory

These tricks earn their place when the brute-force answer is too slow or overflows:

- You need **every prime below `n`**, or a primality fact about a whole range. A sieve precomputes
  all of them in one pass instead of testing each number on its own.
- You're reducing fractions, syncing cycles, or asking whether two numbers share a factor. That's
  a **greatest common divisor**, and Euclid's algorithm finds it in a handful of steps.
- You're computing `base ** exp` for a large `exp`, usually under a modulus. **Binary
  exponentiation** does it in O(log exp) multiplications instead of O(exp).

The unifying idea is the same one from prefix sum: do the clever work once, then read off answers
cheaply. The sieve makes that literal.

## The template

```python
def sieve(n):
    if n < 2:
        return [False] * n
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n, i):
                is_prime[multiple] = False
    return is_prime
```

This is the *Sieve of Eratosthenes*. We start by assuming every number below `n` is prime, then we
walk the numbers in order and, each time we land on one that's still marked prime, we cross off all
of its multiples. Whatever survives is prime.

Two details are worth memorising. We only loop `i` up to `sqrt(n)`, because any composite number
below `n` has a factor no bigger than its square root, so by the time we pass `sqrt(n)` everything
left has already been struck. And we start crossing off at `i * i`, not `2 * i`, because every
smaller multiple of `i` (`2*i`, `3*i`, ...) already got crossed off by a smaller prime. Those two
shortcuts are why the sieve runs in about O(n log log n) rather than O(n * sqrt(n)).

The invariant the build maintains: once we've finished processing all primes up to some value `p`,
every composite whose smallest prime factor is at most `p` is already marked `False`.

## Problem 1: Count Primes

> Count the prime numbers strictly less than a non-negative integer `n`. So `count_primes(10)` is
> `4`, the primes being 2, 3, 5, and 7.

The phrase "count the primes below `n`" is the sieve's home turf. We build the boolean array once
and sum the `True`s.

### Write the test first

```python
from .count_primes import count_primes


def test_no_primes_below_two():
    assert count_primes(2) == 0


def test_below_zero_and_one():
    assert count_primes(0) == 0
    assert count_primes(1) == 0


def test_classic_example():
    assert count_primes(10) == 4


def test_boundary_is_exclusive():
    assert count_primes(3) == 1
    assert count_primes(4) == 2


def test_larger_range():
    assert count_primes(100) == 25
```

The small inputs (`0`, `1`, `2`) are the cases that bite. "Strictly less than" means `count_primes(2)`
is `0`, not `1`, because 2 isn't below 2. And `test_boundary_is_exclusive` pins that down from the
other side: there's exactly one prime below 3 (just 2), and two below 4 (2 and 3).

### Try to run the test

We've imported `count_primes` from a module that doesn't define it yet, so collection fails on the
import before a single test runs:

```
math_problems/solutions/test_count_primes.py:1: in <module>
    from .count_primes import count_primes
E   ImportError: cannot import name 'count_primes' from 'math_problems.solutions.count_primes'
```

No function, no name to import. The error tells us exactly where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `count_primes` that ignores its argument and returns `0`. We're not solving anything yet.
We just want the tests to run so we can watch the real ones fail on the value, which proves they
check what we think they do.

```python
from __future__ import annotations


def count_primes(n: int) -> int:
    return 0
```

Run `uv run pytest`:

```
..FFF
    def test_classic_example():
>       assert count_primes(10) == 4
E       assert 0 == 4
E        +  where 0 = count_primes(10)
```

The two that pass (`test_no_primes_below_two` and `test_below_zero_and_one`) only pass because they
happen to expect `0`, which is what our stub returns. The other three fail on the value. That's the
right kind of failure: the test runs, and it disagrees with the stub for the right reason.

### Write enough code to make it pass

Now the real sieve. Build `is_prime`, cross off the multiples, and sum what survives.

```python
from __future__ import annotations


def count_primes(n: int) -> int:
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for multiple in range(i * i, n, i):
                is_prime[multiple] = False
    return sum(is_prime)
```

The tests pass.

The `if n < 3` guard handles the three small cases at once: for `n` of `0`, `1`, or `2` there are no
primes strictly below `n`, and it also keeps us from indexing `is_prime[1]` on a length-zero or
length-one array. After that it's the template's sieve, and `sum(is_prime)` counts the survivors
because Python sums `True` as `1` and `False` as `0`.

### Refactor

This is the template inlined, so there's nothing structural to tidy. It's worth naming why we didn't
just call `sieve` from `_template.py`: we could, but spelling the loop out here keeps the solution
readable on its own, and `count_primes` needs the count, not the array. The cost is identical. Re-run
the tests to confirm nothing moved.

## Problem 2: Greatest Common Divisor

> Return the greatest common divisor of two integers `a` and `b`: the largest integer that divides
> both with no remainder.

The slow way is to try every divisor down from `min(a, b)`. Euclid noticed something better two
thousand years ago: the gcd of `a` and `b` is the same as the gcd of `b` and `a % b`. Keep replacing
the pair until the remainder hits zero, and the other number is your answer.

### Write the test first

```python
from .gcd import gcd


def test_shared_factor():
    assert gcd(12, 18) == 6


def test_coprime():
    assert gcd(17, 5) == 1


def test_one_divides_the_other():
    assert gcd(48, 12) == 12


def test_zero_operand():
    assert gcd(0, 9) == 9
    assert gcd(9, 0) == 9
    assert gcd(0, 0) == 0


def test_negative_operands():
    assert gcd(-12, 18) == 6
    assert gcd(-12, -18) == 6
```

`test_coprime` covers the case where the only common divisor is `1`. The zero and negative cases are
where naive implementations quietly break: `gcd(0, 9)` should be `9` (every number divides `0`), and
gcd is about magnitude, so signs shouldn't change the answer.

### Try to run the test

Same story as before. The module is empty, so the import is the first thing to fail:

```
math_problems/solutions/test_gcd.py:1: in <module>
    from .gcd import gcd
E   ImportError: cannot import name 'gcd' from 'math_problems.solutions.gcd'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `gcd` to return `0` so the tests run:

```python
from __future__ import annotations


def gcd(a: int, b: int) -> int:
    return 0
```

Run `uv run pytest`:

```
FFFFF
    def test_shared_factor():
>       assert gcd(12, 18) == 6
E       assert 0 == 6
E        +  where 0 = gcd(12, 18)
```

Every test fails on the value. Good. (This time even the zero cases fail, because `gcd(0, 9)` wants
`9`, not the `0` our stub hands back.)

### Write enough code to make it pass

Euclid's algorithm is a three-line loop. Repeatedly replace `(a, b)` with `(b, a % b)` until `b` is
zero, then return `abs(a)`.

```python
from __future__ import annotations


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)
```

The tests pass.

The loop ends the moment `b` becomes `0`, and at that point `a` holds the divisor. The `abs` at the
end is what makes the negative cases work: `12 % -18` and friends can carry a sign through the loop
in Python, but the *greatest common divisor* is by definition non-negative, so we take the magnitude.
And `gcd(0, 0)` falls straight through the loop (b is already `0`) and returns `abs(0)`, which is `0`,
the conventional answer.

### Refactor

Three lines, nothing to extract. The one thing worth saying out loud is that this is the same
"reduce the problem to a smaller version of itself" move you'll see in recursion chapters, written as
a loop so it can't blow the stack on huge inputs. Re-run the tests.

## Problem 3: Fast Power

> Compute `(base ** exp) % mod` for a non-negative `exp`, fast enough that a huge exponent doesn't
> melt your laptop.

Multiplying `base` by itself `exp` times is O(exp), and `exp` can be in the billions. *Binary
exponentiation* gets it down to O(log exp) by squaring. The insight: `base**exp` is `base**(exp/2)`
squared when `exp` is even, and one extra `base` when it's odd. So we read the exponent's bits, and
for each bit we square the running base and multiply it into the result when the bit is set.

### Write the test first

```python
import pytest

from .fast_pow import fast_pow


def test_small_power():
    assert fast_pow(2, 10, 1000) == 24


def test_exponent_zero():
    assert fast_pow(7, 0, 13) == 1


def test_mod_one_is_always_zero():
    assert fast_pow(7, 5, 1) == 0


def test_matches_builtin_pow():
    assert fast_pow(3, 200, 1_000_000_007) == pow(3, 200, 1_000_000_007)


def test_base_larger_than_mod():
    assert fast_pow(123, 4, 7) == pow(123, 4, 7)


def test_negative_exponent_rejected():
    with pytest.raises(ValueError):
        fast_pow(2, -1, 5)
```

`test_small_power` is hand-checkable: `2**10` is `1024`, and `1024 % 1000` is `24`. The two tests
that compare against the built-in `pow(base, exp, mod)` are the real workhorses: Python's three-arg
`pow` already does modular exponentiation correctly, so it's a free oracle to check our logic against
large inputs. `test_exponent_zero` nails the base case (anything to the zero is `1`), and the
`ValueError` test states our contract: this function is for non-negative exponents only.

### Try to run the test

Nothing to import yet:

```
math_problems/solutions/test_fast_pow.py:2: in <module>
    from .fast_pow import fast_pow
E   ImportError: cannot import name 'fast_pow' from 'math_problems.solutions.fast_pow'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
from __future__ import annotations


def fast_pow(base: int, exp: int, mod: int) -> int:
    return 0
```

Run `uv run pytest`:

```
FF.FFF
    def test_small_power():
>       assert fast_pow(2, 10, 1000) == 24
E       assert 0 == 24
E        +  where 0 = fast_pow(2, 10, 1000)
```

Five fail on the value and one passes: `test_mod_one_is_always_zero` slips through because anything
mod `1` really is `0`, which is what the stub returns. That single accidental pass is a good reminder
that one green test proves nothing on its own. The `ValueError` test fails too, because our stub
never raises, which is exactly the next thing we need to fix.

### Write enough code to make it pass

Reject the negative exponent first, then run the squaring loop. We keep everything reduced mod `mod`
as we go so the numbers never grow large.

```python
from __future__ import annotations


def fast_pow(base: int, exp: int, mod: int) -> int:
    if exp < 0:
        raise ValueError("exp must be non-negative")
    result = 1 % mod
    base %= mod
    while exp:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result
```

Green.

Walk the loop with `exp` in binary. `exp & 1` asks "is the lowest bit set?", and if it is we fold the
current `base` into `result`. Then we square `base` (lining it up for the next bit) and shift `exp`
right by one to drop the bit we just handled. Each iteration handles one bit, so we do about
`log2(exp)` rounds. Reducing mod `mod` at every multiply keeps the intermediate values small, which
is the whole reason this is safe for enormous exponents.

The two tidy details: `result = 1 % mod` starts the accumulator at `1` but handles `mod == 1`
correctly (it becomes `0`), and `base %= mod` up front means `test_base_larger_than_mod` works
without a special case.

### Refactor

The body is already tight. **The shape to remember is "look at the bits, square the base, multiply on
a set bit."** It's the same skeleton you'd use for fast matrix power or any associative operation, not
just integer multiplication, so it's worth keeping in your head as a template rather than a one-off.
Re-run the tests and they stay green.

## Wrapping up

- **The Sieve of Eratosthenes** finds every prime below `n` in one shared pass, O(n log log n), by
  crossing off multiples starting at `i * i` and only looping `i` up to `sqrt(n)`.
- **Euclid's algorithm** finds a gcd by repeatedly replacing `(a, b)` with `(b, a % b)` until the
  remainder is zero. Take `abs` at the end so signs don't matter.
- **Binary exponentiation** computes `base ** exp` in O(log exp) by reading the exponent's bits,
  squaring the base each step and multiplying it in on a set bit. Reduce mod `mod` as you go.
- **Name your folder `math_problems`, never `math`**, so you don't shadow the standard library.

Next: [Bit Manipulation](bit-manipulation.md), where the `exp & 1` and `exp >>= 1` moves from fast
power become the whole toolkit.
