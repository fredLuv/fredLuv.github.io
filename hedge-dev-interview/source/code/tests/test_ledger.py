from __future__ import annotations

import sqlite3
import unittest

from hedgeprep.ledger import ConflictingEvent, LedgerEntry, LedgerStore


class LedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.store = LedgerStore(self.connection)
        self.store.initialize()
        self.entries = [
            LedgerEntry("cash:broker", "USD", -12_500),
            LedgerEntry("cash:internal", "USD", 12_500),
        ]

    def tearDown(self) -> None:
        self.connection.close()

    def test_balanced_event_and_outbox_commit_together(self) -> None:
        created = self.store.post(
            event_id="E-1",
            entries=self.entries,
            topic="cash-movements",
            event_key="ACCOUNT-7",
            event={"kind": "CashSettled", "amount_minor": 12_500},
        )
        self.assertTrue(created)
        self.assertEqual(self.store.balances("E-1"), {"USD": 0})
        self.assertEqual([record.event_id for record in self.store.pending_outbox()], ["E-1"])

    def test_unbalanced_event_changes_nothing(self) -> None:
        with self.assertRaisesRegex(ValueError, "not balanced"):
            self.store.post(
                event_id="E-2",
                entries=[self.entries[0], LedgerEntry("cash:internal", "USD", 12_499)],
                topic="cash-movements",
                event_key="ACCOUNT-7",
                event={"kind": "CashSettled"},
            )
        count = self.connection.execute("SELECT COUNT(*) FROM journal_event").fetchone()[0]
        self.assertEqual(count, 0)

    def test_identical_duplicate_is_idempotent(self) -> None:
        arguments = dict(
            event_id="E-3",
            entries=self.entries,
            topic="cash-movements",
            event_key="ACCOUNT-7",
            event={"kind": "CashSettled", "amount_minor": 12_500},
        )
        self.assertTrue(self.store.post(**arguments))
        self.assertFalse(self.store.post(**arguments))
        count = self.connection.execute("SELECT COUNT(*) FROM ledger_entry").fetchone()[0]
        self.assertEqual(count, 2)

    def test_conflicting_duplicate_is_rejected(self) -> None:
        self.store.post(
            event_id="E-4",
            entries=self.entries,
            topic="cash-movements",
            event_key="ACCOUNT-7",
            event={"kind": "CashSettled", "amount_minor": 12_500},
        )
        with self.assertRaises(ConflictingEvent):
            self.store.post(
                event_id="E-4",
                entries=self.entries,
                topic="cash-movements",
                event_key="ACCOUNT-7",
                event={"kind": "CashSettled", "amount_minor": 12_501},
            )


if __name__ == "__main__":
    unittest.main()
