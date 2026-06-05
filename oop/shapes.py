"""A small Shape hierarchy that exercises the parts of OOP you actually reach for.

``Shape`` is the base class. ``Circle`` and ``Rectangle`` subclass it and each define their own
``area``. The base also gives every shape a name, a useful ``__repr__``, value equality via
``__eq__``, and an ordering by area via ``__lt__`` so a list of mixed shapes sorts cleanly.
"""

from __future__ import annotations

import math
from functools import total_ordering


@total_ordering
class Shape:
    """Base class for a 2D shape with a name and an area.

    ``area`` is the one thing every subclass must answer for itself, so the base raises
    ``NotImplementedError`` rather than guessing. Everything else (repr, equality, ordering)
    is shared and works for any subclass that fills in ``area``.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def area(self) -> float:
        raise NotImplementedError("subclasses must define area")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(area={self.area:.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return math.isclose(self.area, other.area)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area < other.area


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

    @classmethod
    def square(cls, side: float) -> Rectangle:
        """Build a square as the special case of a rectangle (an alternate constructor)."""
        return cls(side, side)

    @staticmethod
    def is_valid(width: float, height: float) -> bool:
        """A rectangle needs two positive sides. No ``self``, no ``cls``: it's just a helper."""
        return width > 0 and height > 0


def total_area(shapes: list[Shape]) -> float:
    """Sum the areas of any mix of shapes. This is polymorphism: we call ``.area`` on each
    without caring which subclass it is."""
    return sum(shape.area for shape in shapes)
