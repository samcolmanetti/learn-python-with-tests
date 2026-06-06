import math

import pytest
from shapes import Circle, Rectangle, Shape, total_area


def test_circle_area():
    assert math.isclose(Circle(2).area, math.pi * 4)


def test_rectangle_area():
    assert Rectangle(3, 4).area == 12


def test_base_shape_has_no_area():
    with pytest.raises(NotImplementedError):
        _ = Shape("nothing").area


def test_total_area_is_polymorphic():
    shapes = [Circle(1), Rectangle(2, 3), Rectangle(1, 1)]
    expected = math.pi + 6 + 1
    assert math.isclose(total_area(shapes), expected)


def test_repr_uses_subclass_name():
    assert repr(Rectangle(3, 4)) == "Rectangle(area=12.00)"
    assert repr(Circle(1)) == "Circle(area=3.14)"


def test_equality_compares_area_across_subclasses():
    # A 1x1 rectangle and a circle of the same area are equal by our rule.
    same_area_radius = math.sqrt(1 / math.pi)
    assert Rectangle(1, 1) == Circle(same_area_radius)


def test_equality_against_non_shape_is_false():
    assert (Rectangle(1, 1) == "rectangle") is False


def test_shapes_sort_by_area():
    shapes = [Rectangle(3, 4), Circle(1), Rectangle(1, 1)]
    ordered = sorted(shapes)
    assert [round(shape.area, 2) for shape in ordered] == [1.0, 3.14, 12.0]


def test_total_ordering_gives_us_greater_than():
    assert Rectangle(3, 4) > Circle(1)


def test_square_classmethod_builds_a_rectangle():
    sq = Rectangle.square(5)
    assert isinstance(sq, Rectangle)
    assert sq.area == 25


def test_is_valid_staticmethod():
    assert Rectangle.is_valid(2, 3) is True
    assert Rectangle.is_valid(0, 3) is False
    assert Rectangle.is_valid(2, -1) is False
