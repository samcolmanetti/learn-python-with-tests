from __future__ import annotations


def is_valid(s: str) -> bool:
    """Return ``True`` if every bracket in ``s`` is closed by the right type in the right order."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack
