"""
audio.py - Sound effects and background music for BibleTales.

SoundManager loads every sound file once when the game starts, then plays
them by name, for example sounds.play("correct"). If a sound file is
missing, or the computer has no audio device, the game keeps working
silently instead of crashing.
"""

from pathlib import Path

import arcade # pyright: ignore[reportMissingImports]

# The sounds folder sits next to this file (created by make_sounds.py)
SOUND_FOLDER = Path(__file__).resolve().parent / "sounds"

# Sound name used in the game  ->  file in the sounds folder
EFFECT_FILES = {
    "click": "click.wav",
    "tick": "tick.wav",
    "correct": "correct.wav",
    "wrong": "wrong.wav",
    "lock": "lock.wav",
    "stage_clear": "stage_clear.wav",
    "victory": "victory.wav",
    "lose": "lose.wav",
}
MUSIC_FILE = "music.wav"
MUSIC_VOLUME = 0.22          # background music is kept quiet on purpose


class SoundManager:
    """Loads and plays all sound effects and the looping music."""

    def __init__(self):
        """Load every sound file listed above."""
        self.effects = {}               # name -> loaded Sound
        self.music = None               # the loaded music Sound
        self.music_player = None        # the player while music is playing
        self.music_on = True            # False after the player presses M

        for name, filename in EFFECT_FILES.items():
            self.effects[name] = self._load(filename)
        self.music = self._load(MUSIC_FILE)

    def _load(self, filename):
        """
        Load one sound file.

        Args:
            filename (str): File name inside the sounds folder

        Returns:
            arcade.Sound: The loaded sound, or None if loading failed
        """
        try:
            return arcade.load_sound(str(SOUND_FOLDER / filename))
        except Exception as error:      # missing file or no audio support
            print(f"[audio] Could not load {filename}: {error}")
            return None

    def play(self, name, volume=0.6):
        """
        Play a sound effect once.

        Args:
            name (str): One of the names in EFFECT_FILES
            volume (float): 0.0 (silent) to 1.0 (full)
        """
        sound = self.effects.get(name)
        if sound is None:
            return
        try:
            arcade.play_sound(sound, volume=volume)
        except Exception as error:
            print(f"[audio] Could not play {name}: {error}")

    def start_music(self):
        """Start the background music loop (does nothing if already on)."""
        if self.music is None or not self.music_on:
            return
        if self.music_player is not None:
            return
        try:
            self.music_player = arcade.play_sound(
                self.music, volume=MUSIC_VOLUME, loop=True)
        except Exception as error:
            print(f"[audio] Could not start music: {error}")

    def stop_music(self):
        """Stop the background music."""
        if self.music_player is not None:
            try:
                arcade.stop_sound(self.music_player)
            except Exception as error:
                print(f"[audio] Could not stop music: {error}")
            self.music_player = None

    def toggle_music(self):
        """Switch the music on or off (the M key calls this)."""
        self.music_on = not self.music_on
        if self.music_on:
            self.start_music()
        else:
            self.stop_music()
