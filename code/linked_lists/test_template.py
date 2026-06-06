from ._template import ListNode, build_list, to_list


def test_build_then_to_list_round_trips():
    assert to_list(build_list([1, 2, 3])) == [1, 2, 3]


def test_build_empty_is_none():
    assert build_list([]) is None


def test_to_list_of_none_is_empty():
    assert to_list(None) == []


def test_node_links_in_order():
    head = build_list([7, 8])
    assert head.val == 7
    assert head.next.val == 8
    assert head.next.next is None


def test_single_node_repr():
    assert repr(ListNode(5)) == "ListNode(5)"
