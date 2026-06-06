from __future__ import annotations

from .shapes import circle_area, square_area


def describe(shape: str, size: float) -> str:
    if shape == "circle":
        return f"circle r={size} area={circle_area(size):.2f}"
    if shape == "square":
        return f"square s={size} area={square_area(size):.2f}"
    raise ValueError(f"unknown shape: {shape!r}")


def total_area(shapes: list[tuple[str, float]]) -> float:
    funcs = {"circle": circle_area, "square": square_area}
    total = 0.0
    for shape, size in shapes:
        if shape not in funcs:
            raise ValueError(f"unknown shape: {shape!r}")
        total += funcs[shape](size)
    return total


def main() -> None:
    print(describe("circle", 1))
    print(describe("square", 2))


if __name__ == "__main__":
    main()
