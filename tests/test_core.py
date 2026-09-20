import json
import tempfile
import unittest
from pathlib import Path

import acoustic_bbox


class CoreTests(unittest.TestCase):
    def test_scenario_is_structured(self):
        event = acoustic_bbox.create_scenario("1")
        self.assertIn(event.category, acoustic_bbox.CATEGORIES)
        self.assertIn(event.priority, acoustic_bbox.PRIORITIES)
        self.assertTrue(event.event_id.startswith("BX-"))

    def test_json_round_trip(self):
        event = acoustic_bbox.create_scenario("3")
        encoded = json.dumps(acoustic_bbox.asdict(event), separators=(",", ":"))
        decoded = json.loads(encoded)
        self.assertEqual(decoded["event_id"], event.event_id)
        self.assertEqual(decoded["event_type"], "SUPPLY_REQUIRED")

    def test_sqlite_event_and_audit(self):
        with tempfile.TemporaryDirectory() as d:
            store = acoustic_bbox.Store(Path(d) / "test.db")
            event = acoustic_bbox.create_scenario("5")
            store.save_event(event)
            store.audit(event.event_id, "CREATED", "test")
            self.assertEqual(len(store.recent_events()), 1)
            self.assertEqual(len(store.timeline(event.event_id)), 1)
            store.close()


if __name__ == "__main__":
    unittest.main()
