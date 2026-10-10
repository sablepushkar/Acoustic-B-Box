# Acoustic-B-Box — Developer Notes

## A.B.B 2A — event validation and traceability

I am keeping the project as a small operations simulator rather than presenting it as a working hospital alert product. The current useful path is event creation → validation → transport simulation → acknowledgement/resolution → SQLite history and audit timeline.

### Changes in this pass

- Give the project/payload a single visible version label: `A.B.B 2A`.
- Validate event descriptions and source-device identifiers before payload creation.
- Require a non-negative integer for simulated response units; reject booleans as counts.
- Require response roles to be a list of non-empty strings.
- Require event data to be a dictionary that can be serialized as strict JSON (no NaN/Infinity or arbitrary Python objects).
- Add regression tests for the invalid-input cases.

### Verify

```bash
python acoustic_bbox.py --test
python -m unittest discover -s tests -v
python acoustic_bbox.py --demo
```

### Do not overstate

The simulator can demonstrate state transitions, retries, hashing, and local persistence. It cannot prove that audio will reach a real responder, that the message is private, or that an event was clinically interpreted correctly. Those require separate hardware, security, and workflow validation.
