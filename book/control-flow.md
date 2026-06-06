# Control flow

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/control_flow)**

Control flow is how a program decides what to do next: branch on a condition, loop over some work,
bail out early. We'll build two small functions test-first, `fizzbuzz` and `grade_classifier`, and
pick up `if`/`elif`/`else`, `for`, `while`, `break`, `continue`, truthiness, and the ternary along
the way.

## Write the test first

FizzBuzz is the classic warm-up: count from 1, but say "Fizz" for multiples of 3, "Buzz" for
multiples of 5, and "FizzBuzz" for multiples of both. We'll return a list of strings so the tests
can check it without capturing printed output.

Start with the dullest possible case: a couple of plain numbers, no fizzing yet. In
`control_flow/test_control_flow.py`:

```python
from control_flow import fizzbuzz


def test_fizzbuzz_plain_numbers():
    assert fizzbuzz(2) == ["1", "2"]
```

## Try to run the test

We've imported `fizzbuzz` from a module that doesn't define it yet, so the import is the first
thing to break. Run `uv run pytest`:

```
ImportError: cannot import name 'fizzbuzz' from 'control_flow.control_flow'
```

Listen to the error: there's no function, so that's where we start.

## Write the minimal amount of code for the test to run and check the failing test output

Give it a `fizzbuzz` that ignores its argument and returns an empty list. We're not solving
anything yet. We just want the test to run so we can watch it fail on the value, which proves the
test checks what we think it does. In `control_flow/control_flow.py`:

```python
def fizzbuzz(n):
    return []
```

Run `uv run pytest`:

```
    def test_fizzbuzz_plain_numbers():
>       assert fizzbuzz(2) == ["1", "2"]
E       AssertionError: assert [] == ['1', '2']
E         Right contains 2 more items, first extra item: '1'
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

## Write enough code to make it pass

We need to walk the numbers from 1 to `n` and collect each one as a string. A `for` loop over
`range` does the walking.

```python
def fizzbuzz(n):
    lines = []
    for i in range(1, n + 1):
        lines.append(str(i))
    return lines
```

`range(1, n + 1)` yields `1, 2, ..., n`. The `+ 1` is there because `range` stops one short of its
upper bound, so `range(1, 3)` gives us `1, 2`. Run the tests again and they're green.

## Refactor

There's nothing to tidy in four lines, and the next requirement is about to change the loop body
anyway, so we'll leave it. Re-run the tests to confirm nothing moved.

## Repeat for new requirements: Fizz and Buzz

Now the actual point of the exercise. Multiples of 3 become "Fizz", multiples of 5 become "Buzz".

### Write the test first

```python
def test_fizzbuzz_fizz_on_three():
    assert fizzbuzz(3) == ["1", "2", "Fizz"]


def test_fizzbuzz_buzz_on_five():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
```

The five-element case checks both rules at once: `3` fizzes, `5` buzzes, and `4` stays a plain
number in between.

### Try to run the test

Our current loop stringifies every number, so the new tests fail on the value. Run `uv run pytest`:

```
    def test_fizzbuzz_fizz_on_three():
>       assert fizzbuzz(3) == ["1", "2", "Fizz"]
E       AssertionError: assert ['1', '2', '3'] == ['1', '2', 'Fizz']
```

We produced `'3'` where the test wants `'Fizz'`. No surprise: we haven't told the code about
multiples yet.

### Write enough code to make it pass

To branch on a condition we reach for `if`/`elif`/`else`. The test for "is `i` a multiple of 3" is
`i % 3 == 0`, where `%` is the modulo (remainder) operator: `6 % 3` is `0`, `7 % 3` is `1`.

```python
def fizzbuzz(n):
    lines = []
    for i in range(1, n + 1):
        if i % 3 == 0:
            lines.append("Fizz")
        elif i % 5 == 0:
            lines.append("Buzz")
        else:
            lines.append(str(i))
    return lines
```

The chain runs top to bottom and stops at the first branch that's true. `if` tests the first
condition, each `elif` (short for "else if") tests another, and the `else` catches everything that
fell through. A number like `4` matches neither multiple, so it lands in the `else`. The tests pass.

### Refactor

Nothing to clean up, but it's worth naming what we just used: an `if`/`elif`/`else` *chain* is
mutually exclusive. Exactly one branch runs. We'll lean on that in a moment when the order of the
branches starts to matter. Re-run the tests.

## Repeat for new requirements: FizzBuzz, and why order matters

A multiple of both 3 and 5 (so a multiple of 15) should be "FizzBuzz".

### Write the test first

```python
def test_fizzbuzz_fizzbuzz_on_fifteen():
    assert fizzbuzz(15)[-1] == "FizzBuzz"


def test_fizzbuzz_zero_is_empty():
    assert fizzbuzz(0) == []
