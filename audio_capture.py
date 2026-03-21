import os
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 44100
DURATION_SECONDS = 10
CHANNELS = 1
OUTPUT_PATH = "audio_files/live_capture.wav"
DEVICE = 0  # Set to USB mic device index if not system default
              # Check available devices: python3 -c "import sounddevice; print(sounddevice.query_devices())"


def record_clip(path: str = OUTPUT_PATH,
                duration: int = DURATION_SECONDS,
                samplerate: int = SAMPLE_RATE,
                device=DEVICE) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=CHANNELS,
        dtype="float32",
        device=device,
        blocking=True,
    )
    sf.write(path, audio, samplerate)
    return path


if __name__ == "__main__":
    print(f"Recording {DURATION_SECONDS}s clip...")
    out = record_clip()
    print(f"Saved to {out}")
