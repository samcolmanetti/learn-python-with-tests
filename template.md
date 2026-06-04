# Chapter template

*Copy this when writing a new chapter. Delete the guidance in italics as you fill it in.*

---

# [Chapter title]

**[You can find all the code for this chapter here](https://github.com/your-org/python-with-tests/tree/main/CHAPTER_FOLDER)**

*One or two sentences: what will the reader be able to do after this chapter, and what
Python feature or interview pattern does it teach?*

## Write the test first

*Start with the smallest behaviour you can describe. Write a `pytest` test for a function
that does not exist yet. Show the test code.*

```python
def test_something():
    assert something("input") == "expected"
```

## Try to run the test

*Run `pytest`. Show the failing output — for a missing function this is usually a
`NameError` or `ImportError`. Confirming the failure proves the test is wired up.*

```
NameError: name 'something' is not defined
```

## Write the minimal amount of code for the test to run and check the failing test output

*Write just enough for the test to **run** (not pass) — e.g. a stub returning the wrong
thing — and show the assertion failure. Keep the discipline: don't solve it yet.*

```
AssertionError: assert '' == 'expected'
```

## Write enough code to make it pass

*Now make it pass with the simplest code that works. Show the implementation and the green
run.*

```
1 passed
```

## Refactor

*Improve names, remove duplication, tidy the implementation — with the test as your safety
net. Re-run to stay green.*

## Repeat for new requirements

*Add the next failing test for the next behaviour (an edge case, an error path) and walk the
loop again. Most chapters cycle through this section a few times.*

## Wrapping up

*Summarise the idea in a few bullets:*

- *The Python feature or pattern, in one line.*
- *When to reach for it in an interview.*
- *The invariant or gotcha worth memorising.*
