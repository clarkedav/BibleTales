"""
guide.py - Eli, the friendly 2D guide who talks to the player.

Eli is drawn entirely with Arcade shapes (circles, polygons and arcs), so no
image files are needed. He bobs gently, blinks, moves his mouth while he is
talking and shows a happy or sad face when the player answers.

SpeechBubble shows what Eli says with a typewriter effect: the letters
appear one after another, like someone speaking.
"""

import math
import random

import arcade # type: ignore

from ui import (DARK, NAVY, WHITE, GOLD, draw_box)

# ─── WHAT ELI SAYS AFTER AN ANSWER ────────────────────────────────────

GUIDE_CORRECT = [
    "Well done!",
    "Exactly right!",
    "You know your Scripture!",
    "Great answer!",
    "That is correct, keep going!",
]
GUIDE_WRONG = [
    "Not this time, but that is how we learn.",
    "Good try! The answer is waiting in Scripture.",
    "Do not worry, every traveller stumbles.",
    "Almost! Scripture will help you here.",
]
GUIDE_TIMEOUT = [
    "Time ran out!",
    "The time is up. Think a little faster next time.",
]

# ─── ELI'S COLORS ─────────────────────────────────────────────────────

SKIN = (205, 150, 105)
ROBE = (63, 105, 170)
CLOTH = (250, 246, 235)          # white head cloth
BAND = (139, 90, 43)
STAFF = (120, 80, 40)
MOUTH = (120, 40, 40)
CHEEK = (232, 130, 120, 140)


class Guide:
    """An animated cartoon guide drawn from basic shapes."""

    def __init__(self, x, y, scale=1.0):
        """
        Create the guide.

        Args:
            x (float): Center x of the guide's feet
            y (float): Bottom y of the guide's robe
            scale (float): Size multiplier (1.0 is about 160 pixels tall)
        """
        self.x = x
        self.y = y
        self.scale = scale
        self.time = random.uniform(0, 5)    # animation clock (random start)
        self.mood = "idle"                  # "idle", "happy" or "sad"
        self.mood_timer = 0.0               # seconds left before going idle
        self.talking = False                # True while the mouth moves

    def set_mood(self, mood, seconds=1.6):
        """
        Show a mood (happy or sad) for a short time.

        Args:
            mood (str): "happy", "sad" or "idle"
            seconds (float): How long to keep the mood before relaxing
        """
        self.mood = mood
        self.mood_timer = seconds

    def update(self, delta_time, talking=False):
        """
        Advance the animation clock and mood timer.

        Args:
            delta_time (float): Seconds since the last frame
            talking (bool): Whether the guide should move his mouth
        """
        self.time += delta_time
        self.talking = talking
        if self.mood_timer > 0:
            self.mood_timer -= delta_time
            if self.mood_timer <= 0:
                self.mood = "idle"

    def draw(self):
        """Draw the whole character: staff, robe, head, face."""
        s = self.scale
        x = self.x
        # A gentle up and down bob makes the guide feel alive
        y = self.y + math.sin(self.time * 2.2) * 3 * s

        # Shadow on the ground (does not bob)
        arcade.draw_ellipse_filled(self.x, self.y - 3 * s, 100 * s, 14 * s,
                                   (0, 0, 0, 50))

        # Walking staff with a curled top
        arcade.draw_line(x + 58 * s, y - 2 * s, x + 58 * s, y + 128 * s,
                         STAFF, 5 * s)
        arcade.draw_arc_outline(x + 48 * s, y + 128 * s, 20 * s, 20 * s,
                                STAFF, 0, 180, 5 * s)

        # Robe: a four point shape, narrow at the shoulders and wide at the hem
        arcade.draw_polygon_filled(
            [(x - 28 * s, y + 92 * s), (x + 28 * s, y + 92 * s),
             (x + 50 * s, y), (x - 50 * s, y)], ROBE)
        # Golden sash around the waist
        arcade.draw_polygon_filled(
            [(x - 34 * s, y + 55 * s), (x + 34 * s, y + 55 * s),
             (x + 38 * s, y + 43 * s), (x - 38 * s, y + 43 * s)], GOLD)
        # Hand holding the staff
        arcade.draw_circle_filled(x + 58 * s, y + 62 * s, 7 * s, SKIN)

        # Head
        head_y = y + 122 * s
        arcade.draw_circle_filled(x, head_y, 30 * s, SKIN)

        # Head cloth: a half circle on top plus two side flaps and a band
        arcade.draw_arc_filled(x, head_y + 2 * s, 76 * s, 76 * s,
                               CLOTH, 0, 180)
        arcade.draw_polygon_filled(
            [(x - 38 * s, head_y + 2 * s), (x - 26 * s, head_y + 2 * s),
             (x - 30 * s, head_y - 22 * s), (x - 42 * s, head_y - 14 * s)],
            CLOTH)
        arcade.draw_polygon_filled(
            [(x + 38 * s, head_y + 2 * s), (x + 26 * s, head_y + 2 * s),
             (x + 30 * s, head_y - 22 * s), (x + 42 * s, head_y - 14 * s)],
            CLOTH)
        arcade.draw_line(x - 37 * s, head_y + 11 * s, x + 37 * s,
                         head_y + 11 * s, BAND, 5 * s)

        self._draw_face(x, head_y, s)

    def _draw_face(self, x, head_y, s):
        """
        Draw the eyes, cheeks and mouth (the part that changes with mood).

        Args:
            x (float): Center x of the head
            head_y (float): Center y of the head
            s (float): Scale multiplier
        """
        # Blink for a fraction of a second every few seconds
        blinking = (self.time % 3.4) < 0.14
        for side in (-1, 1):
            eye_x = x + side * 11 * s
            if blinking:
                arcade.draw_line(eye_x - 4 * s, head_y - 3 * s,
                                 eye_x + 4 * s, head_y - 3 * s, DARK, 2 * s)
            else:
                arcade.draw_circle_filled(eye_x, head_y - 3 * s, 4 * s, DARK)

        # Rosy cheeks when happy
        if self.mood == "happy":
            for side in (-1, 1):
                arcade.draw_circle_filled(x + side * 19 * s, head_y - 11 * s,
                                          5 * s, CHEEK)

        # Mouth: moving while talking, otherwise it follows the mood
        if self.talking and self.mood != "sad":
            opening = (math.sin(self.time * 16) + 1) / 2    # swings 0 to 1
            arcade.draw_ellipse_filled(x, head_y - 15 * s, 14 * s,
                                       (3 + 9 * opening) * s, MOUTH)
        elif self.mood == "sad":
            arcade.draw_arc_outline(x, head_y - 24 * s, 18 * s, 12 * s,
                                    MOUTH, 20, 160, 3 * s)
        elif self.mood == "happy":
            arcade.draw_arc_outline(x, head_y - 8 * s, 24 * s, 18 * s,
                                    MOUTH, 200, 340, 3 * s)
        else:
            arcade.draw_arc_outline(x, head_y - 9 * s, 16 * s, 10 * s,
                                    MOUTH, 200, 340, 3 * s)


