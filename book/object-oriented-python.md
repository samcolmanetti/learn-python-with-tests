# Object-oriented Python

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/oop)**

We're going to build a tiny hierarchy of shapes (a `Circle` and a `Rectangle` that share a base
`Shape`) and use it to meet the bits of OOP you actually reach for in an interview: inheritance,
`super()`, the dunder methods `__repr__`, `__eq__` and `__lt__`, `@property`, and the
`classmethod`/`staticmethod` pair. Each one earns its place by making a failing test pass.

## Write the test first

Start with the smallest real behaviour: a circle knows its area, and so does a rectangle. Create
`oop/test_shapes.py`.

```python
import math

from shapes import Circle, Rectangle


def test_circle_area():
    assert math.isclose(Circle(2).area, math.pi * 4)


def test_rectangle_area():
    assert Rectangle(3, 4).area == 12
```

A circle of radius 2 has area `pi * 4`, and floats never compare exactly, so we lean on
`math.isclose` rather than `==`. A 3 by 4 rectangle has area 12, which is an integer, so that one
can use `==`.

Notice `Circle(2).area` is read like an attribute, not called like `Circle(2).area()`. That's
deliberate, and we'll see why in a moment.

## Try to run the test

There's no `oop/shapes.py` yet, so `uv run pytest` can't even import the names:

```
ImportError: cannot import name 'Circle' from 'oop.shapes'
```

The import is the first thing to break. Listen to it: it's telling us exactly which names to
define.

## Write the minimal amount of code for the test to run and check the failing test output

Create `oop/shapes.py` with both classes, but have `area` lie and return `0`. We want the test to
*run* and fail on the value, which proves it's checking what we think.

```python
from __future__ import annotations


class Shape:
    def __init__(self, name):
        self.name = name


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("circle")
        self.radius = radius

    @property
    def area(self):
        return 0


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("rectangle")
        self.width = width
        self.height = height

    @property
    def area(self):
        return 0
```

Two things are already doing real work here. `class Circle(Shape)` means `Circle` *inherits* from
`Shape`, so a circle is a shape. And `super().__init__("circle")` calls the base class's
`__init__` to set `self.name`, instead of repeating that line in every subclass. That's `super()`:
it hands work up to the parent.

The `@property` is why we wrote `.area` and not `.area()`. **A `@property` turns a method into a
read-only attribute**, computed on access. The caller treats `area` like data, but we get to run
code behind it.

Run `uv run pytest`:

```
    def test_circle_area():
>       assert math.isclose(Circle(2).area, math.pi * 4)
E       assert False
E        +  where False = <built-in function isclose>(0, (3.141592653589793 * 4))

    def test_rectangle_area():
>       assert Rectangle(3, 4).area == 12
E       assert 0 == 12
E        +  where 0 = <oop.shapes.Rectangle object at 0x1083d3520>.area
```

Both fail on the value, `0`, not on a missing name. That's the failure we wanted.

## Write enough code to make it pass

Now compute the real areas. A circle is `pi * r^2`, a rectangle is `width * height`.

```python
from __future__ import annotations

import math


class Shape:
    def __init__(self, name: str) -> None:
        self.name = name


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        super().__init__("circle")
        self.radius = radius

    @property
    def area(self) -> float:
        return math.pi * self.radius**2


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        super().__init__("rectangle")
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        return self.width * self.height
```

The tests pass.

## Refactor

The base `Shape` carries a `name` but says nothing about `area`, even though every subclass has
one. That's a gap: someone could write `Shape("blob").area` and get a confusing `AttributeError`
about a missing attribute, rather than a clear "you forgot to implement this".

Let me make the base class state the contract out loud. Give `Shape` an `area` property that
refuses to guess.

```python
class Shape:
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def area(self) -> float:
        raise NotImplementedError("subclasses must define area")
```

`NotImplementedError` is the conventional way to say **this method is abstract: a subclass must
override it**. The subclasses already do, so they're unaffected. Let me pin this down with a test
so the contract doesn't quietly rot.

