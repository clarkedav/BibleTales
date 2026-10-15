"""
make_sounds.py - Creates all BibleTales sound effects and background music.

Run it once from the project folder:

    python make_sounds.py

It writes WAV files into a "sounds" folder. The sounds are built from
simple sine waves, so they are original and free to use. No extra libraries
are needed, only Python's standard library.

How the sound is made: a sound is a long list of numbers (samples) that
tell the speaker how far to push each 1/22050th of a second. A pure note
is a sine wave, and a chime is a sine wave that slowly fades out.
"""

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 22050                                    # samples per second
OUTPUT_FOLDER = Path(__file__).resolve().parent / "sounds"

# Semitone distance of each note name from C
NOTE_OFFSETS = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
                "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def frequency(note):
    """
    Convert a note name such as "C4" into its pitch in Hertz.

    Args:
        note (str): Note letter(s) followed by an octave number

    Returns:
        float: The frequency in Hz (A4 is 440)
    """
    name, octave = note[:-1], int(note[-1])
    midi_number = 12 * (octave + 1) + NOTE_OFFSETS[name]
    return 440.0 * 2 ** ((midi_number - 69) / 12)


def make_tone(freq, duration, volume=0.5, shape="soft", decay=4.0):
    """
    Create one note as a list of samples.

    Args:
        freq (float): Pitch in Hz
        duration (float): Length in seconds
        volume (float): Loudness from 0 to 1
        shape (str): "sine" (pure), "soft" (warm, with overtones) or
            "square" (buzzy)
        decay (float): How fast the note fades (bigger = faster)

    Returns:
        list: The samples of the note
    """
    count = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(count):
        t = i / SAMPLE_RATE
        phase = 2 * math.pi * freq * t
        if shape == "square":
            value = 0.4 if math.sin(phase) >= 0 else -0.4
        elif shape == "soft":
            # Adding quieter higher notes (overtones) makes it warmer
            value = (math.sin(phase) + 0.3 * math.sin(2 * phase)
                     + 0.1 * math.sin(3 * phase))
        else:
            value = math.sin(phase)
        attack = min(1.0, t / 0.005)                  # avoids a click at start
        release = min(1.0, (duration - t) / 0.02)     # avoids a click at end
        fade = math.exp(-decay * t / duration)        # natural fade out
        samples.append(value * attack * release * fade * volume)
    return samples


def new_buffer(seconds):
    """
    Create silent audio of a given length.

    Args:
        seconds (float): Length in seconds

    Returns:
        list: A list of zeros
    """
    return [0.0] * int(SAMPLE_RATE * seconds)


def mix_into(buffer, samples, start, wrap=False):
    """
    Add (mix) a sound into a buffer starting at a sample position.

    Args:
        buffer (list): The audio being built
        samples (list): The sound to add
        start (int): Sample position where the sound begins
        wrap (bool): If True, anything past the end continues at the
            beginning, which makes background music loop smoothly
    """
    for offset, value in enumerate(samples):
        index = start + offset
        if wrap:
            index %= len(buffer)
        elif index >= len(buffer):
            break
        buffer[index] += value


