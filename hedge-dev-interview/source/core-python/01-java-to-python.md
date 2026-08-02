# 1. Mental Model and Syntax

## Interview outcome

Write small, readable Python without translating Java line by line. Explain what
Python decides at runtime and what tooling checks before runtime.

## The Java-to-Python translation table

| Java instinct | Python default | Important break in the analogy |
|---|---|---|
| nominal class/interface | duck typing plus optional `Protocol` | behavior can matter without inheritance |
| `null` | `None` | use `is None`, not `== None` |
| getters/setters | direct attributes or `@property` | do not write boilerplate accessors by default |
| method overloads | defaults, keyword args, singledispatch | later definitions replace earlier ones |
| streams | comprehensions, generator expressions, iterators | many iterators are single-pass |
| try-with-resources | `with` context manager | works for any enter/exit protocol |
| checked exception | no checked exceptions | document and test failure contracts |
| `equals` / `==` | `==` / `is` | `is` means identity, never value equality |
| primitives + references | everything is an object reference | names bind to objects; assignment does not copy |
| static generics | gradual type hints | hints do not enforce types at runtime |

## Names bind; variables are not boxes

```python
a = [1, 2]
b = a            # bind another name to the same list
b.append(3)
assert a == [1, 2, 3]

c = a.copy()     # new outer list
assert c == a and c is not a
```

Assignment changes a binding. Mutation changes an object. This single model
explains aliasing, mutable defaults, shallow copies, and many interview traps.

Parameter passing is **call by sharing**: the function receives a new local name
bound to the same object. Rebinding the local name is invisible to the caller;
mutating the shared object is visible.

```python
def change(xs: list[int]) -> None:
    xs.append(9)      # caller sees mutation
    xs = [0]          # local rebinding only

values = [1]
change(values)
assert values == [1, 9]
```

## Core syntax worth making automatic

```python
from collections.abc import Iterable

def positive_notional(prices: Iterable[float], quantities: Iterable[int]) -> float:
    return sum(
        price * quantity
        for price, quantity in zip(prices, quantities, strict=True)
        if quantity > 0
    )
```

Notice the interview-relevant choices:

- accept the broad interface you need (`Iterable`), not only `list`;
- use a generator expression so `sum` consumes lazily;
- use `zip(..., strict=True)` when unequal input lengths are a data error;
- annotate the public contract and choose names that carry domain meaning.

### Collections

- `list`: ordered, mutable sequence; append is amortized O(1), front removal O(n).
- `tuple`: ordered, immutable container; hashable only if all elements are hashable.
- `dict`: insertion-ordered mapping; average O(1) lookup; keys must be hashable.
- `set`: unique hashable members; use for membership and set algebra.
- `deque`: O(1) append/pop at both ends; use for queues and rolling windows.
- `heapq`: list-backed min-heap; use for priorities or merging ordered streams.

### Comprehensions versus loops

Use a comprehension for one readable transform/filter. Use a loop when there are
multiple state changes, logging, early exits, or error branches.

```python
symbols = {row.symbol for row in rows if row.is_active}

valid = []
for row in rows:
    if not row.is_active:
        continue
    validate(row)
    valid.append(normalize(row))
```

## Truthiness is a protocol

`None`, numeric zero, and empty containers are false. Other objects are usually
true unless `__bool__` or `__len__` says otherwise.

Do not collapse semantically distinct states:

```python
# Wrong if zero is a valid limit
limit = configured_limit or default_limit

# Correct
limit = default_limit if configured_limit is None else configured_limit
```

## Imports and module boundaries

A module is executed once per interpreter process on first import, then cached in
`sys.modules`. Avoid network calls, thread creation, large data loads, or mutable
global setup at import time. Put executable entry points behind:

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Circular imports usually reveal muddled ownership. Move shared domain types to a
lower-level module or invert the dependency behind a protocol.

## Failure modes

- `[[0] * width] * height` aliases every row.
- `if value:` wrongly rejects valid zero or empty values.
- `except Exception: pass` destroys evidence and may corrupt state.
- wildcard imports hide dependencies and invite collisions.
- a class with only one stateless method is often just a function.
- clever nested comprehensions make review and debugging slower.

## Drill

Write `top_exposures(rows, n)` where each row is `(symbol, quantity, price)`.
Return the `n` symbols with largest absolute notional, reject duplicate symbols,
reject non-positive `n`, and do not mutate the input. State time and space cost.

Expected reasoning: one validation pass plus sorting is O(m log m) time and O(m)
space. A size-`n` heap can reduce selection to O(m log n) if `n` is small, but the
simpler sort may be the better interview implementation unless scale demands it.

## Answer frame

> Python names reference objects. Assignment rebinds a name; mutation changes the
> referenced object. I choose collections by operation and express the narrowest
> useful contract with type hints, while remembering those hints are not runtime
> enforcement.