```python
import pytest

from shapes import Circle, Rectangle, Shape


def test_base_shape_has_no_area():
    with pytest.raises(NotImplementedError):
        _ = Shape("nothing").area
```

We assign to `_` because reading `.area` is the thing under test, and the throwaway name keeps the
linter from complaining about a useless expression. Re-run the tests and everything's still green.

## Repeat for new requirements

A shape hierarchy earns its keep when you can treat a mixed pile of shapes uniformly. Our next
requirement: sum the area of a list of shapes without caring which kind each one is.

### Write the test first

```python
def test_total_area_is_polymorphic():
    shapes = [Circle(1), Rectangle(2, 3), Rectangle(1, 1)]
    expected = math.pi + 6 + 1
    assert math.isclose(total_area(shapes), expected)
```

Add `total_area` to the import line:

```python
from shapes import Circle, Rectangle, Shape, total_area
```

### Try to run the test

```
ImportError: cannot import name 'total_area' from 'oop.shapes'
```

No `total_area` yet, so the import breaks again.

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
def total_area(shapes):
    return 0
```

Run `uv run pytest`:

```
    def test_total_area_is_polymorphic():
        shapes = [Circle(1), Rectangle(2, 3), Rectangle(1, 1)]
        expected = math.pi + 6 + 1
>       assert math.isclose(total_area(shapes), expected)
E       assert False
E        +  where False = <built-in function isclose>(0, 10.141592653589793)
```

Fails on the value. Good.

### Write enough code to make it pass

```python
def total_area(shapes: list[Shape]) -> float:
    return sum(shape.area for shape in shapes)
```

Green.

This is *polymorphism*, and it's the whole reason the hierarchy exists. `total_area` calls
`shape.area` on each element and never asks "are you a circle or a rectangle?". Each object answers
for itself. **Add a `Triangle` tomorrow and `total_area` keeps working untouched**, as long as the
triangle is a `Shape` with an `area`.

### Refactor

Nothing to tidy in a one-line generator. The point was the design, not the code.

## Repeat for new requirements: a readable shape

Print a shape and you get the default `<oop.shapes.Rectangle object at 0x...>`, which tells you
nothing useful in a test failure or a debugger. Let's fix how a shape shows itself.

### Write the test first

```python
def test_repr_uses_subclass_name():
    assert repr(Rectangle(3, 4)) == "Rectangle(area=12.00)"
    assert repr(Circle(1)) == "Circle(area=3.14)"
```

### Try to run the test

```
    def test_repr_uses_subclass_name():
>       assert repr(Rectangle(3, 4)) == "Rectangle(area=12.00)"
E       AssertionError: assert '<oop.shapes.... 0x107d13670>' == 'Rectangle(area=12.00)'
E         - Rectangle(area=12.00)
E         + <oop.shapes.Rectangle object at 0x107d13670>
```

The default `repr` is the memory-address noise on the bottom line. We want the top line.

### Write the minimal amount of code for the test to run and check the failing test output

We can't easily stub this one "wrong but running", because the default `repr` already runs, so the
test above *is* the failing-for-the-right-reason output. Onward.

### Write enough code to make it pass

Define `__repr__` once on the base class, and let every subclass inherit it.

```python
def __repr__(self) -> str:
    return f"{type(self).__name__}(area={self.area:.2f})"
```

The tests pass.

`__repr__` is a *dunder* (double-underscore) method: Python calls it for you when something needs
the object's representation. The clever bit is `type(self).__name__`, which is `"Rectangle"` for a
rectangle and `"Circle"` for a circle, even though the method lives on `Shape`. **Write the dunder
once on the base, and `type(self)` makes it report the real subclass**. That's inheritance and
polymorphism working together.

### Refactor

One line, defined in the right place. Leave it.

## Repeat for new requirements: equal shapes

Two shapes with the same area should compare equal, regardless of kind. A 1 by 1 square and a
circle of area 1 are, for our purposes, the same size.

### Write the test first

```python
def test_equality_compares_area_across_subclasses():
    same_area_radius = math.sqrt(1 / math.pi)
    assert Rectangle(1, 1) == Circle(same_area_radius)


