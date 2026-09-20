#!/usr/bin/env python3
"""Acoustic-B-Box v0.2 - small hospital-operations communication simulator.

This is a learning prototype, not a clinical system. All medical examples are
synthetic and all response/staff fields are simulation parameters only.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path("acoustic_bbox.db")
CATEGORIES = {
    "MEDICAL": "Clinical event",
    "EQUIPMENT": "Equipment problem",
    "LOGISTICS": "Supply/logistics request",
    "ENVIRONMENT": "Environment alert",
    "OPERATIONS": "Workflow notification",
    "SYSTEM": "System/device status",
}
PRIORITIES = {
    "P0": "Critical / immediate attention",
    "P1": "Urgent / rapid attention",
    "P2": "Priority / soon",
    "P3": "Routine",
    "P4": "Informational",
}
DEPARTMENTS = ["Emergency", "ICU", "Ward A", "Pharmacy", "Laboratory", "Maintenance", "Operations"]

SCENARIOS = {
    "1": ("MEDICAL", "P1", "VITAL_ALERT", "ICU", "Synthetic patient-monitor alert", 2),
    "2": ("EQUIPMENT", "P1", "DEVICE_FAILURE", "Emergency", "Synthetic monitor/device failure", 1),
    "3": ("LOGISTICS", "P2", "SUPPLY_REQUIRED", "Pharmacy", "Synthetic supply request", 1),
    "4": ("ENVIRONMENT", "P2", "TEMPERATURE_ALERT", "Ward A", "Synthetic temperature alert", 1),
    "5": ("OPERATIONS", "P3", "WORKFLOW_NOTIFICATION", "Operations", "Synthetic workflow notification", 0),
    "6": ("SYSTEM", "P4", "DEVICE_STATUS", "Maintenance", "Synthetic device status update", 0),
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id(prefix="BX"):
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


@dataclass
class Event:
    event_id: str
    created_at: str
    category: str
    priority: str
    event_type: str
    department: str
    description: str
    source_device: str = "SIM-DEVICE-01"
    status: str = "CREATED"
    minimum_staff: int = 0
    response_roles: list[str] = field(default_factory=list)
    attempts: int = 0
    transport: str = "SIMULATOR"


class Store:
    def __init__(self, path=DB_PATH):
        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row
        self.con.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY, created_at TEXT, category TEXT,
                priority TEXT, event_type TEXT, department TEXT,
                description TEXT, source_device TEXT, status TEXT,
                minimum_staff INTEGER, response_roles TEXT,
                attempts INTEGER, transport TEXT
            );
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT, at TEXT, action TEXT, details TEXT
            );
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY, department TEXT,
                status TEXT, last_seen TEXT
            );
            """
        )
        self.seed_devices()

    def seed_devices(self):
        for i, department in enumerate(DEPARTMENTS, 1):
            self.con.execute(
                "INSERT OR IGNORE INTO devices VALUES (?, ?, ?, ?)",
                (f"SIM-DEVICE-{i:02d}", department, "ONLINE", now()),
            )
        self.con.commit()

    def save_event(self, event):
        self.con.execute(
            """INSERT OR REPLACE INTO events VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                event.event_id, event.created_at, event.category,
                event.priority, event.event_type, event.department,
                event.description, event.source_device, event.status,
                event.minimum_staff, json.dumps(event.response_roles),
                event.attempts, event.transport,
            ),
        )
        self.con.commit()

    def audit(self, event_id, action, details=""):
        self.con.execute(
            "INSERT INTO audit_log(event_id, at, action, details) VALUES (?, ?, ?, ?)",
            (event_id, now(), action, details),
        )
        self.con.commit()

    def recent_events(self, limit=10):
        return self.con.execute(
            "SELECT * FROM events ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()

    def timeline(self, event_id):
        return self.con.execute(
            "SELECT * FROM audit_log WHERE event_id=? ORDER BY id", (event_id,)
        ).fetchall()

    def close(self):
        self.con.close()


def create_scenario(choice):
    if choice not in SCENARIOS:
        raise ValueError("Unknown scenario.")
    category, priority, event_type, department, description, staff = SCENARIOS[choice]
    roles = {
        "P0": ["primary_responder", "supervisor"],
        "P1": ["department_responder"],
        "P2": ["assigned_operator"],
        "P3": ["department_queue"],
        "P4": [],
    }[priority]
    return Event(
        event_id=new_id(),
        created_at=now(),
        category=category,
        priority=priority,
        event_type=event_type,
        department=department,
        description=description,
        minimum_staff=staff,
        response_roles=roles,
    )


def print_event(event):
    print(f"\n[{event.priority}] {event.event_id} | {event.category} | {event.event_type}")
    print(f"Department : {event.department}")
    print(f"Status     : {event.status}")
    print(f"Description: {event.description}")
    print(f"Staff demo : {event.minimum_staff}")
    print(f"Roles      : {', '.join(event.response_roles) or 'none'}")
    print(f"Transport  : {event.transport}")
    print(f"Attempts   : {event.attempts}")


def simulate_event(store, event):
    store.save_event(event)
    store.audit(event.event_id, "CREATED", event.category)
    print_event(event)

    for status in ["DISPATCHED", "DELIVERED", "ACKNOWLEDGED", "IN_PROGRESS", "RESOLVED"]:
        time.sleep(0.15)
        event.status = status
        event.attempts = 1
        store.save_event(event)
        store.audit(event.event_id, status, f"transport={event.transport}")
        print(f"  ✓ {status}")

    print(f"\nEvent {event.event_id} completed in simulation.")


def show_dashboard(store):
    rows = store.recent_events()
    print("\n=== ACOUSTIC-B-BOX SAMPLE OPERATIONS DASHBOARD ===")
    print(f"Database: {DB_PATH}")
    print(f"Categories: {len(CATEGORIES)} | Priorities: {len(PRIORITIES)}")
    print("-" * 72)
    if not rows:
        print("No events yet. Run a scenario first.")
        return
    for r in rows:
        print(
            f"{r['priority']:>2} | {r['status']:<13} | "
            f"{r['event_id']:<15} | {r['department']:<12} | {r['event_type']}"
        )


def run_scenario(store):
    print("\nChoose a synthetic scenario:")
    for key, item in SCENARIOS.items():
        print(f"{key}. [{item[1]}] {item[4]}")
    choice = input("Scenario: ").strip()
    simulate_event(store, create_scenario(choice))


def run_self_test():
    event = create_scenario("1")
    assert event.category in CATEGORIES
    assert event.priority in PRIORITIES
    payload = json.dumps(asdict(event), separators=(",", ":")).encode()
    recovered = json.loads(payload.decode())
    assert recovered["event_id"] == event.event_id
    assert recovered["priority"] == event.priority
    print("SELF-TEST: PASS")
    print("✓ Event creation")
    print("✓ Priority/category validation")
    print("✓ JSON encode/decode")
    print("✓ Message ID generation")
    print("No microphone/speaker required.")


def broadcast_acoustic(event):
    """Optional experimental hardware path; simulator does not need it."""
    try:
        import ggwave
        import numpy as np
        import sounddevice as sd
    except ImportError:
        print("Optional acoustic dependencies are not installed.")
        print("Use python acoustic_bbox.py --simulate for the sample system.")
        return

    payload = json.dumps(asdict(event), separators=(",", ":")).encode()
    params = ggwave.getDefaultParameters()
    context = ggwave.init(params)
    try:
        waveform = ggwave.encode(context, payload)
        audio = np.frombuffer(waveform, dtype=np.int16)
        print(f"Broadcasting {event.event_id} ({len(payload)} bytes)...")
        sd.play(audio, params.sampleRate)
        sd.wait()
        print("Acoustic transmission finished.")
    finally:
        ggwave.free(context)


def main():
    parser = argparse.ArgumentParser(description="Acoustic-B-Box v0.2 sample system")
    parser.add_argument("--simulate", action="store_true", help="Run the simple hospital-event simulator")
    parser.add_argument("--dashboard", action="store_true", help="Show recent events")
    parser.add_argument("--test", action="store_true", help="Run the hardware-free self-test")
    args = parser.parse_args()

    if args.test:
        run_self_test()
        return

    store = Store()
    try:
        if args.dashboard:
            show_dashboard(store)
        elif args.simulate:
            run_scenario(store)
            show_dashboard(store)
        else:
            print("Acoustic-B-Box v0.2")
            print("1. Run sample hospital event")
            print("2. View dashboard")
            print("3. Self-test")
            print("4. Acoustic broadcast (experimental)")
            choice = input("Select: ").strip()
            if choice == "1":
                run_scenario(store)
                show_dashboard(store)
            elif choice == "2":
                show_dashboard(store)
            elif choice == "3":
                run_self_test()
            elif choice == "4":
                broadcast_acoustic(create_scenario("1"))
            else:
                print("Invalid selection.")
    finally:
        store.close()


if __name__ == "__main__":
    main()