```

I'm checking `fizzbuzz(15)[-1]`, the last element, rather than spelling out all fifteen lines: 15
is the first number that should fizz *and* buzz, and `[-1]` indexes from the end. The zero case
earns its keep too: `range(1, 1)` is empty, so the loop never runs and we get `[]` for free.

### Try to run the test

Run `uv run pytest`:

```
    def test_fizzbuzz_fizzbuzz_on_fifteen():
>       assert fizzbuzz(15)[-1] == "FizzBuzz"
E       AssertionError: assert 'Fizz' == 'FizzBuzz'
```

Look closely at that failure. `15 % 3 == 0` is true, so our chain takes the *first* matching branch
and returns `"Fizz"`, then never even checks the 5. The `else if` structure that made the branches
mutually exclusive is now working against us.

### Write enough code to make it pass

The fix is to test the most specific condition first. A multiple of 15 is the special case, so it
goes at the top of the chain.

```python
def fizzbuzz(n):
    lines = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            lines.append("FizzBuzz")
        elif i % 3 == 0:
            lines.append("Fizz")
        elif i % 5 == 0:
            lines.append("Buzz")
        else:
            lines.append(str(i))
    return lines
```

**In an `if`/`elif` chain, order is part of the logic.** Put the narrowest condition first, because
the chain commits to the first match and ignores the rest. The tests pass, including the empty-list
case that the loop handled without any special code.

### Refactor

The function is doing one clear thing per line, so I'll leave the shape alone. Re-run the tests to
keep yourself honest.

## Repeat for new requirements: grading, and the value of boundaries

On to the second function. `grade_classifier` takes a `score` from 0 to 100 and returns a letter:
A for 90 and up, then B, C, D in ten-point bands, and F below 60.

### Write the test first

```python
def test_grade_a():
    assert grade_classifier(95) == "A"


def test_grade_boundaries():
    assert grade_classifier(90) == "A"
    assert grade_classifier(89) == "B"
    assert grade_classifier(60) == "D"
    assert grade_classifier(59) == "F"


def test_grade_zero():
    assert grade_classifier(0) == "F"
```

The middle test is the one I care about. Off-by-one errors live on the boundaries, so we pin down
both sides of each edge: `90` is an A but `89` is a B, `60` is a D but `59` is an F. If the code
ever uses `>` where it meant `>=`, one of these catches it.

Add the new import for `grade_classifier` to the top of the test file:

```python
from control_flow import fizzbuzz, grade_classifier
```

### Try to run the test

`grade_classifier` doesn't exist yet, so the import breaks first. Run `uv run pytest`:

```
ImportError: cannot import name 'grade_classifier' from 'control_flow.control_flow'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always return `"F"` so the tests run on the value:

```python
def grade_classifier(score):
    return "F"
```

Run `uv run pytest`:

```
    def test_grade_a():
>       assert grade_classifier(95) == "A"
E       AssertionError: assert 'F' == 'A'
E         - A
E         + F
```

`test_grade_zero` happens to pass, because `0` really is an F and that's all our stub knows how to
say. The graded cases fail on the value. Good, now let's make them pass for the right reason.

### Write enough code to make it pass

Another `if`/`elif` chain, and here the top-down ordering does real work. If we check `>= 90`
first, then by the time we reach `>= 80` we already know the score is below 90, so testing only the
lower bound is enough.

```python
def grade_classifier(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

Each branch `return`s, so we never need an explicit "and less than 90" clause: reaching the second
`elif` already implies it. The boundary tests pass because `>=` includes the edge: `90 >= 90` is
true, so `90` is an A, while `89` falls through to the B branch.

### Refactor

Clean as it is. Returning from each branch keeps the function flat and readable, which beats setting
a `grade` variable and returning it at the end. Re-run the tests.

## Repeat for new requirements: rejecting bad input

A score of `150` isn't an A, it's nonsense. Let's reject anything outside 0 to 100.

### Write the test first

```python
import pytest


def test_grade_rejects_too_high():
    with pytest.raises(ValueError):
        grade_classifier(101)


def test_grade_rejects_negative():
    with pytest.raises(ValueError):
        grade_classifier(-1)
```

`pytest.raises` asserts that the block inside the `with` raises the given exception. If
`grade_classifier(101)` returns a grade instead of raising, the test fails. (Put the `import pytest`
at the top of the test file with the other imports.)

### Try to run the test

Right now `grade_classifier(101)` cheerfully returns `"A"`, so no exception is raised. Run
`uv run pytest`:

```
    def test_grade_rejects_too_high():
        with pytest.raises(ValueError):
>           grade_classifier(101)
E           Failed: DID NOT RAISE <class 'ValueError'>
```

"DID NOT RAISE" is pytest telling us the code sailed through without complaint.

### Write enough code to make it pass

Guard the input at the top with a single `if` and a compound condition. The `or` is true when
*either* side is, so we reject a score that's too low or too high.

```python
def grade_classifier(score):
    if score < 0 or score > 100:
        raise ValueError("score must be between 0 and 100")
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