def test_equality_against_non_shape_is_false():
    assert (Rectangle(1, 1) == "rectangle") is False
```

The second test is the one people forget: comparing a shape to a string shouldn't blow up, it
should just be `False`.

### Try to run the test

```
    def test_equality_compares_area_across_subclasses():
        same_area_radius = math.sqrt(1 / math.pi)
>       assert Rectangle(1, 1) == Circle(same_area_radius)
E       assert Rectangle(area=1.00) == Circle(area=1.00)
```

Look closely: the failure message reads `Rectangle(area=1.00) == Circle(area=1.00)`, which *looks*
like two equal things. (That tidy `repr` we just wrote is paying off already.) **By default `==`
on a custom object means identity: same object in memory.** Two different objects are never equal,
no matter how alike they look.

### Write the minimal amount of code for the test to run and check the failing test output

The default `__eq__` is already running and giving us the failure above, so this step has nothing
to stub. Straight to the implementation.

### Write enough code to make it pass

Define `__eq__` on the base, comparing areas. Return the `NotImplemented` singleton (not `False`)
when the other thing isn't a shape, which tells Python to try the other operand's `__eq__` before
giving up.

```python
def __eq__(self, other: object) -> bool:
    if not isinstance(other, Shape):
        return NotImplemented
    return math.isclose(self.area, other.area)
```

Both tests pass: the two equal-area shapes compare equal, and `Rectangle(1, 1) == "rectangle"`
comes back `False` because Python falls back to identity once both sides return `NotImplemented`.

**Returning `NotImplemented` rather than `False` is the correct way to say "I can't compare
these".** It's a subtle one, and it's exactly the kind of detail an interviewer pokes at.

### Refactor

Nothing to clean. Note we used `math.isclose` again, for the same float reason as the area tests.

## Repeat for new requirements: sorting shapes by area

The headline act: sort a mixed list of shapes from smallest to largest. This is where `__lt__`
("less than") comes in, because `sorted` orders things by asking `a < b`.

### Write the test first

```python
def test_shapes_sort_by_area():
    shapes = [Rectangle(3, 4), Circle(1), Rectangle(1, 1)]
    ordered = sorted(shapes)
    assert [round(shape.area, 2) for shape in ordered] == [1.0, 3.14, 12.0]
```

### Try to run the test

```
    def test_shapes_sort_by_area():
        shapes = [Rectangle(3, 4), Circle(1), Rectangle(1, 1)]
>       ordered = sorted(shapes)
E       TypeError: '<' not supported between instances of 'Circle' and 'Rectangle'
```

`sorted` reached for `<` between a `Circle` and a `Rectangle` and found nothing. **You can't sort
objects Python doesn't know how to order.**

### Write the minimal amount of code for the test to run and check the failing test output

The `TypeError` above is already the right failure: it fails because `__lt__` is missing, which is
precisely what we're about to add. No stub needed.

### Write enough code to make it pass

Add `__lt__` to the base, comparing areas, again returning `NotImplemented` for a non-shape.

```python
def __lt__(self, other: object) -> bool:
    if not isinstance(other, Shape):
        return NotImplemented
    return self.area < other.area
```

The tests pass, and the shapes come out smallest first.

We only defined `<`. That's enough for `sorted`, because sorting only ever needs `<`. But a reader
who tries `circle > rectangle` would hit the same `TypeError` we just saw, because `>` is a
separate dunder (`__gt__`).

### Refactor

Rather than hand-write `__gt__`, `__le__` and `__ge__` to round out the ordering, lean on the
standard library. `functools.total_ordering` is a class decorator that **fills in the rest of the
comparison operators from just `__eq__` and `__lt__`**. We already have both.

```python
from functools import total_ordering


@total_ordering
class Shape:
    ...
```

Now add one test to prove the extra operator showed up for free:

```python
def test_total_ordering_gives_us_greater_than():
    assert Rectangle(3, 4) > Circle(1)
