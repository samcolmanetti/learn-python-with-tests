"""A tiny sub-package of area helpers, one shape per module."""

from .circle import area as circle_area
from .square import area as square_area

__all__ = ["circle_area", "square_area"]
