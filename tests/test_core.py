import json
import tempfile
import unittest
from pathlib import Path

import acoustic_bbox as app


class CoreTests(unittest.TestCase):
    def test_event_payload(self):
        event = app.create_scenario("3")
        payload = app.payload_for(event)
        self.assertEqual(payload["message_id"], event.event_id)
        self.assertEqual(payload["priority"], "P2")
        self.assertEqual(
            json.loads(app.payload_bytes(event).decode())["event_type"],
            "SUPPLY_REQUIRED",
        )

    def test_lifecycle_and_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = app.Store(Path(tmp) / "test.db")
            event = app.create_scenario("2")
            app.complete_simulated_event(
                store,
                event,
                app.SimulatorTransport(planned_failures=1),
            )
            self.assertEqual(event.status, "RESOLVED")
            self.assertEqual(event.attempts, 2)
            self.assertEqual(
                store.con.execute(
                    "SELECT COUNT(*) FROM transmissions WHERE event_id=?",
                    (event.event_id,),
                ).fetchone()[0],
                2,
            )
            self.assertTrue(len(store.timeline(event.event_id)) >= 6)
            store.close()

    def test_invalid_transition_is_rejected(self):
        event = app.create_scenario("5")
        with self.assertRaises(ValueError):
            app.transition(event, "RESOLVED")


if __name__ == "__main__":
    unittest.main()
