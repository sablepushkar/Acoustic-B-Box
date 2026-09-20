#!/usr/bin/env python3
"""
Acoustic-BBox: emergency data-over-sound prototype.

This prototype demonstrates a small, local, air-gapped-style data channel:
JSON -> GGWave audio -> speaker -> microphone -> GGWave -> JSON.

The medical payload below is MOCK DATA ONLY. Do not use this prototype
with real patient information or as a clinical communication system.
"""

import json
import time

import ggwave
import numpy as np
import sounddevice as sd


SAMPLE_RATE = 48000
BLOCK_SIZE = 1024

# GGWave protocol 1 is the audible-fast protocol in the GGWave examples.
PROTOCOL_ID = 1
TX_VOLUME = 25


def broadcast_emergency_beacon():
    """Encode mock emergency data and play it through the default speaker."""
    mock_medical_data = {
        "patient_id": "MOCK-001",
        "emergency_status": "CRITICAL",
        "vital_signs": {
            "heart_rate_bpm": 118,
            "spo2_percent": 91,
            "temperature_c": 38.2,
        },
    }

    # Compact JSON keeps the acoustic payload small.
    payload = json.dumps(
        mock_medical_data,
        separators=(",", ":"),
    ).encode("utf-8")

    # Create a GGWave context configured for our audio sample rate.
    params = ggwave.getDefaultParameters()
    params.sampleRate = float(SAMPLE_RATE)
    context = ggwave.init(params)

    try:
        # GGWave returns raw 16-bit PCM audio bytes.
        waveform = ggwave.encode(
            context,
            payload,
            PROTOCOL_ID,
            TX_VOLUME,
            SAMPLE_RATE,
        )

        audio = np.frombuffer(waveform, dtype=np.int16)

        print("Broadcasting emergency beacon...")
        print(json.dumps(mock_medical_data, indent=2))
        sd.play(audio, SAMPLE_RATE)
        sd.wait()
        print("Beacon transmission complete.")

    finally:
        ggwave.free(context)


def listen_for_beacon():
    """Listen on the default microphone until a GGWave JSON packet is decoded."""
    params = ggwave.getDefaultParameters()
    params.sampleRate = float(SAMPLE_RATE)
    context = ggwave.init(params)
    decoder_state = ggwave.State()

    print("Listening for an emergency beacon...")
    print("Press Ctrl+C to stop.")

    def callback(indata, frames, time_info, status):
        if status:
            print(f"Audio status: {status}")

        raw_audio = indata[:, 0].astype(np.int16, copy=False).tobytes()

        try:
            decoded = ggwave.decode(context, raw_audio, decoder_state)
        except Exception:
            # Ignore incomplete/noisy chunks and keep listening.
            return

        if decoded:
            try:
                recovered_data = json.loads(decoded.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return

            print("\n=== EMERGENCY BEACON RECEIVED ===")
            print(json.dumps(recovered_data, indent=2))
            print("==================================")
            raise sd.CallbackStop()

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=BLOCK_SIZE,
            callback=callback,
        ):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nListener stopped.")
    finally:
        ggwave.free(context)


if __name__ == "__main__":
    print("Acoustic-BBox")
    print("1 - Broadcast emergency beacon")
    print("2 - Listen for emergency beacon")

    choice = input("Select mode (1/2): ").strip()

    if choice == "1":
        broadcast_emergency_beacon()
    elif choice == "2":
        listen_for_beacon()
    else:
        print("Invalid choice. Please select 1 or 2.")