def save_wav(filename, samples):
    """
    Write samples to a 16-bit mono WAV file.

    Args:
        filename (str): Name of the file inside the sounds folder
        samples (list): The audio samples
    """
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    # Only turn the volume down if the sound would be too loud (clipping)
    peak = max(1.0, max(abs(s) for s in samples))
    frames = b"".join(
        struct.pack("<h", int(max(-1.0, min(1.0, s / peak)) * 30000))
        for s in samples)
    with wave.open(str(OUTPUT_FOLDER / filename), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(frames)
    print(f"Created sounds/{filename}")


def sequence(notes, spacing, duration, volume=0.45, total=None):
    """
    Play a list of notes one after another.

    Args:
        notes (list): Note names such as ["C5", "E5"]
        spacing (float): Seconds between the start of each note
        duration (float): Length of each note
        volume (float): Loudness
        total (float): Total length of the result in seconds

    Returns:
        list: The finished samples
    """
    length = total or (spacing * len(notes) + duration)
    buffer = new_buffer(length)
    for i, note in enumerate(notes):
        mix_into(buffer, make_tone(frequency(note), duration, volume,
                                   "soft", 5.0), int(i * spacing * SAMPLE_RATE))
    return buffer


def build_music():
    """
    Build the calm looping background music.

    It is a gentle harp-like pattern over four chords (C, Am, F, G) played
    twice, about 23 seconds long, and it loops without a gap.

    Returns:
        list: The samples of the music
    """
    beat = 60.0 / 84                           # 84 beats per minute
    bar = beat * 4
    step = beat / 2                            # eighth notes
    # (bass note, four notes of the chord to arpeggiate)
    chords = [("C3", ["C4", "E4", "G4", "C5"]),
              ("A2", ["A3", "C4", "E4", "A4"]),
              ("F2", ["F3", "A3", "C4", "F4"]),
              ("G2", ["G3", "B3", "D4", "G4"])]
    progression = chords * 2
    pattern = [0, 1, 2, 3, 2, 1, 2, 1]         # which chord note to play

    buffer = new_buffer(bar * len(progression))
    for bar_number, (bass, notes) in enumerate(progression):
        bar_start = bar_number * bar
        # Long soft bass note under the whole bar
        mix_into(buffer, make_tone(frequency(bass), bar * 1.05, 0.22,
                                   "soft", 1.2),
                 int(bar_start * SAMPLE_RATE), wrap=True)
        # Eight arpeggio notes over the bar
        for step_number, which in enumerate(pattern):
            start = bar_start + step_number * step
            mix_into(buffer, make_tone(frequency(notes[which]), step * 2.5,
                                       0.18, "soft", 3.0),
                     int(start * SAMPLE_RATE), wrap=True)
    return buffer


def main():
    """Create every sound file in the sounds folder."""
    # Short interface sounds
    save_wav("click.wav", sequence(["A5"], 0, 0.08, 0.5, 0.08))
    save_wav("tick.wav", sequence(["E6"], 0, 0.06, 0.35, 0.06))
    save_wav("lock.wav", sequence(["A2"], 0, 0.25, 0.7, 0.3))

    # Right answer: a bright rising chime
    save_wav("correct.wav", sequence(["C5", "E5", "G5"], 0.09, 0.35))

    # Wrong answer: two low buzzy notes going down
    wrong = new_buffer(0.55)
    mix_into(wrong, make_tone(frequency("G3"), 0.2, 0.35, "square", 2.0), 0)
    mix_into(wrong, make_tone(frequency("D3"), 0.32, 0.35, "square", 3.0),
             int(0.2 * SAMPLE_RATE))
    save_wav("wrong.wav", wrong)

    # Finished a stage: a short happy fanfare
    save_wav("stage_clear.wav",
             sequence(["C5", "E5", "G5", "C6"], 0.13, 0.5, 0.45))

    # Won the whole journey: fanfare followed by a held chord
    victory = sequence(["C5", "E5", "G5", "C6", "E6"], 0.15, 0.5, 0.4, 3.0)
    for note in ("C5", "E5", "G5", "C6"):
        mix_into(victory, make_tone(frequency(note), 2.0, 0.22, "soft", 2.0),
                 int(0.85 * SAMPLE_RATE))
    save_wav("victory.wav", victory)

    # Lost the journey: slow falling notes
    save_wav("lose.wav",
             sequence(["G4", "E4", "D4", "C4"], 0.38, 0.8, 0.45, 2.4))

    # Background music (takes a few seconds to calculate)
    print("Building music, please wait...")
    save_wav("music.wav", build_music())
    print("Done! All sounds are in the sounds folder.")


if __name__ == "__main__":
    main()