class SpeechBubble:
    """A speech bubble whose text appears one letter at a time."""

    def __init__(self, cx, cy, width, height, font_size=18):
        """
        Create an empty speech bubble.

        Args:
            cx (float): Center x of the bubble box
            cy (float): Center y of the bubble box
            width (float): Box width
            height (float): Box height
            font_size (int): Size of the text
        """
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.full_text = ""         # everything the guide wants to say
        self.shown = 0.0            # how many letters are visible so far
        self.speed = 45.0           # letters per second

        left = cx - width / 2
        top = cy + height / 2
        # One Text object whose words we change as the letters appear
        self.text = arcade.Text(
            "", left + 20, top - 14, color=DARK, font_size=font_size,
            width=width - 40, multiline=True, anchor_x="left",
            anchor_y="top",
        )

    def say(self, message, speed=45.0):
        """
        Start saying something new.

        Args:
            message (str): The words to type out
            speed (float): Letters per second
        """
        self.full_text = message
        self.shown = 0.0
        self.speed = speed
        self.text.text = ""

    def update(self, delta_time):
        """
        Reveal more letters as time passes.

        Args:
            delta_time (float): Seconds since the last frame
        """
        if self.is_done():
            return
        self.shown = min(len(self.full_text),
                         self.shown + self.speed * delta_time)
        visible = self.full_text[:int(self.shown)]
        # Only touch the Text object when something changed (it is slow)
        if visible != self.text.text:
            self.text.text = visible

    def is_done(self):
        """
        Check whether all of the text is visible.

        Returns:
            bool: True once the whole message has been typed
        """
        return int(self.shown) >= len(self.full_text)

    def skip(self):
        """Show all of the text immediately."""
        self.shown = len(self.full_text)
        self.text.text = self.full_text

    def draw(self):
        """Draw the bubble box, its pointer towards the guide, and the text."""
        draw_box(self.cx, self.cy, self.width, self.height, WHITE, NAVY, 3)
        left = self.cx - self.width / 2
        # Small triangle pointing left at the guide
        arcade.draw_triangle_filled(left - 16, self.cy, left + 3,
                                    self.cy + 12, left + 3, self.cy - 12,
                                    WHITE)
        arcade.draw_line(left - 16, self.cy, left + 3, self.cy + 12, NAVY, 3)
        arcade.draw_line(left - 16, self.cy, left + 3, self.cy - 12, NAVY, 3)
        self.text.draw()