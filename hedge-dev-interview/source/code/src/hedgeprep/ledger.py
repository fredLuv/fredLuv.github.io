"""Transactional ledger and outbox example using the Python standard library."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from typing import Any


class ConflictingEvent(ValueError):
    """The same event identity was reused for a different payload."""


@dataclass(frozen=True, slots=True)
class LedgerEntry:
    account: str
    currency: str
    amount_minor: int

    def __post_init__(self) -> None:
        if not self.account or len(self.currency) != 3:
            raise ValueError("account and three-letter currency are required")
        if self.amount_minor == 0:
            raise ValueError("zero-value ledger entries are not useful")


@dataclass(frozen=True, slots=True)
class OutboxRecord:
    event_id: str
    topic: str
    event_key: str
    payload: str


class LedgerStore:
    """Persists a balanced journal and Kafka outbox in one SQL transaction."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.row_factory = sqlite3.Row

    def initialize(self) -> None:
        self._connection.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS journal_event (
                event_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS ledger_entry (
                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL REFERENCES journal_event(event_id),
                account TEXT NOT NULL,
                currency TEXT NOT NULL CHECK (length(currency) = 3),
                amount_minor INTEGER NOT NULL CHECK (amount_minor <> 0)
            );

            CREATE TABLE IF NOT EXISTS outbox (
                event_id TEXT PRIMARY KEY REFERENCES journal_event(event_id),
                topic TEXT NOT NULL,
                event_key TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                published_at TEXT
            );

            CREATE INDEX IF NOT EXISTS outbox_pending
            ON outbox (created_at, event_id)
            WHERE published_at IS NULL;
            """
        )

    def post(
        self,
        *,
        event_id: str,
        entries: list[LedgerEntry],
        topic: str,
        event_key: str,
        event: dict[str, Any],
    ) -> bool:
        """Return True for a new event and False for an identical duplicate."""
        if not event_id or not topic or not event_key or len(entries) < 2:
            raise ValueError("identity, destination, and at least two entries required")

        totals: dict[str, int] = {}
        for entry in entries:
            totals[entry.currency] = totals.get(entry.currency, 0) + entry.amount_minor
        unbalanced = {currency: total for currency, total in totals.items() if total}
        if unbalanced:
            raise ValueError(f"journal is not balanced by currency: {unbalanced}")

        payload = json.dumps(event, sort_keys=True, separators=(",", ":"))
        with self._connection:
            inserted = self._connection.execute(
                "INSERT OR IGNORE INTO journal_event(event_id, payload) VALUES (?, ?)",
                (event_id, payload),
            )
            if inserted.rowcount == 0:
                existing = self._connection.execute(
                    "SELECT payload FROM journal_event WHERE event_id = ?", (event_id,)
                ).fetchone()
                if existing is None or existing["payload"] != payload:
                    raise ConflictingEvent(f"event ID {event_id!r} has another payload")
                return False

            self._connection.executemany(
                """
                INSERT INTO ledger_entry(event_id, account, currency, amount_minor)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (event_id, entry.account, entry.currency, entry.amount_minor)
                    for entry in entries
                ],
            )
            self._connection.execute(
                """
                INSERT INTO outbox(event_id, topic, event_key, payload)
                VALUES (?, ?, ?, ?)
                """,
                (event_id, topic, event_key, payload),
            )
        return True

    def balances(self, event_id: str) -> dict[str, int]:
        rows = self._connection.execute(
            """
            SELECT currency, SUM(amount_minor) AS total
            FROM ledger_entry
            WHERE event_id = ?
            GROUP BY currency
            """,
            (event_id,),
        )
        return {row["currency"]: row["total"] for row in rows}

    def pending_outbox(self, limit: int = 100) -> list[OutboxRecord]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        rows = self._connection.execute(
            """
            SELECT event_id, topic, event_key, payload
            FROM outbox
            WHERE published_at IS NULL
            ORDER BY created_at, event_id
            LIMIT ?
            """,
            (limit,),
        )
        return [OutboxRecord(**dict(row)) for row in rows]

    def mark_published(self, event_id: str) -> None:
        with self._connection:
            updated = self._connection.execute(
                """
                UPDATE outbox
                SET published_at = CURRENT_TIMESTAMP
                WHERE event_id = ? AND published_at IS NULL
                """,
                (event_id,),
            )
            if updated.rowcount != 1:
                raise KeyError(f"no pending outbox event {event_id!r}")


def entry_payload(entries: list[LedgerEntry]) -> list[dict[str, str | int]]:
    """Small helper for an auditable event body in the lab/demo."""
    return [asdict(entry) for entry in entries]