A guard clause that raises and returns early keeps the bad case out of the main logic below. The
tests pass, and the earlier grading tests still pass because valid scores never trip the guard.

### Refactor

You could write the guard as `if not (0 <= score <= 100)`, using Python's chained comparison (yes,
`0 <= score <= 100` reads exactly like the maths). Both say the same thing. I find the explicit
`< 0 or > 100` reads more plainly as "out of range", so I'll keep it. Re-run the tests.

## Repeat for new requirements: while, break, continue, and truthiness

One more function to exercise the looping keywords we haven't met yet. `first_passing` takes a list
of scores and returns the grade of the first *passing* one (60 or better, so anything that isn't an
F), skipping any junk values that fall outside 0 to 100. If nothing passes, it returns `"none"`.

### Write the test first

```python
def test_first_passing_finds_first():
    assert first_passing([40, 55, 72, 95]) == "C"


def test_first_passing_skips_invalid():
    assert first_passing([200, -3, 88]) == "B"


def test_first_passing_none_when_all_fail():
    assert first_passing([10, 20, 30]) == "none"


def test_first_passing_empty():
    assert first_passing([]) == "none"
```

`test_first_passing_finds_first` wants `"C"`: `40` and `55` are failing, `72` is the first passing
score and grades to a C, and we stop there without ever looking at `95`. The skip case checks that
`200` and `-3` get thrown out before they're graded. Extend the import once more:

```python
from control_flow import first_passing, fizzbuzz, grade_classifier
```

### Try to run the test

The function doesn't exist yet:

```
ImportError: cannot import name 'first_passing' from 'control_flow.control_flow'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always return `"none"`:

```python
def first_passing(scores):
    return "none"
```

Run `uv run pytest`:

```
    def test_first_passing_finds_first():
>       assert first_passing([40, 55, 72, 95]) == "C"
E       AssertionError: assert 'none' == 'C'
E         - C
E         + none
```

The two "nothing passes" tests pass by accident (our stub only ever says `"none"`), and the real
cases fail on the value. Onward.

### Write enough code to make it pass

We'll walk the list with a `while` loop and an index, so we have somewhere to show `break` and
`continue`. `continue` jumps straight to the next iteration, skipping the rest of the loop body;
`break` leaves the loop entirely.

```python
def first_passing(scores):
    i = 0
    answer = "none"
    while i < len(scores):
        score = scores[i]
        i += 1
        if not (0 <= score <= 100):
            continue
        grade = grade_classifier(score)
        if grade != "F":
            answer = grade
            break
    return answer
```

When a score is out of range, `continue` skips it before we ever call `grade_classifier`, which is
why the guard in that function never fires here. When we find a passing grade, we record it and
`break` out, so later scores are never examined. That early exit is the whole point: we want the
*first* passing grade, not all of them. The tests pass.

### Refactor

Worth a word on truthiness, since it's lurking here. An empty list is *falsy* in Python: `[]`, `0`,
`""`, and `None` all behave like `False` in a condition, while non-empty containers and non-zero
numbers are *truthy*. Our `while i < len(scores)` already handles the empty list (the condition is
false immediately, so the loop body never runs), but you'll often see the shorter `while scores:`
idiom that leans on truthiness directly.

One more idiom belongs in a chapter on control flow: the *ternary*, Python's one-line conditional.
The shape is `value_if_true if condition else value_if_false`. The grade-or-default choice could
fold into a single expression:

```python
result = grade if grade != "F" else answer
```

It reads right to left compared to other languages, but once it clicks it's tidy for short
either-or assignments. Don't reach for it when the branches are long; a plain `if`/`else` is clearer
then. Re-run the tests and watch all of them stay green.

> A note for the future: Python 3.10 added `match`/`case`, a structural pattern-matching statement
> that can read more cleanly than a long `if`/`elif` chain. We're targeting Python 3.9 in this book,
> so we won't use it, but it's worth knowing it exists once you're on 3.10 or newer.

## Wrapping up

* `if`/`elif`/`else` chains are mutually exclusive and run top to bottom, so **order is part of the
  logic**: put the most specific condition first.
* `for` walks a `range` or a collection; `while` loops on a condition.
* `continue` skips to the next iteration, `break` leaves the loop. Use them to skip junk and to stop
  at the first hit.
* **Boundary tests** (`89` versus `90`) are where `>` versus `>=` bugs hide. Test both sides of
  every edge.
* Truthiness: `[]`, `0`, `""`, and `None` are falsy; the ternary `a if cond else b` is the one-line
  conditional. `match`/`case` is a 3.10+ option we're skipping here.

Next: [Comprehensions](comprehensions.md), where a loop that builds a list collapses into a single
expression.
