# Acoustic-B-Box

[![Tests](https://github.com/sablepushkar/Acoustic-B-Box/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/sablepushkar/Acoustic-B-Box/actions/workflows/tests.yml)

Acoustic-B-Box is my experiment with moving a structured event through a simple delivery workflow. It currently has a software simulator and an optional GGWave-based WAV encode/decode path.

## What it includes

- Synthetic event types with P0–P4 priority labels.
- Department and role routing fields with lifecycle transitions.
- SQLite storage for events, transmission attempts, device-status examples and history entries.
- Retry/failure simulation and event timelines.
- A SHA-256 fingerprint of the canonical payload.
- A terminal dashboard, demo scenarios and a hardware-free self-test.
- Optional audio encoding/decoding and automated tests.

Device counts in the dashboard are seeded simulator data, not live availability.

## Quick run

```bash
python acoustic_bbox.py --test
python acoustic_bbox.py --demo
python acoustic_bbox.py --dashboard
python acoustic_bbox.py --simulate
```

To inspect an event timeline, use an ID printed by a demo run:

```bash
python acoustic_bbox.py --timeline BX-XXXXXXXX
```

## Optional WAV path

```bash
python -m pip install -r requirements.txt
python acoustic_bbox.py --encode-wav BX-XXXXXXXX --wav-out acoustic_event.wav
python acoustic_bbox.py --decode-wav acoustic_event.wav
```

The event ID must exist in the local demo data. See the [portfolio demo guide](docs/portfolio-demo.md) and [transport validation notes](docs/transport-validation.md) for what to capture and what remains untested.

## Limits

A passing simulator run does not prove real acoustic delivery. Usable range, interference handling, privacy and successful delivery between physical devices have not been established. A hash can detect payload changes but does not authenticate a sender. This is a learning prototype, not an emergency dispatch product or medical device. Use synthetic data only and do not rely on it for real emergencies.

The project is also included in [Saturnum](https://github.com/sablepushkar/Saturnum), where I run combined checks with VIREON.
