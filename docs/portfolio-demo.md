# Acoustic-B-Box: portfolio demo

Use synthetic events only. This walkthrough demonstrates the simulator and local checks; it does not certify real audio transport.

## 1. Run the hardware-free check

```bash
python acoustic_bbox.py --test
python acoustic_bbox.py --demo
```

Capture the actual test output and one demo event ID.

## 2. Follow an event

```bash
python acoustic_bbox.py --timeline BX-XXXXXXXX
```

Replace the example ID with one printed by the demo. Explain the event fields, simulated lifecycle and local history. Dashboard device counts are seeded examples, not live devices.

## 3. Optional WAV experiment

Install dependencies from `requirements.txt`, then encode and decode a WAV using an event ID from the local demo. Record whether the decode/validation step passed on the machine used. A local WAV round trip is not the same as delivery between separate devices.

## What this demo establishes

It can demonstrate structured payload validation, simulated delivery states and local event history. It does not establish range, delivery reliability under interference, sender authentication, confidentiality or emergency-service readiness.
