"""Concurrency in Python: ThreadPoolExecutor for I/O-bound work, and a small asyncio coroutine.

Two ways to run work concurrently in the standard library:

- ``concurrent.futures.ThreadPoolExecutor`` runs a function over many inputs on a pool of
  threads. Because of the GIL, threads don't speed up CPU-bound Python, but they overlap the
  *waiting* in I/O-bound work (network calls, disk reads).
- ``asyncio`` runs coroutines (``async def``) on a single thread with an event loop. ``await``
  hands control back to the loop while one coroutine waits, so others can run.

Everything here is a pure function or a trivial coroutine, so the tests are deterministic and
fast with no real sleeps to flake on.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor


def square(n: int) -> int:
    """A pure, CPU-cheap function we can map over inputs."""
    return n * n


def parallel_map(numbers: list[int], workers: int = 4) -> list[int]:
    """Run ``square`` over ``numbers`` on a thread pool, results in input order.

    ``executor.map`` returns results in the same order as the inputs, regardless of which
    thread finished first, so the output is deterministic.
    """
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(square, numbers))


async def fetch_value(n: int) -> int:
    """A coroutine that 'fetches' a value. Stands in for an awaited I/O call."""
    await asyncio.sleep(0)  # yield to the event loop without a real delay
    return n * n


async def gather_values(numbers: list[int]) -> list[int]:
    """Await many ``fetch_value`` coroutines concurrently and collect their results.

    ``asyncio.gather`` schedules every coroutine on the same event loop and returns their
    results in the order the coroutines were passed, not the order they finished.
    """
    return await asyncio.gather(*(fetch_value(n) for n in numbers))


def fetch_all(numbers: list[int]) -> list[int]:
    """Synchronous entry point that runs the async pipeline to completion.

    ``asyncio.run`` starts an event loop, runs the coroutine, and tears the loop down. It's the
    one synchronous call you need to cross from ordinary code into async code.
    """
    return asyncio.run(gather_values(numbers))
