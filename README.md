# Acoustic-B-Box

## v0.3 — compact hospital-operations communication prototype

Acoustic-B-Box is a learning project for structured, event-based notifications.
The sample models a small hospital operations workflow and keeps GGWave as an
optional acoustic transport instead of making sound the whole application.

**Prototype boundary:** all medical examples are synthetic. Response-unit and
role fields are simulation parameters, not clinical guidance. Do not use this
repository with real patient information or for real emergency decision-making.

## What the sample demonstrates

```text
Event → Priority → Department → Transport → Delivery → Acknowledgement
      → In Progress → Resolution → Audit trail
```

The current sample includes:

- six synthetic event categories and P0–P4 priorities;
- simple department/role routing data;
- SQLite persistence for events, transmissions, devices and audit records;
- explicit lifecycle validation;
- retry + failure demonstration;
- SHA-256 payload integrity fingerprint;
- terminal operations dashboard and event timeline;
- hardware-free self-test and six-scenario demo mode;
- optional GGWave WAV encode/decode path;
- GitHub Actions CI and a Codespaces-ready Python environment.

## Run without extra packages

```bash
python acoustic_bbox.py --test
python acoustic_bbox.py --demo
python acoustic_bbox.py --dashboard
```

Run one scenario interactively:

```bash
python acoustic_bbox.py --simulate
```

Inspect a particular event:

```bash
python acoustic_bbox.py --timeline BX-XXXXXXXX
```

## Optional acoustic experiment

Install the optional GGWave package:

```bash
pip install -r requirements.txt
```

The sample can create a normal mono 16-bit WAV containing the GGWave payload.
That keeps acoustic testing separate from the hospital simulation itself and
makes the result easy to play/record on physical devices.

First run a demo, note an event ID, then:

```bash
python acoustic_bbox.py --encode-wav BX-XXXXXXXX --wav-out acoustic_event.wav
python acoustic_bbox.py --decode-wav acoustic_event.wav
```

The GGWave project describes itself as a small FSK-based data-over-sound
library with audible and ultrasound protocols and error correction. This
repository uses one audible protocol for the sample and keeps the transport
replaceable. See the upstream project for the full protocol set and limits.

## Tablet workflow

GitHub Codespaces can provide the Python runtime and terminal through a browser,
including on a tablet. The simulator/self-test can therefore be developed and
run without a local laptop. The Codespace itself should not be assumed to have
direct access to the tablet's physical microphone or speaker.

## Architecture direction

The project is intentionally small now, but the boundaries are future-friendly:

```text
Application events
       ↓
Event model + lifecycle
       ↓
Transport adapter
  ├─ Simulator
  └─ GGWave WAV
       ↓
Persistence + audit
       ↓
Future web UI / routing / authentication / interoperability
```

A later version can add LAN/Wi-Fi transport, a web dashboard, configurable
escalation rules, stronger identity/security controls, and eventually a
healthcare interoperability adapter without replacing the basic event model.

## Testing philosophy

The repository separates what can be proven locally from what needs physical
hardware. Core logic is covered by automated tests and GitHub Actions. Acoustic
performance must be validated separately with actual audio hardware and controlled
experiments before any real-world use is considered.
