from .._template import build_list
from .has_cycle import has_cycle


def link_into_cycle(values, pos):
    """Build a list from ``values``, then point the last node at index ``pos`` (-1 for none)."""
    head = build_list(values)
    if head is None:
        return None
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return head


def test_no_cycle_is_false():
    assert has_cycle(link_into_cycle([1, 2, 3, 4], -1)) is False


def test_tail_back_to_middle_is_true():
    assert has_cycle(link_into_cycle([3, 2, 0, -4], 1)) is True


def test_two_node_self_loop_is_true():
    assert has_cycle(link_into_cycle([1, 2], 0)) is True


def test_single_node_no_cycle_is_false():
    assert has_cycle(link_into_cycle([1], -1)) is False


def test_empty_list_is_false():
    assert has_cycle(build_list([])) is False
