"""Greedy has no single reusable skeleton, so this file is a note, not a template.

A greedy algorithm makes the locally best choice at each step and never revisits
it. Unlike two pointers or prefix sum, there is no generic function to import and
adapt. The shape changes per problem: sometimes you sweep left to right tracking a
single number (a reach, a running balance, a last-seen index), sometimes you sort
first and then sweep.

What every greedy solution shares is the obligation to argue that the local choice
is safe, that taking it never blocks a better global answer. That argument is the
real work. The code is usually one short pass.

Each worked problem in ``solutions/`` carries its own greedy choice and its own
proof sketch. Start there.
"""
