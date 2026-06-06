import math

from . import shapes
from .geometry import describe, total_area
from .shapes import circle_area, square_area


def test_square_area():
    assert square_area(3) == 9


def test_circle_area():
    assert circle_area(2) == math.pi * 4


def test_package_init_reexports():
    # The names come from the package itself, not the submodules.
    assert shapes.circle_area is circle_area
    assert shapes.square_area is square_area


def test_all_lists_the_public_names():
    assert shapes.__all__ == ["circle_area", "square_area"]


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


def test_total_area_sums_each_shape():
    shapes_in = [("square", 2), ("square", 3)]
    assert total_area(shapes_in) == 13


def test_total_area_empty_is_zero():
    assert total_area([]) == 0
