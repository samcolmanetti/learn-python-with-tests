# Modules and packaging

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/modules_packaging)**

Every Python file is a module, and a folder of modules is a package. In this chapter we'll grow a tiny `shapes` package test-first and watch how `import`, `__init__.py`, `__all__`, and relative imports actually behave.

We're going to build a sub-package `modules_packaging/shapes/` with one module per shape, then a flat `geometry.py` next to it that imports and uses the package. The tests drive the whole thing, so by the end you'll have seen exactly which `import` statement breaks when, and why.

## Write the test first

Start with the smallest useful thing: the area of a square. We'll keep each shape in its own file inside a `shapes` package, and re-export a tidy `square_area` name from the package itself.

Here's the test, in `modules_packaging/test_geometry.py`:

```python
from .shapes import square_area


def test_square_area():
    assert square_area(3) == 9
```

That import line is the interesting part. The leading dot means "relative to the package this test lives in". So `from .shapes import square_area` reads as: from the `shapes` sub-package sitting next to me, import the name `square_area`. None of that exists yet.

## Try to run the test

Run `uv run pytest`. The import is the first thing to blow up, before any assertion runs:

```
ImportError: cannot import name 'area' from 'modules_packaging.shapes.square' (/Users/soar/src/python-with-tests/modules_packaging/shapes/square.py)
```

(I've written the package skeleton in the steps below already, so the error you see has walked one layer deeper than a bare module would. The point stands: Python can find the package, but the name we asked for isn't there yet.)

Listen to the traceback. It's a map. The test imported `shapes`, which ran `shapes/__init__.py`, which tried to pull `area` out of `square.py`, and `square.py` had nothing to give. **A package's `__init__.py` runs when the package is first imported, so an error in it surfaces as an import error in whoever imported the package.**

## Write the minimal amount of code for the test to run and check the failing test output

Let's lay down the skeleton, but make `square.area` deliberately wrong. We want the test to run and fail on the value, which proves the wiring is right before the maths is.

A package is just a folder with an `__init__.py`. Create these four files:

`modules_packaging/shapes/square.py`:

```python
from __future__ import annotations


def area(side: float) -> float:
    return 0.0
```

