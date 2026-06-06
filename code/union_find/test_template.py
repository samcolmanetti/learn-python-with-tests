from ._template import UnionFind


def test_new_elements_start_disconnected():
    uf = UnionFind()
    assert uf.connected("a", "b") is False


def test_union_connects():
    uf = UnionFind()
    uf.union("a", "b")
    assert uf.connected("a", "b") is True


def test_union_is_transitive():
    uf = UnionFind()
    uf.union(1, 2)
    uf.union(2, 3)
    assert uf.connected(1, 3) is True


def test_union_returns_true_on_real_merge_false_when_already_joined():
    uf = UnionFind()
    assert uf.union(1, 2) is True
    assert uf.union(1, 2) is False


def test_count_tracks_disjoint_sets():
    uf = UnionFind()
    uf.find(1)
    uf.find(2)
    uf.find(3)
    assert uf.count == 3
    uf.union(1, 2)
    assert uf.count == 2
