# 2. Objects, Mutability, Equality, and Hashing

## Interview outcome

Predict aliasing and collection behavior, design safe value objects, and explain
the equality/hash contract.

## Identity, equality, and hash

```python
a = [1, 2]
b = [1, 2]
assert a == b       # equivalent values
assert a is not b   # distinct objects
```

Use `is` for singletons such as `None` and occasionally sentinel objects. Use
`==` for values. Small-integer and string interning are implementation details,
not a reason to use `is` for numbers or text.

Hash collections assume an object's hash is stable while stored and that equal
objects have equal hashes:

```text
a == b  =>  hash(a) == hash(b)
```

The reverse is not required; collisions are legal. Mutable containers are
normally unhashable because changing data involved in a hash would make the
object impossible to find in its bucket.

## Shallow versus deep copy

```python
original = {"AAPL": {"qty": 10}}
shallow = original.copy()
shallow["AAPL"]["qty"] = 20
assert original["AAPL"]["qty"] == 20
```

A shallow copy duplicates the outer container, not nested objects. Deep copy is
not a universal fix: it can be expensive, copy objects that should remain shared,
or fail on handles. Prefer immutable domain values and explicit reconstruction.

## Safe domain objects

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True, slots=True)
class Fill:
    order_id: str
    symbol: str
    quantity: int
    price: Decimal

    @property
    def notional(self) -> Decimal:
        return self.price * self.quantity
```

- `frozen=True` prevents normal attribute reassignment and communicates a value.
- `slots=True` avoids a per-instance attribute dictionary and rejects accidental
  attribute creation; measure before claiming a performance win.
- generated equality compares fields. A frozen dataclass can usually be hashed
  if all fields are hashable.
- `Decimal` can express exact base-10 rules, but only if precision, rounding, and
  conversion policy are explicit. Never construct it from an inexact float when
  exact decimal intent matters: use `Decimal("10.25")`.

For timestamps, prefer timezone-aware `datetime` in the domain and an integer
epoch representation at wire/storage boundaries when required. Never mix naive
and aware timestamps.

## Mutable default trap

Defaults are evaluated when the function is defined, not per call.

```python
def collect(value: int, bucket: list[int] = []) -> list[int]:  # wrong
    bucket.append(value)
    return bucket

def collect_safe(value: int, bucket: list[int] | None = None) -> list[int]:
    result = [] if bucket is None else bucket
    result.append(value)
    return result
```

Dataclasses protect against obvious mutable field defaults; use a factory:

```python
from dataclasses import dataclass, field

@dataclass
class Book:
    levels: dict[int, int] = field(default_factory=dict)
```

## Special methods form protocols

Python syntax delegates to “dunder” methods:

- `len(x)` → `x.__len__()`
- `x[y]` → `x.__getitem__(y)`
- `for v in x` → iteration protocol
- `with x` → `__enter__` / `__exit__`
- `x + y` → `__add__` then reflected/fallback rules

Call the public operation (`len(x)`), not the dunder directly. Implement a
protocol only when the semantics are unsurprising. A portfolio is not a number
merely because `+` can be implemented.

## Class attributes and instance attributes

```python
class Counter:
    total = 0              # shared class attribute

    def __init__(self) -> None:
        self.local = 0     # per-instance attribute
```

Attribute lookup checks the instance and class hierarchy, with descriptor rules
involved. Mutable class attributes are shared across instances and often cause
the same bug as mutable function defaults.

## Numeric traps relevant to finance

- binary floats cannot exactly represent many decimal fractions;
- `NaN != NaN`, and NaNs can silently contaminate calculations;
- boolean is a subclass of integer (`isinstance(True, int)` is true);
- negative indexing is valid and may hide boundary errors;
- `round` follows banker-style ties and float representation can surprise;
- mixing units or currencies is a domain-model bug, not a precision bug.

## Drill

Design an immutable `Price` value with `currency`, `amount`, and a method to add
another price. Reject currency mismatch. Decide whether it should be hashable,
and write three tests: equality, mismatch, and dictionary-key use.

## Answer frame

> Identity says whether two names reference the same object; equality is a
> type-defined value relation. Hash keys must remain stable, and equality implies
> equal hashes. I prefer immutable value objects at system boundaries because
> they reduce aliasing and make replay, testing, and concurrency easier.
