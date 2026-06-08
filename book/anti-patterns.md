# Anti-patterns

TDD and interview prep both have failure modes that *feel* productive while teaching you little.
Here are the ones to watch for.

## Testing anti-patterns

### Testing implementation instead of behaviour

A test should assert *what* a function does, not *how*. If your test checks that a helper was
called or inspects a private variable, it breaks the moment you refactor, even when behaviour is
unchanged. Assert on inputs and outputs:

```python
# Bad: couples the test to internal structure
assert solver._cache == {2: 1, 3: 2}

# Good: asserts the observable contract
assert solver.fib(5) == 5
```

### Over-mocking

Mock external boundaries (network, clock, filesystem), not your own logic. A test where
everything is mocked proves only that your mocks return what you told them to. In interview-style
problems you almost never need mocks at all: the code is pure functions over data.

### Assert-nothing tests

A test that runs code but asserts nothing (or asserts something always-true) is worse than no
test: it's a green light that means nothing. Every test must be able to *fail*. Watch it fail
before you make it pass. That's the discipline this book keeps repeating.

### One giant test

A single test with twenty assertions stops at the first failure and hides the rest. Prefer
several focused tests, or a `parametrize` table where each case is reported independently.

### Weak assertions

`assert result` passes for `True`, `1`, `"anything"`, and any non-empty list. `assert result ==
[1, 2, 3]` says what you actually mean. Be specific.

## Interview-prep anti-patterns

### Grinding problem count

300 solved problems with no structure is worse than 60 across well-understood patterns. Optimise
for **patterns you can execute from a blank file**, not for a number.

### Reading solutions without reproducing them

Understanding a solution is not the same as being able to write it. If you haven't re-derived it
from an empty file, you don't have it yet. (See [the blank-file rule](how-to-study.md).)

### Memorising specific problems

Interviewers vary the problem precisely so memorisation fails. Learn the *pattern* and its
trigger conditions, so you can adapt it to a problem you've never seen.

### Jumping straight to the optimal solution

Freezing because you can't see the O(n) trick immediately is common and avoidable. Write the
brute force, get it green, *then* optimise. A working O(n²) beats a broken O(n), and the
progression is exactly what's being scored.

### Silent coding

The answer matters less than your visible reasoning. Coding in silence, even correctly, gives
the interviewer nothing to evaluate. State the contract, name your edge cases, narrate the
trade-offs. Tests are a natural way to externalise all of this.

### Ignoring edge cases until they bite

Empty input, single element, duplicates, negatives, not-found. Enumerate them up front as tests,
while you can still think clearly, instead of discovering them when a hidden case fails.

## Wrapping up

- Test **behaviour**, with assertions specific enough to fail for the right reason.
- Mock boundaries, not your own logic, and rarely at that in interview problems.
- Optimise prep for **patterns reproduced from blank files**, not problem count.
- Make your reasoning **visible**: contract, edge cases, trade-offs, brute-force-then-optimise.
