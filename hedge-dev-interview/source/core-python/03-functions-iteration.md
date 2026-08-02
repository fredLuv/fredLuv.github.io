# 3. Functions, Iteration, and Resource Scope

## Interview outcome

Use functions as values, avoid closure traps, stream data with generators, and
manage resources deterministically.

## Functions are objects

Functions can be passed, returned, stored, and decorated. Closures retain bindings
from an enclosing scope.

```python
from collections.abc import Callable

def above(limit: float) -> Callable[[float], bool]:
    def predicate(value: float) -> bool:
        return value > limit
    return predicate
```

Names in closures are resolved when the inner function runs (late binding), which
creates a classic loop trap:

```python
wrong = [lambda: i for i in range(3)]
assert [f() for f in wrong] == [2, 2, 2]

fixed = [lambda i=i: i for i in range(3)]
assert [f() for f in fixed] == [0, 1, 2]
```

The fixed version captures each current value in a new default argument.

## Decorators preserve contracts

A decorator replaces a function with another callable. Preserve metadata and
return the wrapped result.

```python
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def timed(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        started = perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            elapsed = perf_counter() - started
            print(f"{fn.__name__} seconds={elapsed:.6f}")
    return wrapper
```

In production, emit a metric rather than printing. Be cautious with decorators
that change exception behavior, hide signatures, or introduce unbounded retries.

## Iterable, iterator, generator

- An **iterable** can produce an iterator (`iter(x)`).
- An **iterator** produces the next item (`next(x)`) and retains traversal state.
- A **generator function** contains `yield`; calling it returns a generator without
  executing its body yet.

```python
from collections.abc import Iterable, Iterator

def changes(prices: Iterable[float]) -> Iterator[float]:
    it = iter(prices)
    try:
        previous = next(it)
    except StopIteration:
        return
    for current in it:
        yield current - previous
        previous = current
```

This is lazy and O(1) auxiliary space. Errors can occur during consumption, not
construction. A generator is generally single-pass and should not be silently
reused.

## Context managers are scoped guarantees

`with` is for more than files. Use it for locks, transactions, tracing spans,
temporary configuration, and resource lifecycles.

```python
from contextlib import contextmanager
from collections.abc import Iterator

@contextmanager
def transaction(connection) -> Iterator[None]:
    try:
        yield
    except BaseException:
        connection.rollback()
        raise
    else:
        connection.commit()
```

Catch `BaseException` here only because cleanup must occur for cancellation and
interrupts too; re-raise immediately. Normal application error handling usually
catches specific `Exception` subclasses.

## Argument design

```python
def submit_order(
    symbol: str,
    quantity: int,
    *,
    limit_price: float | None = None,
    reduce_only: bool = False,
) -> str:
    ...
```

The `*` makes later parameters keyword-only. This prevents opaque calls such as
`submit_order("AAPL", 100, 12.3, True)` and makes API evolution safer. Avoid
functions with a dozen booleans; use a configuration value object.

`*args` collects positional arguments and `**kwargs` collects named arguments.
Use them in adapters and decorators, not to erase a domain API's contract.

## Scope rules

Python resolves names through local, enclosing, global, builtins (LEGB). Assignment
inside a function makes a name local unless declared `nonlocal` or `global`.
Prefer returned state or an object over hidden global mutation.

## Drill

Implement `merge_ticks(streams)`, accepting sorted iterables of `(timestamp,
sequence, value)` and yielding one globally ordered stream without loading all
events. Define tie-breaking. Hint: `heapq.merge` can do the hard part when each
input uses the same total ordering.

Then wrap consumption in a context manager that records processed count and
elapsed time even if parsing raises.

## Answer frame

> Iterables describe how to obtain an iterator; iterators carry traversal state;
> generators are a concise implementation that suspend at `yield`. Laziness lowers
> memory and time-to-first-result but moves work and failures to consumption. I use
> context managers to make cleanup and commit/rollback rules explicit.
