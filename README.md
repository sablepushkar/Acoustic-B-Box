# Acoustic-B-Box

## v0.2 - Resilient hospital-operations communication prototype

Acoustic-B-Box is a small learning project exploring how structured, event-based
notifications could move between nearby systems when ordinary communication
paths are unavailable. GGWave is the experimental acoustic transport; it is not
the product's entire architecture.

IMPORTANT: this repository is a prototype and simulator. All medical data is
synthetic and all priority, staffing and response fields are demonstration
parameters, not clinical guidance. Do not use this project with real patient
data or for real emergency decision-making.

## Simple architecture

Event -> Priority -> Department -> Transport -> Delivery -> Acknowledgement -> Resolution -> Audit

The current sample keeps this practical:

- a terminal menu creates synthetic hospital scenarios;
- P0-P4 priorities classify the event;
- departments and responder roles are simulated;
- SQLite stores events and an audit trail;
- the simulator runs without microphone/speaker hardware;
- GGWave remains an optional experimental transport;
- message IDs and event states provide a foundation for later routing,
  escalation, web dashboards and interoperability.

## Run the sample

The easiest test is hardware-free:

    python acoustic_bbox.py --test

Run a sample hospital event:

    python acoustic_bbox.py --simulate

View stored events:

    python acoustic_bbox.py --dashboard

Optional acoustic experiment:

    pip install -r requirements.txt
    python acoustic_bbox.py

The acoustic path requires compatible local audio hardware and a working GGWave
Python installation. The simulator does not.

## Tablet development

GitHub Codespaces provides a browser-based VS Code environment with a terminal
and compute, so this repository can be developed and tested from a tablet.
Codespaces is suitable for the simulator/self-test; remote Codespaces should
not be treated as direct access to the tablet's physical microphone/speaker.

## Current sample scope

Categories:
- MEDICAL
- EQUIPMENT
- LOGISTICS
- ENVIRONMENT
- OPERATIONS
- SYSTEM

Priority:
- P0 Critical
- P1 Urgent
- P2 Priority
- P3 Routine
- P4 Informational

Event states:
CREATED -> DISPATCHED -> DELIVERED -> ACKNOWLEDGED -> IN_PROGRESS -> RESOLVED

## Future roadmap

1. Web dashboard
2. Real routing and configurable escalation rules
3. Device registry and authentication
4. Multi-transport abstraction
5. Better acoustic reliability tests
6. Role-based access control
7. FHIR interoperability layer
8. Security/privacy review and controlled real-world validation

The goal is to demonstrate sound software architecture first, then investigate
whether any component is suitable for controlled practical deployment later.
