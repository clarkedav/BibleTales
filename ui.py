"""
ui.py - Shared colors, drawing helpers and small animation helpers.

Every screen in BibleTales needs the same few things: colors, a way to draw
boxes and text, a way to test mouse clicks, and some confetti for happy
moments. They live here so main.py and guide.py can both import them
without repeating code.
"""

import math
import random

import arcade # pyright: ignore[reportMissingImports]

# ─── COLORS (RGB tuples: red, green, blue from 0 to 255) ──────────────

SKY = (135, 206, 235)
NAVY = (21, 67, 130)
WHITE = (255, 255, 255)
GOLD = (255, 193, 7)
GREEN = (67, 160, 71)
RED = (229, 57, 53)
GRAY = (150, 150, 150)
PANEL = (232, 244, 253)
DARK = (30, 30, 30)
PATH_BROWN = (139, 110, 70)
LOCKED = (120, 125, 140)       # fill color for stages the player cannot open yet

# Colors used by the confetti bursts
CONFETTI_COLORS = [GOLD, GREEN, RED, (66, 165, 245), (186, 104, 200), WHITE]


# ─── BOX DRAWING ──────────────────────────────────────────────────────

def draw_box(cx, cy, width, height, fill, outline=None, border=3):
    """
    Draw a filled rectangle with an optional outline.

    Args:
        cx (float): Center x position
        cy (float): Center y position
        width (float): Box width
        height (float): Box height
        fill (tuple): RGB or RGBA fill color (a 4th number makes it see-through)
        outline (tuple): Optional RGB outline color
        border (int): Outline thickness in pixels
    """
    # Arcade 3 describes rectangles with a Rect object built from a
    # center point (XYWH = x, y, width, height).
    box = arcade.rect.XYWH(cx, cy, width, height)
    arcade.draw_rect_filled(box, fill)
    if outline:
        arcade.draw_rect_outline(box, outline, border)


# ─── TEXT DRAWING ─────────────────────────────────────────────────────

# Creating a Text object is slow, so each unique piece of text is created
# once and stored here. After that we only move it and draw it.
TEXT_CACHE = {}


def draw_label(text, x, y, color=WHITE, size=16, bold=False,
               wrap_width=None, anchor_x="center"):
    """
    Draw text on the screen using a cached arcade.Text object.

    Args:
        text (str): The text to draw
        x (float): X position
        y (float): Y position (the middle of the text)
        color (tuple): RGB text color
        size (int): Font size
        bold (bool): Whether the text is bold
        wrap_width (int): If given, text wraps to this width and is centered
        anchor_x (str): "left", "center" or "right" alignment around x
    """
    # The key identifies "this exact text, drawn this exact way".
    key = (text, color, size, bold, wrap_width, anchor_x)
    label = TEXT_CACHE.get(key)
    if label is None:
        if wrap_width:
            # Wrapped text needs multiline=True and a width to wrap at
            label = arcade.Text(
                text, x, y, color=color, font_size=size, width=wrap_width,
                align="center", bold=bold, anchor_x="center",
                anchor_y="center", multiline=True,
            )
        else:
            label = arcade.Text(
                text, x, y, color=color, font_size=size, bold=bold,
                anchor_x=anchor_x, anchor_y="center",
            )
        TEXT_CACHE[key] = label
    # The same cached text can be drawn in different places
    label.x = x
    label.y = y
    label.draw()


# ─── MOUSE HELPER ─────────────────────────────────────────────────────

def point_in_box(px, py, cx, cy, width, height):
    """
    Check whether a point (such as a mouse click) is inside a box.

    Args:
        px (float): Point x
        py (float): Point y
        cx (float): Box center x
        cy (float): Box center y
        width (float): Box width
        height (float): Box height

    Returns:
        bool: True if the point is inside the box
    """
    return abs(px - cx) <= width / 2 and abs(py - cy) <= height / 2


# ─── HEART ICON ───────────────────────────────────────────────────────

def draw_heart(x, y, size, color):
    """
    Draw a small heart shape (used for the lives display).

    A heart is two circles side by side with a triangle underneath.

    Args:
        x (float): Center x position
        y (float): Center y position
        size (float): Rough size of the heart in pixels
        color (tuple): RGB fill color
    """
    r = size * 0.55                                   # radius of each bump
    arcade.draw_circle_filled(x - r * 0.8, y + r * 0.4, r, color)
    arcade.draw_circle_filled(x + r * 0.8, y + r * 0.4, r, color)
    arcade.draw_triangle_filled(x - r * 1.75, y + r * 0.1,
                                x + r * 1.75, y + r * 0.1,
                                x, y - r * 1.6, color)


# ─── CONFETTI ─────────────────────────────────────────────────────────

class Particle:
    """One piece of confetti that flies out, falls and fades away."""

    def __init__(self, x, y, vx, vy, color, size, life):
        """
        Create a confetti piece.

        Args:
            x (float): Starting x position
            y (float): Starting y position
            vx (float): Horizontal speed in pixels per second
            vy (float): Vertical speed in pixels per second
            color (tuple): RGB color
            size (float): Radius in pixels
            life (float): Seconds before it has fully faded
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self, delta_time):
        """
        Move the piece and pull it down with gravity.

        Args:
            delta_time (float): Seconds since the last frame
        """
        self.vy -= 600 * delta_time           # gravity
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.life -= delta_time

    def is_alive(self):
        """
        Check whether the piece should still be drawn.

        Returns:
            bool: True while it still has life left and is on screen
        """
        return self.life > 0 and self.y > -20

    def draw(self):
        """Draw the piece, fading it out as its life runs down."""
        fade = max(0.0, self.life / self.max_life)
        arcade.draw_circle_filled(self.x, self.y, self.size,
                                  (*self.color[:3], int(255 * fade)))


def spawn_confetti(particles, x, y, count=30):
    """
    Add a burst of confetti to a list of particles.

    Args:
        particles (list): The list the new pieces are added to
        x (float): Burst center x
        y (float): Burst center y
        count (int): Number of pieces
    """
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)       # any direction
        speed = random.uniform(120, 380)
        particles.append(Particle(
            x, y,
            math.cos(angle) * speed,
            math.sin(angle) * speed + 150,           # a bit of upward kick
            random.choice(CONFETTI_COLORS),
            random.uniform(3, 6),
            random.uniform(1.0, 1.8),
        ))
