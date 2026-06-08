# Why TDD for interviews

Test-driven development has a reputation as a slow, ceremonial practice for big codebases. In a
coding interview it's the opposite: it's the fastest way to a correct answer under pressure.
Here's the case.

## What doesn't work

**Grinding hundreds of random problems.** It feels productive, but without structure you learn
problems, not patterns, and you forget last week's. You also build no reusable habit for the
moment you're stuck on a *new* problem in a real interview.

**Reading solutions.** You nod along, it makes sense, and then a blank editor in the interview
reveals you can't reproduce it. Understanding a solution and being able to *generate* one are
different skills.

**"Just code it and run it on the examples."** This is how most people interview, and it's why
they freeze: they write the whole thing, run it, get a wrong answer, and have no idea which part
is broken. No safety net, no feedback until the end.

## What TDD gives you in an interview

**A failing test forces you to define "done" first.** Before writing any logic you write
`assert two_sum([2, 7, 11, 15], 9) == (0, 1)`. Now the function's contract (inputs, output
shape, edge cases) is concrete and agreed with your interviewer. Half of interview failures are
solving the wrong problem, and a test up front prevents that.

**Edge cases become a checklist, not an afterthought.** Empty input, single element, duplicates,
negatives, the target-not-found case: you write them as tests *before* you're deep in the
logic, when you can still think clearly about them. Interviewers love watching a candidate
enumerate edge cases early.

**You get feedback every 30 seconds, not at the end.** Red, green, red, green. When something
breaks you know exactly which behaviour and which line, because only the last small change could
have caused it. No staring at a 40-line function wondering where it went wrong.

**Refactoring is safe.** Get it working with a brute-force O(n²), lock it in with tests, then
optimise to O(n) with the tests catching any mistake the moment you make it. This "make it work,
then make it fast" path, visible to the interviewer, is exactly the thinking they're scoring.

**It externalises your reasoning.** The interview isn't really about the answer; it's about
*how you think*. Tests make your thinking visible: here's the contract, here are the cases I'm
worried about, here's me proving each one. That narrative is worth more than a silently-correct
solution.

## "Isn't there no time for tests?"

You're writing the example checks anyway. TDD just means writing them *first*, as real
assertions, instead of eyeballing `print` output at the end. It's the same work, reordered so it
helps you instead of judging you. With `pytest` a test is one line (`assert f(x) == y`), so the
overhead is seconds.

You won't write tests for every interview problem the same way you would production code. But the
*habit* (start from the contract, name your edge cases, work in small verified steps) is what
makes you fast and calm. That habit is what this book trains.

## How this book builds the habit

Every chapter walks the same loop: **write the failing test → watch it fail → minimal code to
pass → refactor**. By the time you've done it across the Python fundamentals and a dozen
interview patterns, it's automatic. In the real interview you won't be *doing TDD*; you'll just
be someone who naturally starts from examples, names edge cases, and works in verified steps.
