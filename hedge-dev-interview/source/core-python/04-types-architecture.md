# 4. Types and Clean Architecture

## Interview outcome

Use Python's type system to express boundaries without turning the code into Java,
and design components that are replaceable in tests and production.

## Gradual typing, honestly stated

Type hints are metadata. Static checkers, IDEs, linters, and readers use them;
CPython does not generally reject a wrong argument at runtime.

Annotate public boundaries and non-obvious domain structures. Let obvious local
variables infer. A type checker is strongest when `Any` is rare and untyped I/O
is validated at the boundary.

```python
from typing import NewType

OrderId = NewType("OrderId", str)
StrategyId = NewType("StrategyId", str)
```

`NewType` helps static tools distinguish values represented by the same runtime
type. It does not create a runtime wrapper.

## Protocols over inheritance

```python
from collections.abc import Iterable
from typing import Protocol

class PriceSource(Protocol):
    def prices(self, symbol: str) -> Iterable[float]: ...

class SignalEngine:
    def __init__(self, source: PriceSource) -> None:
        self._source = source
```

Any object with the required method satisfies the structural contract to a static
checker. This enables small fakes without forcing a shared base class. Use an
abstract base class when shared runtime identity, registration, or implementation
is genuinely part of the contract.

## Model states so invalid transitions stand out

```python
from dataclasses import dataclass
from enum import Enum, auto

class OrderStatus(Enum):
    CREATED = auto()
    SENT = auto()
    ACKNOWLEDGED = auto()
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()

TERMINAL = {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED}

@dataclass(frozen=True, slots=True)
class OrderUpdate:
    order_id: str
    status: OrderStatus
    cumulative_quantity: int
```

Do not model a state machine as unrelated booleans (`is_sent`, `is_filled`,
`is_cancelled`) that can represent impossible combinations.

## Dependency direction

Keep the domain independent from databases, brokers, and frameworks:

```text
entry point → application service → domain
                 ↓
             ports/protocols
                 ↑
      broker, database, file adapters
```

The domain defines what it needs. Adapters implement it. Tests supply in-memory
implementations. This is dependency inversion without ceremony.

## Validation belongs at boundaries

External dictionaries/JSON are untrusted. Parse once into domain values, reject
unknown or invalid states, then let internal code operate on stronger invariants.
Do not spread `dict[str, object]` through the system.

Separate:

- transport schema (wire compatibility);
- validated domain event (business meaning);
- storage schema (query and retention concerns).

One class rarely serves all three well.

## Composition versus inheritance

Prefer a strategy that receives a signal function and risk policy over a deep
hierarchy of `AbstractBaseMeanRevertingEquityStrategy`. Inheritance is appropriate
when substitutability is stable and tested. Composition keeps independent axes of
change independent.

## Packaging rules for an interview project

- `src/` layout prevents tests from accidentally importing the working directory.
- one package with cohesive modules beats many tiny deployment units;
- use absolute imports across packages and relative imports sparingly within one;
- public API is explicit; leading underscore marks implementation detail;
- configuration enters at the composition root, not through imports of globals.

## Drill

Define protocols for `Clock`, `EventStore`, and `ExecutionGateway`. Design a
`TradingService` that validates an order, checks risk, persists intent, submits,
and records the result. Explain what happens if the gateway times out after the
venue accepted the order.

The senior answer does not blindly retry. It uses a stable client order ID, marks
the result unknown, queries/reconciles, and makes recovery repeatable.

## Answer frame

> I use typing to make boundaries and domain states visible, not to simulate Java.
> Protocols define the behavior a consumer needs. Domain logic depends on those
> ports, while I/O adapters depend inward. Runtime validation occurs once at
> untrusted boundaries.
