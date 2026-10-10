# Acoustic-B-Box — A.B.B 2A

**A small event-communication and delivery-audit prototype**

Acoustic-B-Box models how a structured operational event could move through priority assignment, department routing, transport attempts, acknowledgement, work-in-progress, and resolution. The useful part is the auditable event lifecycle; audio is an optional transport experiment, not the whole system.

## What works in the prototype

- Synthetic event categories and P0–P4 priorities.
- Department/role routing fields and explicit lifecycle transitions.
- SQLite storage for events, transmissions, device status, and audit entries.
- Retry/failure simulation and per-event timeline.
- SHA-256 fingerprint of the canonical payload.
- Terminal dashboard, demo scenarios, and hardware-free self-test.
- Optional GGWave WAV encode/decode path.
- Automated tests and GitHub Actions checks.

## Event path

```text
Create event → validate → canonical payload/hash → transport attempt
      → delivery/failure → acknowledgement → work → resolution
      → persisted event, transmission history, and audit trail
```

## Run it

The core simulator uses the Python standard library:

```bash
python acoustic_bbox.py --test
python acoustic_bbox.py --demo
python acoustic_bbox.py --dashboard
python acoustic_bbox.py --simulate
```

Inspect an event timeline with its event ID:

```bash
python acoustic_bbox.py --timeline BX-XXXXXXXX
```

For the optional audio experiment:

```bash
python -m pip install -r requirements.txt
python acoustic_bbox.py --encode-wav BX-XXXXXXXX --wav-out acoustic_event.wav
python acoustic_bbox.py --decode-wav acoustic_event.wav
```

## A.B.B 2A — what this update focuses on

The update tightens event-boundary validation so malformed descriptions, routing fields, and non-JSON payload data are rejected before persistence or transport. The payload carries the named prototype version so a saved message can be traced back to the code line that produced it.

## Limits that matter

All examples are synthetic. This is not an emergency dispatch product, medical device, or reliable alert channel. A successful simulator run does not establish acoustic range, intelligibility, privacy, interference tolerance, or delivery guarantees on real hardware. The physical audio path still needs controlled testing on actual devices before any operational claim could be made. Do not use real patient data or rely on this for real emergency response.

## Next practical steps

1. Test invalid event fields and payload serialization failures.
2. Add deterministic delivery metrics across repeated simulation runs.
3. Separate transport interfaces further if a second transport is actually implemented.
4. Test audio round trips and failure rates on hardware before making performance claims.
5. Add identity, authorization, and threat modelling before considering networked deployment.

See `DEV_NOTES.md` for the update notes and test commands.
