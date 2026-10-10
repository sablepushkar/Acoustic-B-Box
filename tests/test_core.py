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
        self.assertEqual(payload["bbox_version"], "A.B.B Q3")
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

    def test_description_must_be_non_empty(self):
        event = app.create_scenario("3")
        event.description = "  "
        with self.assertRaisesRegex(ValueError, "description"):
            app.validate_event(event)

    def test_boolean_is_not_accepted_as_response_unit_count(self):
        event = app.create_scenario("3")
        event.response_units = True
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            app.validate_event(event)

    def test_non_json_payload_data_is_rejected(self):
        event = app.create_scenario("3")
        event.data = {"bad": float("nan")}
        with self.assertRaisesRegex(ValueError, "strict JSON"):
            app.validate_event(event)

    def test_response_roles_must_be_non_empty_strings(self):
        event = app.create_scenario("3")
        event.response_roles = [" "]
        with self.assertRaisesRegex(ValueError, "response_roles"):
            app.validate_event(event)

    def test_decoder_accepts_current_project_version(self):
        packet = app.payload_for(app.create_scenario("3"))
        self.assertIs(app.validate_decoded_packet(packet), packet)

    def test_decoder_rejects_stale_payload_version(self):
        packet = app.payload_for(app.create_scenario("3"))
        packet["bbox_version"] = "0.3"
        with self.assertRaisesRegex(ValueError, "A.B.B Q3"):
            app.validate_decoded_packet(packet)

    def test_decoder_rejects_missing_message_id(self):
        packet = app.payload_for(app.create_scenario("3"))
        packet.pop("message_id")
        with self.assertRaisesRegex(ValueError, "A.B.B Q3"):
            app.validate_decoded_packet(packet)

    def test_decoder_rejects_non_object_payload(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            app.validate_decoded_packet(["not", "an", "object"])


if __name__ == "__main__":
    unittest.main()
