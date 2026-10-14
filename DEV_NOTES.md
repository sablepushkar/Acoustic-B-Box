# Acoustic-B-Box — development notes

## Packet validation

While checking the WAV decoder, I found that it still expected an older payload identifier while the builder used the current one. I aligned the builder and decoder checks and moved the envelope checks into `validate_decoded_packet`.

The validator checks that the decoded packet is a JSON object, uses the expected payload identifier and contains a non-empty message ID. Tests cover a current packet, an older identifier, a missing ID and non-object values, alongside malformed and oversized packets.

The payload identifier is an internal compatibility field, not a public project release name. Real acoustic delivery between separate devices still needs separate testing.
