# Trie

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/trie)**

A trie (say it "try", it's short for re*trie*val) is a tree keyed by character: words that share a
prefix share a path. It's an **interview pattern**, so we keep a reusable [`trie/_template.py`](trie/_template.py)
and build worked problems on top of it in `trie/solutions/`, each one test-first.

## When to reach for a trie

The signal is a problem about *strings sharing prefixes*, asked more than once. A hash set answers
"is this exact word here?" in one shot, but it can't tell you "does any stored word start with
`app`?" without scanning everything. A trie can, because the prefix is a literal walk down the tree.

Reach for a trie when:

- You need **prefix queries**: autocomplete, "does any word start with this", "replace each word
  with its shortest stored prefix".
- You're matching words with **wildcards** or doing a **word search** where you want to abandon a
  path the instant its prefix stops matching anything.
- You have **many words and many lookups**, and each lookup is O(length of the word), independent
  of how many words you've stored.

The cost is memory: a node per character per distinct prefix. You trade space for the ability to
walk prefixes directly.

## The template

Here's the whole skeleton from [`trie/_template.py`](trie/_template.py).

```python
from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict = {}
        self.is_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """Whether the exact ``word`` was inserted."""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Whether any inserted word starts with ``prefix``."""
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
```

Two ideas carry the whole pattern.

The first is the node: a `dict` from the next character to a child `TrieNode`, plus an `is_word`
flag. The flag is the part people forget. Without it you can't tell a *stored word* from a *prefix
of a stored word*. Insert `apple` and the node at `app` exists, but `is_word` is `False` there, so
`search("app")` correctly says no while `starts_with("app")` says yes.

The second is `insert`: `setdefault(ch, TrieNode())` walks down, creating a child only when the
character isn't already there, so words that share a prefix share those nodes. That shared path is
the entire reason the structure is fast. `_walk` is the read side: follow the characters, return
the node you land on, or `None` the moment a character is missing.

**The invariant the template maintains: the node you reach by spelling out `s` from the root
represents exactly the prefix `s`, and its `is_word` flag says whether `s` is itself a stored
word.** Every problem below is a different way of reading that walk.

## Problem 1: Add and Search Word with wildcards

> Build a `WordDictionary` with `add_word(word)` and `search(word)`. In `search`, a `.` matches any
> single letter. `search("b.d")` should find `bad`.

The plain `Trie` already does exact `search` by walking one character at a time. The new thing is
the `.`: at that position any child could be the match, so we can't follow a single path anymore.
We have to try them all. That's a depth-first search down the trie, and it's where the pattern
earns its keep.

### Write the test first

```python
from .add_and_search_word import WordDictionary


def test_exact_match():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("bad") is True


def test_missing_word():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("dad") is False


def test_single_dot_matches_one_char():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search(".ad") is True
    assert d.search("b.d") is True


def test_all_dots():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("...") is True


def test_dot_does_not_match_wrong_length():
    d = WordDictionary()
    d.add_word("bad")
    assert d.search("..") is False
    assert d.search("....") is False


def test_dot_picks_among_several_branches():
    d = WordDictionary()
    d.add_word("bad")
    d.add_word("mad")
    assert d.search(".ad") is True
    assert d.search("pad") is False


def test_prefix_is_not_a_word():
    d = WordDictionary()
    d.add_word("bads")
    assert d.search("bad") is False
```

`test_dot_does_not_match_wrong_length` is the one that pins the behaviour down. A `.` matches *one*
letter, not zero and not many, so `".."` and `"...."` must miss a three-letter word. And
`test_dot_picks_among_several_branches` makes sure a `.` actually tries more than one child:
`".ad"` has to reach across both the `b` branch and the `m` branch.

### Try to run the test

We've imported `WordDictionary` from a module that doesn't define it, so the import breaks before
any test runs:

```
E   ImportError: cannot import name 'WordDictionary' from 'trie.solutions.add_and_search_word'
```

The error points at the one thing missing. Let's give it a home.

### Write the minimal amount of code for the test to run and check the failing test output

Write a `WordDictionary` whose `search` always returns `False`. It's wrong on purpose. We want the
tests to run so we can watch them fail on the value, which proves they're checking what we think.

```python
from __future__ import annotations


class WordDictionary:
    def __init__(self) -> None:
        pass

    def add_word(self, word: str) -> None:
        pass

    def search(self, word: str) -> bool:
        return False
```

Run `uv run pytest`:

```
    def test_exact_match():
        d = WordDictionary()
        d.add_word("bad")
>       assert d.search("bad") is True
E       AssertionError: assert False is True
E        +  where False = search('bad')
```

The tests run and fail on the value, not on a missing name. The misses (`test_missing_word`,
`test_prefix_is_not_a_word`) pass only because they happen to expect `False`, which is all our stub
ever returns. That's the cue to write the real thing.

### Write enough code to make it pass

`add_word` is the template's `insert` verbatim. `search` is the new part: walk the word, but when
we hit a `.`, recurse into every child and succeed if *any* of them leads to a match. That "any of
them" is the DFS.

```python
from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        return self._search(word, 0, self.root)

    def _search(self, word: str, i: int, node: TrieNode) -> bool:
        if i == len(word):
            return node.is_word
        ch = word[i]
        if ch == ".":
            return any(self._search(word, i + 1, child) for child in node.children.values())
        child = node.children.get(ch)
        if child is None:
            return False
        return self._search(word, i + 1, child)
```

The tests pass.

`_search` carries an index `i` into the word and the `node` we've walked to so far. When `i`
reaches the end of the word, the answer is just `node.is_word`, which is what makes
`test_prefix_is_not_a_word` come out right: we land on the node for `bad`, but it was never marked
a word, so `is_word` is `False`. A normal letter follows one child or fails. A `.` calls
`_search` once per child and short-circuits the moment one returns `True`. That single `any(...)`
line is the difference between following a path and exploring a tree.

The length cases fall out for free. If the word still has characters but the current node has no
matching child, we return `False`; if the word ends early, we check `is_word` at a node that isn't
a word end. So `".."` and `"...."` both miss `bad` without any special handling.

### Refactor

The recursion reads cleanly, so there's nothing to tidy in the logic. The one judgement call is
that we duplicated `TrieNode` and `insert` here instead of importing `Trie` from the template. I
did that on purpose: a solution file that stands on its own is easier to read in an interview and
in this chapter. When the DFS lives right next to the node it walks, the whole problem fits on one
screen. Re-run the tests to confirm nothing moved.

## Problem 2: Replace Words with the shortest root

> Given a list of root words and a sentence, replace every word in the sentence with the shortest
> root that is a prefix of it. If `cat` is a root, `cattle` becomes `cat`. Words with no matching
> root are left alone.

This is a prefix query, dressed up. Build a trie of the roots, then for each word in the sentence,
walk it character by character and stop at the **first node marked `is_word`**. Because we stop at
the first one, we get the shortest root automatically.

### Write the test first

```python
from .replace_words import replace_words


def test_basic_replacement():
    roots = ["cat", "bat", "rat"]
    sentence = "the cattle was rattled by the battery"
    assert replace_words(roots, sentence) == "the cat was rat by the bat"


def test_shortest_root_wins():
    roots = ["a", "aa", "aaa", "aaaa"]
    sentence = "a aa a aaaa aaa bbb"
    assert replace_words(roots, sentence) == "a a a a a bbb"


def test_no_root_leaves_word_untouched():
    roots = ["cat"]
    sentence = "the dog ran"
    assert replace_words(roots, sentence) == "the dog ran"


def test_word_equal_to_root():
    roots = ["cat"]
    sentence = "cat"
    assert replace_words(roots, sentence) == "cat"


def test_empty_roots():
    assert replace_words([], "hello world") == "hello world"
```

`test_shortest_root_wins` is the heart of it. With `a`, `aa`, `aaa`, and `aaaa` all in the trie,
every `a`-word should collapse to the single `a`, because that's the first word-end we hit on the
way down. A solution that grabs the longest prefix, or the first root that happens to match, gets
this wrong.

### Try to run the test

Nothing to import yet:

```
E   ImportError: cannot import name 'replace_words' from 'trie.solutions.replace_words'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to hand the sentence straight back. It'll pass the cases where nothing needs replacing and
fail the rest, which is exactly the split we want to see.

```python
from __future__ import annotations


def replace_words(roots: list[str], sentence: str) -> str:
    return sentence
```

Run `uv run pytest`:

```
    def test_basic_replacement():
        roots = ["cat", "bat", "rat"]
        sentence = "the cattle was rattled by the battery"
>       assert replace_words(roots, sentence) == "the cat was rat by the bat"
E       AssertionError: assert 'the cattle w...y the battery' == 'the cat was rat by the bat'
E         - the cat was rat by the bat
E         + the cattle was rattled by the battery
```

The three "no replacement" tests pass because the stub happens to be correct for them. The two that
actually replace a word fail, and they fail showing the exact untouched sentence. Now make them
pass for the right reason.

### Write enough code to make it pass

Build the trie from the roots, then map each word in the sentence through a `shortest_root` helper
that walks until it finds a word-end or runs out of trie.

```python
from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


def replace_words(roots: list[str], sentence: str) -> str:
    root = TrieNode()
    for word in roots:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def shortest_root(word: str) -> str:
        node = root
        for i, ch in enumerate(word):
            node = node.children.get(ch)
            if node is None:
                return word
            if node.is_word:
                return word[: i + 1]
        return word

    return " ".join(shortest_root(word) for word in sentence.split())
```

Green.

`shortest_root` walks the word one character at a time. The two `return` paths inside the loop are
the whole story: if a character isn't in the trie, no root is a prefix, so we return the word
unchanged (that's `test_no_root_leaves_word_untouched`); if we land on a node where `is_word` is
`True`, we've found the shortest root, so we return the slice `word[:i + 1]` and stop. Stopping at
the *first* `is_word` is what makes the shortest one win. The final `return word` handles a word
that's fully walked without ever hitting a word-end, like a sentence word that's a strict prefix of
a root.

### Refactor

This reuses the template's structure but never instantiates `Trie`: we only need `insert` (inlined
into the build loop) and a custom walk that stops early, so a bare `root` node is enough. That's a
common shape for trie problems. You rarely use the template class as-is; you reuse its *node* and
write the one walk your problem needs. Re-run the tests.

## Problem 3: Longest Word buildable one letter at a time

> Given a list of words, return the longest word that can be built one character at a time, where
> every intermediate prefix is also in the list. `apple` is buildable only when `a`, `ap`, `app`,
> and `appl` are all present too. Ties go to the lexicographically smallest word.

Insert every word, then walk the trie from the root, but only step into a child whose node is
itself a word. A path you can follow without ever leaving "word" nodes *is* a word buildable one
letter at a time. We keep the best one we see.

### Write the test first

```python
from .longest_word import longest_word


def test_single_chain():
    words = ["a", "ap", "app", "appl", "apple"]
    assert longest_word(words) == "apple"


def test_breaks_in_chain_are_excluded():
    words = ["a", "banana", "app", "appl", "ap", "apply", "apple"]
    assert longest_word(words) == "apple"


def test_lexicographically_smallest_among_longest():
    words = ["w", "wo", "wor", "worl", "world", "t", "ti", "tig", "tige", "tiger"]
    assert longest_word(words) == "tiger"


def test_no_buildable_word():
    words = ["abc", "bcd"]
    assert longest_word(words) == ""


def test_empty_input():
    assert longest_word([]) == ""
```

`test_no_buildable_word` is the trap. Both `abc` and `bcd` are in the list, but neither is
buildable, because `a`, `ab`, `b`, `bc` and the rest are all missing. A solution that just returns
the longest *word* (rather than the longest *buildable* word) returns `abc` and is wrong. And
`test_lexicographically_smallest_among_longest` forces the tie-break: `tiger` and `world` are both
length 5, so the smaller string wins.

### Try to run the test

```
E   ImportError: cannot import name 'longest_word' from 'trie.solutions.longest_word'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to the empty string. It'll pass the two cases that legitimately expect `""` and fail the
rest.

```python
from __future__ import annotations


def longest_word(words: list[str]) -> str:
    return ""
```

Run `uv run pytest`:

```
    def test_single_chain():
        words = ["a", "ap", "app", "appl", "apple"]
>       assert longest_word(words) == "apple"
E       AssertionError: assert '' == 'apple'
E         - apple

FAILED trie/solutions/test_longest_word.py::test_breaks_in_chain_are_excluded
FAILED trie/solutions/test_longest_word.py::test_lexicographically_smallest_among_longest
3 failed, 2 passed
```

The two passes are `test_no_buildable_word` and `test_empty_input`, both of which want `""`. The
three real cases fail on the value. Time to build it.

### Write enough code to make it pass

Insert every word, then DFS from the root. The rule for descending: only step into a child that's
itself a word, because that keeps every prefix along the path a real word. Visit children in sorted
order and keep the best string by length, breaking ties on the smaller string.

```python
from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


def longest_word(words: list[str]) -> str:
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    best = ""

    def visit(node: TrieNode, built: str) -> None:
        nonlocal best
        if len(built) > len(best) or (len(built) == len(best) and built < best):
            best = built
        for ch in sorted(node.children):
            child = node.children[ch]
            if child.is_word:
                visit(child, built + ch)

    visit(root, "")
    return best
```

The tests pass.

`visit` carries the string `built` so far. The guard `if child.is_word` is the rule that makes this
work: we only extend a path when the next node is a word, so when we reach `apple` we know `a`,
`ap`, `app`, and `appl` were each a word too. That's why `test_no_buildable_word` returns `""`:
from the root, neither `a` nor `b` is a word, so the DFS never descends and `best` stays empty.

The tie-break is the `or` clause: take a longer string always, but if it's the same length, only
swap to a strictly smaller one. Walking `sorted(node.children)` means we tend to meet the smaller
strings first anyway, but the explicit `built < best` makes the rule hold no matter the order.

### Refactor

The DFS is doing two jobs at once: tracking the best answer and deciding where to recurse. They're
short enough to live together, so I'd leave it. The thing worth naming is that all three problems
were the same trie walk wearing different hats. Exact-and-wildcard search branched on `.`,
shortest-root stopped at the first word-end, and this one only descended through word nodes. **The
node and the walk stay the same; the stopping rule is the problem.** Re-run the tests one last time
to be sure.

## Wrapping up

- **A trie keys a tree by character so words that share a prefix share a path.** The node is a dict
  of children plus an `is_word` flag, and that flag is what separates a stored word from a mere
  prefix.
- **Insert is one `setdefault` walk; lookup is one `get` walk.** Both are O(length of the word),
  independent of how many words you've stored.
- **The invariant: the node you reach by spelling out `s` represents the prefix `s`, and `is_word`
  says whether `s` is a stored word.** Every problem is a different reading of that walk.
- **The variant to remember is the DFS over the trie.** A `.` wildcard branches into every child; a
  shortest-root query stops at the first word-end; a buildable-word search only steps through word
  nodes. Same walk, different stopping rule.

Next: [Backtracking](backtracking.md), where the same "try a branch, abandon it the moment it can't
work" idea drives word-search grids, and a trie often rides along to prune dead paths early.
