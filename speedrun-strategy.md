# Speedrun strategy

Once you can solve problems calmly, you need to solve them *fast and under pressure*. A speedrun
is a timed, no-reference, mixed-pattern practice session that simulates the real thing. This is
where prep turns into performance.

## What a speedrun is

- **Timed.** A clock per problem (see budgets below). Interviews are time-boxed, so practise that
  way.
- **No reference.** No notes, no peeking at solutions, no autocomplete crutches. Blank file,
  blank mind, go.
- **Mixed.** You don't know which pattern is coming, exactly like an interview. Recognising the
  pattern *is* part of the drill.

## The interview loop, on a timer

Run the same loop every time so it becomes automatic:

1. **Clarify (1 to 2 min).** Restate the problem. Ask about input size, ranges, duplicates, empty
   input. Write down the constraints, because they hint at the target complexity. If `n` is at most
   20, exponential is fine; if `n` reaches 100,000, you need O(n log n).
2. **Examples into tests (2 to 3 min).** Turn the given example into an assertion, then add the edge
   cases you'll inevitably need: empty, single, duplicates, not-found. These are your spec.
3. **Name the pattern, sketch the approach (2 to 3 min).** Say it out loud: "sorted array, looking
   for a pair, so two pointers." State the complexity you're aiming for *before* coding.
4. **Code to green (10 to 15 min).** Brute force first if the optimal isn't obvious. Get the tests
   passing, then optimise with the tests guarding you.
5. **Verify (2 min).** Re-read against the edge-case tests. Trace one example by hand.

## Time budgets

| Difficulty | Target time |
|------------|-------------|
| Easy | 10 to 15 min |
| Medium | 20 to 30 min |
| Hard | 35 to 45 min |

If you blow the budget: stop, mark the problem, and move on. Afterwards, review what *specifically*
cost you. Was it pattern recognition? A Python API you fumbled? An edge case you missed? That
diagnosis is the point of the speedrun.

## If you get stuck

A protocol beats panic:

1. **Brute force.** Can you solve it with a nested loop or with recursion? Code that, get it green.
   Partial credit is real, and a working slow solution often reveals the fast one.
2. **Smaller input.** Solve `n = 1, 2, 3` by hand. The transition between cases is often the
   recurrence or the invariant.
3. **Reach for the toolbox.** Run the menu: would a `set` kill a nested-loop scan? would sorting
   give you two pointers or greedy? would a `heapq` avoid a full sort? a `dict` of seen values?
4. **Narrate the stuck-ness.** Say "I'm trying to avoid the nested loop, and I think a hash map of
   complements works...". In a real interview this invites a hint and shows your thinking.

## After every speedrun: the retro

The reps don't teach you. The **review** does.

- Which pattern was it, and how fast did you recognise it? Log slow recognitions.
- What broke: logic, an edge case, or a Python API you had to look up?
- Add anything you fumbled to your re-derivation list and redo it from a blank file tomorrow.

## A weekly rhythm

- **Daily:** one new pattern plus re-derive two or three old problems (see
  [How to study](how-to-study.md)).
- **Weekly:** one mixed speedrun of three to five problems under the clock, then a written retro.
- **Before an interview:** a speedrun of your *weakest* patterns, not your favourites.

## Wrapping up

- Speedruns make you **fast and calm**: timed, no-reference, mixed.
- Run a fixed **loop**: clarify, examples-as-tests, name the pattern, code to green, verify.
- **Have a stuck-protocol**: brute force, shrink the input, run the toolbox menu, narrate.
- The **retro** is where the learning is. Diagnose what cost you and re-derive it.

That's the method. Now go pick a pattern from the sidebar and write a failing test.
