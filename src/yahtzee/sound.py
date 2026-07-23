"""Sound effects module for Yahtzee using standard library audio generation."""

import io
import math
import os
import platform
import struct
import subprocess
import tempfile
import threading
import wave


def _generate_wav(samples: list[float], sample_rate: int = 22050) -> bytes:
    """Convert floating point sample list (-1.0 to 1.0) into WAV format bytes."""
    byte_io = io.BytesIO()
    with wave.open(byte_io, "wb") as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        packed = bytearray()
        for sample in samples:
            # Clamp sample to [-1.0, 1.0]
            val = max(-1.0, min(1.0, sample))
            int_val = int(val * 32767)
            packed.extend(struct.pack("<h", int_val))
        wav.writeframes(packed)
    return byte_io.getvalue()


def _create_roll_sound() -> bytes:
    """Generate a deep, warm casino felt table dice tumbling sound."""
    rate = 22050
    duration = 0.42
    total_samples = int(rate * duration)
    samples = [0.0] * total_samples
    import random

    # Deep felt table dice tumbling impacts (warm low-mid frequency thuds)
    impacts = [
        (0.0, 380, 0.45),
        (0.06, 320, 0.40),
        (0.12, 440, 0.35),
        (0.19, 290, 0.30),
        (0.27, 350, 0.22),
        (0.35, 260, 0.15),
    ]

    for start_t, freq, vol in impacts:
        start_sample = int(start_t * rate)
        tap_len = int(rate * 0.04)
        for s in range(tap_len):
            target_idx = start_sample + s
            if target_idx < total_samples:
                dt = s / rate
                # Deep felt thud envelope
                env = math.exp(-70 * dt)
                # Warm resonant body + subtle felt friction
                body = math.sin(2 * math.pi * freq * dt) + 0.3 * math.sin(
                    2 * math.pi * (freq * 0.5) * dt
                )
                felt_friction = (random.random() * 2 - 1) * 0.1 * math.exp(-120 * dt)
                samples[target_idx] += (body + felt_friction) * env * vol

    return _generate_wav(samples, rate)


def _create_hold_sound() -> bytes:
    """Generate a crisp click sound for toggling dice hold."""
    rate = 22050
    duration = 0.06
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / rate
        env = math.exp(-60 * t)
        freq = 800 + 400 * math.sin(2 * math.pi * 30 * t)
        samples.append(math.sin(2 * math.pi * freq * t) * env)
    return _generate_wav(samples, rate)


def _create_score_sound() -> bytes:
    """Generate a pleasant two-tone chime for scoring."""
    rate = 22050
    duration = 0.2
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / rate
        env = math.exp(-8 * t)
        freq = 523.25 if t < 0.1 else 659.25  # C5 then E5
        samples.append(0.7 * math.sin(2 * math.pi * freq * t) * env)
    return _generate_wav(samples, rate)


def _create_win_sound() -> bytes:
    """Generate a fanfare chord for game victory."""
    rate = 22050
    duration = 0.4
    total_samples = int(rate * duration)
    samples = []
    notes = [523.25, 659.25, 783.99, 1046.50]  # C Major chord (C5, E5, G5, C6)
    for i in range(total_samples):
        t = i / rate
        env = math.exp(-5 * t)
        val = sum(math.sin(2 * math.pi * note * t) for note in notes) / len(notes)
        samples.append(0.8 * val * env)
    return _generate_wav(samples, rate)


class SoundManager:
    """Manages audio playback for game events."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._sound_files: dict[str, str] = {}
        self._system = platform.system()
        self._init_sounds()

    def _init_sounds(self):
        """Pre-render sound WAV files."""
        generators = {
            "roll": _create_roll_sound,
            "hold": _create_hold_sound,
            "score": _create_score_sound,
            "win": _create_win_sound,
        }
        for name, gen_fn in generators.items():
            try:
                wav_bytes = gen_fn()
                tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                tf.write(wav_bytes)
                tf.close()
                self._sound_files[name] = tf.name
            except Exception:
                pass

    def play(self, sound_name: str):
        """Play a pre-rendered sound asynchronously."""
        if not self.enabled or sound_name not in self._sound_files:
            return

        def _play_thread():
            try:
                filepath = self._sound_files[sound_name]
                if self._system == "Windows":
                    import winsound

                    winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
                elif self._system == "Darwin":  # macOS
                    subprocess.run(
                        ["afplay", filepath],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                elif self._system == "Linux":
                    res = subprocess.run(
                        ["aplay", "-q", filepath],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    if res.returncode != 0:
                        subprocess.run(
                            ["paplay", filepath],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
            except Exception:
                pass

        threading.Thread(target=_play_thread, daemon=True).start()

    def cleanup(self):
        """Remove temporary sound files."""
        for path in self._sound_files.values():
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass

    def __del__(self):
        self.cleanup()