`modules_packaging/shapes/circle.py` (empty for now, we'll fill it in the next cycle):

```python
from __future__ import annotations
```

`modules_packaging/shapes/__init__.py`, which re-exports the per-shape `area` functions under clearer names:

```python
"""A tiny sub-package of area helpers, one shape per module."""

from .square import area as square_area

__all__ = ["square_area"]
```

That `from .square import area as square_area` is a *relative import*: the dot says "from this same package". We rename `area` to `square_area` on the way out so callers don't have to write `square.area`, they just write `square_area`.

The `__all__` list names the package's public surface. It's the set of names that `from modules_packaging.shapes import *` would pull in. It's documentation you can assert on, which we'll do shortly.

And every folder in the chain needs an `__init__.py`, including `modules_packaging/__init__.py` itself, or Python won't treat the folder as a package you can import from with a dot.

Run `uv run pytest`:

```
    def test_square_area():
>       assert square_area(3) == 9
E       assert 0.0 == 9
E        +  where 0.0 = square_area(3)
```

The import resolved this time. We've gone from "name doesn't exist" to "name exists but returns the wrong number", which is exactly the progress we want.

## Write enough code to make it pass

A square's area is the side squared. Fill in `square.py`:

```python
from __future__ import annotations


def area(side: float) -> float:
    return side * side
```

Run the tests and `test_square_area` is green. We changed `square.py`, and the `as square_area` rename in `__init__.py` carried the fix through without us touching it.

## Refactor

There's nothing to tidy in a one-line function, but it's worth naming the shape of what we built. We have a *package* (`shapes`), a *module* inside it (`square`), and a *public name* (`square_area`) that the package chose to expose. The caller never reaches into `square.py` directly. That indirection is the whole point of `__init__.py`: it lets you rearrange the modules behind a stable public API. Re-run the tests to confirm nothing moved.

## Repeat for new requirements

One shape is lonely. Let's add circles, and while we're here, let's pin down what the package promises with `__all__`.

### Write the test first

Add two tests. One checks the circle area, one asserts that the package re-exports exactly the names we expect, pulled from the package object itself rather than the submodules:

```python
import math

from . import shapes
from .shapes import circle_area, square_area


def test_circle_area():
    assert circle_area(2) == math.pi * 4


def test_package_init_reexports():
    # The names come from the package itself, not the submodules.
    assert shapes.circle_area is circle_area
    assert shapes.square_area is square_area


def test_all_lists_the_public_names():
    assert shapes.__all__ == ["circle_area", "square_area"]
```

`from . import shapes` imports the package as an object, so we can poke at `shapes.__all__` and `shapes.circle_area`. That's a different flavour of import from `from .shapes import circle_area`, which binds the name straight into our namespace. Both reach the same package, they just hand you different things.

### Try to run the test

Run `uv run pytest`. The package's `__init__.py` is about to try importing `circle_area`, and `circle.py` is still empty:

```
ImportError: cannot import name 'area' from 'modules_packaging.shapes.circle' (/Users/soar/src/python-with-tests/modules_packaging/shapes/circle.py)
```

Same failure mode as before, one shape over. The whole test module fails to collect, because the broken import is at the top of the file and nothing past it can run.

### Write the minimal amount of code for the test to run and check the failing test output

Give `circle.py` an `area` that's wrong on purpose, and wire it into the package's `__init__.py`:

`modules_packaging/shapes/circle.py`:

```python
from __future__ import annotations


def area(radius: float) -> float:
    return 0.0
```

`modules_packaging/shapes/__init__.py`:

```python
"""A tiny sub-package of area helpers, one shape per module."""

from .circle import area as circle_area
from .square import area as square_area

__all__ = ["circle_area", "square_area"]
```

Run `uv run pytest`:

```
    def test_circle_area():
>       assert circle_area(2) == math.pi * 4
E       assert 0.0 == 12.566370614359172
E        +  where 0.0 = circle_area(2)
```

The import resolves, `test_package_init_reexports` and `test_all_lists_the_public_names` already pass (the wiring and the `__all__` list are correct), and only the value is wrong. Good.

### Write enough code to make it pass

A circle's area is pi times the radius squared. The `math` module is in the standard library, so we import it at the top of `circle.py`:

```python
from __future__ import annotations

import math


def area(radius: float) -> float:
    return math.pi * radius * radius
```

Run the tests. All green. Notice `circle.py` imports `math` (an *absolute* import of a top-level stdlib module) while `__init__.py` imports `.circle` (a *relative* import of a sibling in the same package). **Use relative imports for modules inside your own package, absolute imports for everything else.** It keeps the package movable: rename the `shapes` folder and the relative imports still resolve.

### Refactor

Nothing to refactor in the functions, but look at what `__all__` is doing now. It lists `circle_area` and `square_area` in the order a reader should think about them, and `test_all_lists_the_public_names` will fail the moment someone adds a name to the package and forgets to list it. That test turns "keep `__all__` honest" from a code-review nag into a red bar. Re-run the tests.

## Repeat for new requirements

Now let's use the package from a flat module next door. We'll write `modules_packaging/geometry.py` with a `describe` function, plus the `if __name__ == "__main__"` block that lets the same file double as a script.

### Write the test first

```python
from .geometry import describe


def test_describe_circle():
    assert describe("circle", 1) == "circle r=1 area=3.14"


def test_describe_square():
    assert describe("square", 2) == "square s=2 area=4.00"


def test_describe_unknown_shape_raises():
    try:
        describe("triangle", 1)
    except ValueError as err:
        assert "triangle" in str(err)
    else:
        raise AssertionError("expected a ValueError")
```

`describe` formats an area to two decimal places and refuses shapes it doesn't know about.

### Try to run the test

Run `uv run pytest`. There's no `geometry.py` yet, so the import fails at the top of the test file:

```
ImportError: cannot import name 'describe' from 'modules_packaging.geometry' (/Users/soar/src/python-with-tests/modules_packaging/geometry.py)
```

The module is missing entirely. Same lesson as the first cycle: the import is the canary.

### Write the minimal amount of code for the test to run and check the failing test output

Stub `geometry.py` so it imports cleanly but returns the wrong string:

```python
from __future__ import annotations

from .shapes import circle_area, square_area


def describe(shape: str, size: float) -> str:
    return ""
```

We import `circle_area` and `square_area` from our own package with a relative import, the same way the tests do. Run `uv run pytest`:

```
    def test_describe_square():
>       assert describe("square", 2) == "square s=2 area=4.00"
E       AssertionError: assert '' == 'square s=2 area=4.00'
```

Running and failing on the value. The `unknown_shape` test also fails, because an empty string is not a raised `ValueError`, which is the reminder that a stub returning `""` says nothing yet about the error path.

### Write enough code to make it pass

Format each known shape and raise on the rest:

```python
from __future__ import annotations

from .shapes import circle_area, square_area


def describe(shape: str, size: float) -> str:
    if shape == "circle":
        return f"circle r={size} area={circle_area(size):.2f}"
    if shape == "square":
        return f"square s={size} area={square_area(size):.2f}"
    raise ValueError(f"unknown shape: {shape!r}")
```

Green. `geometry` leans on the `shapes` package and never touches `circle.py` or `square.py` directly, it only knows the two public names the package exposed.

### Refactor

Now add the part that makes a module also a script. At the bottom of `geometry.py`:

```python
def main() -> None:
    print(describe("circle", 1))
    print(describe("square", 2))


if __name__ == "__main__":
    main()
```

When you run `uv run python -m modules_packaging.geometry`, Python sets that file's `__name__` to the string `"__main__"`, so the guard is true and `main()` runs:

```
circle r=1 area=3.14
square s=2 area=4.00
```

When the test imports `geometry` instead, `__name__` is `"modules_packaging.geometry"`, the guard is false, and `main()` stays quiet. **The `if __name__ == "__main__"` guard is how one file is both an importable module and a runnable script without the import triggering the script.** Re-run the tests, still green, because importing the module no longer prints anything.

## Repeat for new requirements

Last cycle. Let's add a `total_area` that sums a list of shapes, so the package gets exercised in a loop rather than one call at a time.

### Write the test first

```python
from .geometry import describe, total_area


def test_total_area_sums_each_shape():
    shapes_in = [("square", 2), ("square", 3)]
    assert total_area(shapes_in) == 13


def test_total_area_empty_is_zero():
    assert total_area([]) == 0
```

Two squares of side 2 and 3 give 4 plus 9, which is 13. An empty list is zero, the natural base case.

### Try to run the test

Run `uv run pytest`. `total_area` isn't in `geometry.py` yet, so the import line that now asks for it fails:

```
ImportError: cannot import name 'total_area' from 'modules_packaging.geometry'
```

### Write the minimal amount of code for the test to run and check the failing test output

Add a stub that returns the wrong number:

```python
def total_area(shapes: list[tuple[str, float]]) -> float:
    return 0.0
```

Run `uv run pytest`:

```
    def test_total_area_sums_each_shape():
        shapes_in = [("square", 2), ("square", 3)]
>       assert total_area(shapes_in) == 13
E       AssertionError: assert 0.0 == 13
E        +  where 0.0 = total_area([('square', 2), ('square', 3)])
```

`test_total_area_empty_is_zero` happens to pass, because an empty list really should sum to `0.0` and that's what the stub hands back. One accidentally-green test proves nothing on its own, which is why we wrote the summing test too.

### Write enough code to make it pass

Map each shape name to its area function and add them up:

```python
def total_area(shapes: list[tuple[str, float]]) -> float:
    funcs = {"circle": circle_area, "square": square_area}
    total = 0.0
    for shape, size in shapes:
        if shape not in funcs:
            raise ValueError(f"unknown shape: {shape!r}")
        total += funcs[shape](size)
    return total
```

Green. We reuse the same `circle_area` and `square_area` we imported at the top of the file, so there's still exactly one import of the `shapes` package serving the whole module.

### Refactor

The dispatch dict `{"circle": circle_area, "square": square_area}` is rebuilt on every call, which is wasteful and also duplicates the knowledge that `describe` encodes as two `if` branches. I'll leave it as is for this chapter, because pulling it up to a module-level constant is a refactor about this one function, not about packaging, and I don't want to muddy the lesson. Worth knowing the seam is there. Re-run the tests one last time: all green.

## Wrapping up

- **A module is a file, a package is a folder with an `__init__.py`.** Every folder in the import chain needs one.
- **`__init__.py` runs on first import**, so it's where a package picks its public names. We re-exported `circle_area` and `square_area` there with `as`.
- **`__all__` declares the public surface** and is something a test can assert on, so adding a name and forgetting to list it turns into a red bar.
- **Relative imports (`from .square import area`) for siblings in your own package, absolute imports for the standard library.** Relative imports keep the package movable.
- **The `if __name__ == "__main__"` guard** lets one file be both an importable module and a runnable script. Imports see the module name, `python -m` sees `"__main__"`.