```

Re-run the tests. The sort still works, and `>` now works too, without us writing it. That's the
trade `total_ordering` makes: one decorator, less code, in exchange for a small speed cost it
warns about in the docs but that never matters at interview scale.

## Repeat for new requirements: alternate constructors and helpers

Last stop. A square is just a rectangle with equal sides, and "is this a valid rectangle?" is a
question about two numbers that needs no rectangle at all. These map to the two method decorators
people mix up: `classmethod` and `staticmethod`.

### Write the test first

```python
def test_square_classmethod_builds_a_rectangle():
    sq = Rectangle.square(5)
    assert isinstance(sq, Rectangle)
    assert sq.area == 25


def test_is_valid_staticmethod():
    assert Rectangle.is_valid(2, 3) is True
    assert Rectangle.is_valid(0, 3) is False
    assert Rectangle.is_valid(2, -1) is False
```

We call both on the class itself (`Rectangle.square`, `Rectangle.is_valid`), never on an instance.

### Try to run the test

```
    def test_square_classmethod_builds_a_rectangle():
>       sq = Rectangle.square(5)
E       AttributeError: type object 'Rectangle' has no attribute 'square'

    def test_is_valid_staticmethod():
>       assert Rectangle.is_valid(2, 3) is True
E       AttributeError: type object 'Rectangle' has no attribute 'is_valid'
```

Neither exists yet, so both fail on the missing attribute.

### Write the minimal amount of code for the test to run and check the failing test output

Add stubs that exist but return the wrong thing, so the tests run and fail on the value:

```python
@classmethod
def square(cls, side):
    return cls(0, 0)

@staticmethod
def is_valid(width, height):
    return False
```

Run `uv run pytest`:

```
    def test_square_classmethod_builds_a_rectangle():
        sq = Rectangle.square(5)
        assert isinstance(sq, Rectangle)
>       assert sq.area == 25
E       assert 0 == 25

    def test_is_valid_staticmethod():
>       assert Rectangle.is_valid(2, 3) is True
E       assert False is True
```

Now they fail on the values, not on missing names. The `square` stub already proves something
useful: it returns a real `Rectangle` (so `isinstance` passes), just the wrong one.

### Write enough code to make it pass

```python
@classmethod
def square(cls, side: float) -> Rectangle:
    return cls(side, side)

@staticmethod
def is_valid(width: float, height: float) -> bool:
    return width > 0 and height > 0
```

The tests pass.

Here's the distinction worth memorising. **A `classmethod` receives the class as its first
argument (`cls`) and is the Python idiom for an alternate constructor**: `square` builds and
returns a `Rectangle`. **A `staticmethod` receives neither `self` nor `cls`**: `is_valid` is just
a plain function that lives in the class's namespace because it logically belongs there.

Using `cls(side, side)` rather than `Rectangle(side, side)` is the better habit. If someone
subclassed `Rectangle`, calling `square` on that subclass would build the subclass, because `cls`
is whatever class the method was called on.

### Refactor

The implementations are already as small as they get. The only tidy-up is the type hints, which
the snippets above already include. Run the full file one last time with `uv run pytest` and watch
all eleven tests pass.

## Wrapping up

* **Inheritance and `super()`**: `class Circle(Shape)` makes a circle a shape, and
  `super().__init__(...)` runs the parent's setup instead of copying it.
* **`@property`** turns a computed method into a read-only attribute, so `shape.area` reads like
  data.
* **Polymorphism**: code that calls `.area` on any `Shape` works for every subclass, present and
  future, without a single `if isinstance` check.
* **Dunders**: `__repr__` for a readable object, `__eq__` for value equality (return
  `NotImplemented`, not `False`, for foreign types), and `__lt__` so `sorted` can order your
  objects.
* **`functools.total_ordering`** fills in the rest of the comparison operators from `__eq__` and
  `__lt__`.
* **`classmethod` vs `staticmethod`**: `cls` for alternate constructors, neither for a plain
  helper that just belongs in the namespace.
