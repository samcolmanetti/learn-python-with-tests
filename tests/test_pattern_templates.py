"""Tests for the reusable interview-pattern templates (`*/_template.py`).

Two layers:

1. **Importability**, every ``_template.py`` must import cleanly (no syntax errors, no
   top-level side effects). This is the guardrail CONTRIBUTING.md promises.
2. **Behaviour**, the templates are real, working Python, not pseudo-code, so we exercise
   each one on a small example. If a template breaks, these fail loudly.
"""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_FILES = sorted(REPO_ROOT.glob("*/_template.py"))


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.parent.name + "_template", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def test_there_are_templates():
    assert TEMPLATE_FILES, "expected at least one */_template.py pattern template"


@pytest.mark.parametrize("path", TEMPLATE_FILES, ids=lambda p: p.parent.name)
def test_template_imports_cleanly(path):
    module = _load(path)
    assert module is not None


# ----- behaviour: each template does what it claims on a small example -----------------


def test_binary_search_template():
    m = _load(REPO_ROOT / "binary_search/_template.py")
    assert m.binary_search([1, 3, 5, 7, 9], 7) == 3
    assert m.binary_search([1, 3, 5, 7, 9], 8) == -1
    assert m.find_first_true(0, 9, lambda x: x >= 4) == 4


def test_two_pointers_template():
    m = _load(REPO_ROOT / "two_pointers/_template.py")
    data = [0, 1, 0, 3, 0, 2]
    length = m.two_pointers_same(data, lambda x: x != 0)
    assert data[:length] == [1, 3, 2]


def test_sliding_window_template():
    m = _load(REPO_ROOT / "sliding_window/_template.py")
    assert m.fixed_window_max_sum([1, 4, 2, 10, 2, 3], 3) == 16  # best window [4, 2, 10]
    with pytest.raises(ValueError):
        m.fixed_window_max_sum([1, 2], 5)


def test_prefix_sum_template():
    m = _load(REPO_ROOT / "prefix_sum/_template.py")
    prefix = m.build_prefix([2, 4, 6, 8])
    assert m.range_sum(prefix, 1, 2) == 10  # 4 + 6
    assert m.range_sum(prefix, 0, 3) == 20


def test_mono_stack_template():
    m = _load(REPO_ROOT / "stack_and_monotonic_stack/_template.py")
    assert m.next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]


def test_trees_dfs_template():
    m = _load(REPO_ROOT / "trees_dfs/_template.py")
    root = m.TreeNode(1, m.TreeNode(2, m.TreeNode(4)), m.TreeNode(3))
    assert m.max_depth(root) == 3
    assert m.dfs_search(root, 4).val == 4
    assert m.dfs_search(root, 99) is None


def test_trees_bfs_template():
    dfs = _load(REPO_ROOT / "trees_dfs/_template.py")
    bfs = _load(REPO_ROOT / "trees_bfs/_template.py")
    root = dfs.TreeNode(1, dfs.TreeNode(2, dfs.TreeNode(4)), dfs.TreeNode(3))
    assert bfs.level_order(root) == [[1], [2, 3], [4]]
    assert bfs.level_order(None) == []


def test_graphs_traversal_template():
    m = _load(REPO_ROOT / "graphs_traversal/_template.py")
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    assert m.bfs(graph, "a") == ["a", "b", "c", "d"]
    assert set(m.dfs(graph, "a")) == {"a", "b", "c", "d"}
    grid = [[0, 0], [0, 0]]
    assert set(m.grid_neighbors(grid, 0, 0)) == {(0, 1), (1, 0)}


def test_topological_sort_template():
    m = _load(REPO_ROOT / "topological_sort/_template.py")
    order = m.topo_sort({"shirt": ["tie"], "tie": ["jacket"], "jacket": []})
    assert order.index("shirt") < order.index("tie") < order.index("jacket")
    assert m.topo_sort({"a": ["b"], "b": ["a"]}) is None  # cycle


def test_union_find_template():
    m = _load(REPO_ROOT / "union_find/_template.py")
    uf = m.UnionFind()
    assert uf.union(1, 2) is True
    assert uf.union(2, 3) is True
    assert uf.union(1, 3) is False  # already connected
    assert uf.connected(1, 3) is True
    assert uf.connected(1, 4) is False


def test_backtracking_template():
    m = _load(REPO_ROOT / "backtracking/_template.py")
    subs = m.subsets([1, 2, 3])
    assert len(subs) == 8 and [] in subs and [1, 2, 3] in subs
    perms = m.permutations([1, 2, 3])
    assert len(perms) == 6 and [3, 2, 1] in perms


def test_trie_template():
    m = _load(REPO_ROOT / "trie/_template.py")
    trie = m.Trie()
    trie.insert("cat")
    assert trie.search("cat") is True
    assert trie.search("ca") is False
    assert trie.starts_with("ca") is True
    assert trie.starts_with("dog") is False
