"""
main.py - BibleTales

A Bible adventure quiz game built with Python Arcade.

HOW THE GAME WORKS
The journey has two sections, each with its own roadmap:
  * Bible Stories  - a story, then quiz questions about it.
  * Memory Verses  - fill in the missing words of well known verses.
After every TWO Bible stories, one Memory Verse stage opens. Only the current
stage and the stages already finished are open; the rest stay locked.
Finished stages can be replayed in practice mode.

Each stage asks questions against a countdown timer, and later stages are
harder because the time per question gets shorter. A wrong answer or a
timeout costs a life. The game never reveals the answer. Instead, Eli the
guide sends the player to a Bible chapter to read, then the player comes
back and tries again. Missed chapters are collected in a study list that is
shown at the end.

HOW THE CODE IS ORGANIZED
* Settings and map layout   - constants and the position of each stage
* Drawing helpers           - sky, land, top bar, icons
* GameState                 - the player's lives, score and progress
* Sprites                   - the Avatar and Cloud objects that move
* Views (screens)           - Menu, Map, Story, Quiz, Result
* Data validation and main  - check the data, then open the window
"""

import math
import random

import arcade # type: ignore

from audio import SoundManager
from extra_questions import build_journey
from guide import (Guide, SpeechBubble,
                   GUIDE_CORRECT, GUIDE_WRONG, GUIDE_TIMEOUT)
from memory_verses import add_memory_verse_stages
from questions import LOCATIONS as BASE_LOCATIONS
from ui import (NAVY, WHITE, GOLD, GREEN, RED, GRAY, PANEL, DARK,
                PATH_BROWN, LOCKED, draw_box, draw_label, point_in_box,
                draw_heart, spawn_confetti)

# The full journey in order: Bible stories with a memory verse stage after
# every second story. Each stage knows its "section" and its "number".
LOCATIONS = add_memory_verse_stages(build_journey(BASE_LOCATIONS))

# ─── SETTINGS ─────────────────────────────────────────────────────────

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "BibleTales"

STARTING_LIVES = 3          # chances for the WHOLE journey (not per stage)
MAX_LIVES = 5               # a perfect stage earns a life, up to this limit
QUESTIONS_PER_PLAY = 8      # questions asked per stage, picked at random
                            # (set to 100 to ask every question in a stage)
AVATAR_SPEED = 260          # pixels per second when travelling on the map
FEEDBACK_CORRECT_SECONDS = 1.8   # how long "correct" is shown
FEEDBACK_WRONG_SECONDS = 5.0     # wrong answers stay longer so the reading
                                 # hint can be read (ENTER skips ahead)
NODE_RADIUS = 19            # size of each stage marker on the map

# Names of the two sections, shown on tabs, the top bar and by Eli
SECTION_NAMES = {"story": "Bible Stories", "verse": "Memory Verses"}
SECTION_SINGULAR = {"story": "Bible Story", "verse": "Memory Verse"}

# Which stages (by position in LOCATIONS) belong to each section
SECTION_INDEXES = {"story": [], "verse": []}
for _position, _stage in enumerate(LOCATIONS):
    SECTION_INDEXES[_stage["section"]].append(_position)


def reading_hint(read):
    """
    Build the sentence that sends the player back to the Bible.

    The game never gives the answer. It names a whole chapter so the player
    has to open the Bible and read for themselves.

    Args:
        read (str): The chapter(s) to read, for example "Genesis 1"

    Returns:
        str: The instruction shown in Eli's speech bubble
    """
    return (f"Open your Bible and read {read} from start to finish, "
            "then come back and try again.")


# ─── MAP LAYOUT ───────────────────────────────────────────────────────

def compute_positions(count):
    """
    Work out where each stage marker sits on one section's roadmap.

    The stages are spread evenly from left to right and wave up and down
    like a winding road. Because the positions are calculated, adding more
    stages to the data never needs any change here.

    Args:
        count (int): Number of stages in the section

    Returns:
        list: One (x, y) tuple per stage
    """
    positions = []
    left, right = 70, SCREEN_WIDTH - 70
    for i in range(count):
        fraction = i / max(1, count - 1)          # 0.0 for first, 1.0 for last
        x = left + (right - left) * fraction
        y = 340 + 110 * math.sin(i * 0.95)        # wavy road
        positions.append((x, y))
    return positions


# NODE_POSITIONS[n] is where stage number n (in LOCATIONS) is drawn. Each
# section gets its own roadmap, so positions are worked out per section.
NODE_POSITIONS = [None] * len(LOCATIONS)
for _section, _indexes in SECTION_INDEXES.items():
    for _position, _point in zip(_indexes, compute_positions(len(_indexes))):
        NODE_POSITIONS[_position] = _point

# Hills that make up the ground: (center x, center y, radius)
HILL_SHAPES = [(150, -90, 330), (520, -140, 380), (900, -80, 330)]
# x positions of the trees on the hills
TREE_XS = [40, 105, 250, 420, 600, 770, 900, 965]

# ─── LOOK OF EACH SECTION ─────────────────────────────────────────────
# Bible Stories use a bright daytime scene. Memory Verses use a calm evening
# scene with stars and a moon, so the two sections feel different.

THEMES = {
    "story": {
        "sky_top": (80, 160, 230), "sky_bottom": (210, 235, 250),
        "night": False,
        "mountain": (146, 165, 196), "snow": WHITE,
        "hills": [(112, 184, 98), (98, 170, 84), (120, 190, 100)],
        "river": (90, 160, 230),
        "tree_dark": (40, 120, 60), "tree_light": (52, 140, 72),
        "trunk": (110, 75, 45),
    },
    "verse": {
        "sky_top": (22, 24, 76), "sky_bottom": (238, 142, 112),
        "night": True,
        "mountain": (84, 74, 128), "snow": (214, 204, 238),
        "hills": [(54, 100, 94), (44, 88, 88), (60, 106, 98)],
        "river": (96, 132, 210),
        "tree_dark": (24, 72, 60), "tree_light": (34, 90, 72),
        "trunk": (70, 50, 40),
    },
}
SKY_BANDS = 10

# A fixed set of stars (x, y, twinkle offset) for the evening scene
_star_random = random.Random(7)
STARS = [(_star_random.uniform(0, SCREEN_WIDTH),
          _star_random.uniform(300, 630),
          _star_random.uniform(0, 6.28)) for _ in range(45)]


# ─── DRAWING HELPERS ──────────────────────────────────────────────────

def ground_height(x):
    """
    Find how high the ground is at a given x position.

    Each hill is a big circle, so the surface height is the top of
    whichever circle is highest at that x. Used to plant trees on the ground.

    Args:
        x (float): Horizontal position

    Returns:
        float: The y position of the ground surface
    """
    best = 0
    for cx, cy, radius in HILL_SHAPES:
        if abs(x - cx) < radius:
            best = max(best, cy + math.sqrt(radius ** 2 - (x - cx) ** 2))
    return best


def band_color(index, theme):
    """
    Get the color of one horizontal band of the sky gradient.

    Args:
        index (int): Band number, 0 at the top of the screen
        theme (str): "story" or "verse"

    Returns:
        tuple: An (r, g, b) color between the top and bottom sky colors
    """
    palette = THEMES[theme]
    mix = index / (SKY_BANDS - 1)
    top, bottom = palette["sky_top"], palette["sky_bottom"]
    return tuple(int(top[k] + (bottom[k] - top[k]) * mix) for k in range(3))


def draw_sky(t, theme="story"):
    """
    Draw the sky gradient and either the turning sun or stars and a moon.

    Args:
        t (float): Animation time in seconds (spins rays, twinkles stars)
        theme (str): "story" for daytime, "verse" for evening
    """
    # The sky is ten horizontal bands blending from top color to horizon color
    band_height = SCREEN_HEIGHT / SKY_BANDS
    for i in range(SKY_BANDS):
        top = SCREEN_HEIGHT - i * band_height
        draw_box(SCREEN_WIDTH / 2, top - band_height / 2, SCREEN_WIDTH,
                 band_height + 1, band_color(i, theme))

    if THEMES[theme]["night"]:
        # Twinkling stars
        for sx, sy, phase in STARS:
            alpha = int(170 + 85 * math.sin(t * 2 + phase))
            arcade.draw_circle_filled(sx, sy, 2, (255, 255, 255, alpha))
        # A pale moon with a few craters
        arcade.draw_circle_filled(880, 500, 34, (250, 240, 205))
        for cx, cy, r in ((868, 510, 7), (893, 492, 5), (880, 478, 4)):
            arcade.draw_circle_filled(cx, cy, r, (232, 222, 188))
    else:
        # Sun with 12 rays that rotate slowly
        sun_x, sun_y = 880, 500
        for k in range(12):
            angle = t * 0.3 + k * (math.pi * 2 / 12)
            arcade.draw_line(sun_x + math.cos(angle) * 42,
                             sun_y + math.sin(angle) * 42,
                             sun_x + math.cos(angle) * 62,
                             sun_y + math.sin(angle) * 62, (255, 214, 79), 4)
        arcade.draw_circle_filled(sun_x, sun_y, 34, (255, 213, 79))


def draw_land(t, theme="story"):
    """
    Draw mountains, rolling hills, a flowing river and trees.

    Args:
        t (float): Animation time in seconds (makes the river wave)
        theme (str): "story" for daytime colors, "verse" for evening colors
    """
    palette = THEMES[theme]

    # Far mountains with snowy tops (back layer)
    mountains = [(130, 390), (360, 330), (640, 350), (880, 400)]
    for mx, peak in mountains:
        arcade.draw_triangle_filled(mx - 160, 200, mx + 160, 200, mx, peak,
                                    palette["mountain"])
        arcade.draw_triangle_filled(mx - 28, peak - 42, mx + 28, peak - 42,
                                    mx, peak, palette["snow"])

    # Hills (front layer)
    for (cx, cy, radius), color in zip(HILL_SHAPES, palette["hills"]):
        arcade.draw_circle_filled(cx, cy, radius, color)

    # River: short line pieces following a sine wave, shifting over time
    previous = None
    for x in range(0, SCREEN_WIDTH + 40, 40):
        y = 170 + 12 * math.sin(x / 60 + t * 0.8)
        if previous:
            arcade.draw_line(previous[0], previous[1], x, y,
                             palette["river"], 10)
        previous = (x, y)

    # Trees: brown trunk with two green triangles, standing on the ground
    for x in TREE_XS:
        base = ground_height(x) - 6
        draw_box(x, base + 10, 8, 20, palette["trunk"])
        arcade.draw_triangle_filled(x - 18, base + 18, x + 18, base + 18,
                                    x, base + 58, palette["tree_dark"])
        arcade.draw_triangle_filled(x - 14, base + 38, x + 14, base + 38,
                                    x, base + 70, palette["tree_light"])


def draw_top_bar(state, title):
    """
    Draw the blue bar at the top: lives (hearts), title, score, music hint.

    Args:
        state (GameState): The current game state
        title (str): Text shown in the middle of the bar
    """
    draw_box(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 35, SCREEN_WIDTH, 70, NAVY)

    # One heart slot per possible life: red = life left, dim = empty
    for slot in range(MAX_LIVES):
        color = RED if slot < state.lives else (70, 90, 130)
        draw_heart(34 + slot * 34, SCREEN_HEIGHT - 33, 14, color)

    draw_label(title, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 35, GOLD, 24, True)
    draw_label(f"Score: {state.score}", SCREEN_WIDTH - 25,
               SCREEN_HEIGHT - 28, WHITE, 20, True, anchor_x="right")
    hint = "Music: ON (M)" if state.sounds.music_on else "Music: OFF (M)"
    draw_label(hint, SCREEN_WIDTH - 25, SCREEN_HEIGHT - 55,
               (200, 215, 240), 11, False, anchor_x="right")


def draw_padlock(x, y):
    """
    Draw a small padlock icon on a locked stage.

    Args:
        x (float): Center x
        y (float): Center y
    """
    draw_box(x, y - 3, 14, 11, DARK)                          # lock body
    arcade.draw_arc_outline(x, y + 3, 10, 12, DARK, 0, 180, 2)  # shackle


def draw_book(x, y, fill):
    """
    Draw a small closed book, the marker for Memory Verse stages.

    Args:
        x (float): Center x
        y (float): Center y
        fill (tuple): Cover color
    """
    draw_box(x, y, 30, 36, fill, WHITE, 3)                    # cover
    arcade.draw_line(x - 8, y - 16, x - 8, y + 16, (0, 0, 0, 80), 3)  # spine


# ─── GAME STATE ───────────────────────────────────────────────────────

class GameState:
    """Stores the player's progress so every screen can share it."""

    def __init__(self):
        """Create the sound system and a fresh game."""
        self.sounds = SoundManager()   # created once, shared by every screen
        self.reset()

    def reset(self):
        """Reset lives, score and progress to begin a new journey."""
        self.lives = STARTING_LIVES    # lives are shared across all stages
        self.score = 0
        self.level_index = 0           # the furthest stage that is unlocked
        self.correct_answers = 0
        self.questions_answered = 0    # counts real play only, not practice
        self.study_list = []           # chapters the player should read


# ─── MOVEABLE OBJECTS (SPRITES) ───────────────────────────────────────

class Avatar(arcade.SpriteCircle):
    """The golden traveller icon that walks between stages on the map."""

    def __init__(self, x, y):
        """
        Create the avatar at a starting position.

        Args:
            x (float): Starting x position
            y (float): Starting y position
        """
        super().__init__(15, GOLD)     # a gold circle of radius 15
        self.center_x = x
        self.center_y = y
        self.target_x = x              # where the avatar is walking to
        self.target_y = y

    def set_target(self, x, y):
        """
        Choose the point the avatar should walk towards.

        Args:
            x (float): Target x position
            y (float): Target y position
        """
        self.target_x = x
        self.target_y = y

    def has_arrived(self):
        """
        Check whether the avatar has reached its target.

        Returns:
            bool: True when the avatar is at the target position
        """
        return (self.center_x == self.target_x
                and self.center_y == self.target_y)

    def update_position(self, delta_time):
        """
        Move the avatar a small step towards its target.

        Args:
            delta_time (float): Seconds since the last frame
        """
        dx = self.target_x - self.center_x
        dy = self.target_y - self.center_y
        distance = math.hypot(dx, dy)           # straight line distance
        step = AVATAR_SPEED * delta_time        # how far we may move now

        if distance <= step:
            # Close enough: snap to the target so we stop exactly there
            self.center_x = self.target_x
            self.center_y = self.target_y
        else:
            # Move along the line, split into x and y parts
            self.center_x += dx / distance * step
            self.center_y += dy / distance * step


class Cloud(arcade.SpriteCircle):
    """A soft white cloud that drifts slowly across the sky."""

    def __init__(self):
        """Create a cloud with a random size, height and speed."""
        super().__init__(random.randint(28, 45), (255, 255, 255, 150))
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = random.randint(380, 590)
        self.speed = random.randint(15, 40)

    def drift(self, delta_time):
        """
        Move the cloud to the right and wrap around the screen.

        Args:
            delta_time (float): Seconds since the last frame
        """
        self.center_x += self.speed * delta_time
        if self.center_x > SCREEN_WIDTH + 60:
            self.center_x = -60                 # re-enter from the left


def make_clouds(count):
    """
    Build a sprite list filled with drifting clouds.

    Args:
        count (int): How many clouds to create

    Returns:
        arcade.SpriteList: The list of cloud sprites
    """
    clouds = arcade.SpriteList()
    for _ in range(count):
        clouds.append(Cloud())
    return clouds


# ─── BASE SCREEN ──────────────────────────────────────────────────────

class BaseView(arcade.View):
    """Shared behavior for every screen: game state and the M (music) key."""

    def __init__(self, state):
        """
        Store the shared game state.

        Args:
            state (GameState): The shared game state
        """
        super().__init__()
        self.state = state
        self.time = 0.0       # animation clock used by sky, sun and river

    def handle_global_key(self, key):
        """
        Handle keys that work on every screen.

        Args:
            key (int): The key that was pressed

        Returns:
            bool: True if the key was used here (so the screen can ignore it)
        """
        if key == arcade.key.M:
            self.state.sounds.toggle_music()
            return True
        return False


# ─── MENU SCREEN ──────────────────────────────────────────────────────

class MenuView(BaseView):
    """The title screen with the Start button and a welcome from Eli."""

    def __init__(self, state):
        """
        Set up the menu, the clouds, the guide and his welcome message.

        Args:
            state (GameState): The shared game state
        """
        super().__init__(state)
        self.clouds = make_clouds(6)
        self.button = (SCREEN_WIDTH / 2, 290, 300, 70)   # cx, cy, width, height
        self.guide = Guide(110, 14, 0.8)
        self.bubble = SpeechBubble(560, 70, 720, 104, 17)
        self.bubble.say(
            "Welcome, traveller! I am Eli. Walk the Bible stories with me "
            "and learn the verses by heart. When you miss one, I will send "
            "you back to Scripture to read.")

    def on_show_view(self):
        """Start the background music when the menu first appears."""
        self.state.sounds.start_music()

    def on_update(self, delta_time):
        """Animate the clouds, guide and speech bubble each frame."""
        self.time += delta_time
        for cloud in self.clouds:
            cloud.drift(delta_time)
        self.bubble.update(delta_time)
        self.guide.update(delta_time, talking=not self.bubble.is_done())

    def on_draw(self):
        """Draw the scenery, title, start button, instructions and Eli."""
        self.window.clear(color=(135, 206, 235))
        draw_sky(self.time)
        self.clouds.draw()
        draw_land(self.time)

        draw_label("BibleTales", SCREEN_WIDTH / 2, 480, NAVY, 64, True)
        draw_label("A Journey Through Scripture", SCREEN_WIDTH / 2, 410,
                   DARK, 24)

        draw_box(*self.button, NAVY, WHITE)
        draw_label("START JOURNEY", self.button[0], self.button[1],
                   WHITE, 22, True)

        draw_box(SCREEN_WIDTH / 2, 198, 660, 60, PANEL, NAVY, 2)
        draw_label("Click the button or press ENTER", SCREEN_WIDTH / 2,
                   210, DARK, 15)
        draw_label(f"You have {STARTING_LIVES} lives for the whole journey. "
                   "Press M to turn the music on or off.",
                   SCREEN_WIDTH / 2, 182, DARK, 13)

        self.guide.draw()
        self.bubble.draw()

    def start_game(self):
        """Reset the game state and open the map at the first stage."""
        self.state.sounds.play("click")
        self.state.reset()
        self.window.show_view(MapView(self.state, 0, 0))

    def on_mouse_press(self, x, y, button, modifiers):
        """Start the game when the Start button is clicked."""
        if point_in_box(x, y, *self.button):
            self.start_game()

    def on_key_press(self, key, modifiers):
        """Start the game when ENTER or SPACE is pressed."""
        if self.handle_global_key(key):
            return
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            self.start_game()


# ─── MAP SCREEN ───────────────────────────────────────────────────────

class MapView(BaseView):
    """
    The journey map, with one roadmap per section (tabs at the top).

    Finished stages are green, the current stage is gold and pulsing, and
    later stages are gray with a padlock. Bible Stories are circles and
    Memory Verses are little books. The player can click or use the arrow
    keys to move to any stage that is open, then press ENTER to play it.
    Press TAB or click a tab to switch between the two roadmaps.
    """

    def __init__(self, state, from_index, to_index, message=None):
        """
        Set up the map and the avatar's walk.

        Args:
            state (GameState): The shared game state
            from_index (int): Stage the avatar starts at
            to_index (int): Stage the avatar walks to (and has selected)
            message (str): Optional words for Eli to say on arrival
        """
        super().__init__(state)
        self.section = LOCATIONS[to_index]["section"]   # roadmap on show
        self.to_index = to_index
        self.hover_index = None            # stage under the mouse pointer
        self.arrival_pending = False       # True while walking to a new stage
        self.clouds = make_clouds(5)

        # Tabs: cx, cy, width, height
        self.tabs = {"story": (150, 545, 250, 34),
                     "verse": (420, 545, 250, 34)}

        # The avatar starts at one stage and walks to the other. When the
        # next stage is in the other section, it walks in from the left edge.
        end = NODE_POSITIONS[to_index]
        if LOCATIONS[from_index]["section"] == self.section:
            start = NODE_POSITIONS[from_index]
        else:
            start = (20, end[1])
        self.avatar = Avatar(*start)
        self.avatar.set_target(*end)
        self.avatar_list = arcade.SpriteList()
        self.avatar_list.append(self.avatar)

        self.guide = Guide(80, 14, 0.7)
        self.bubble = SpeechBubble(560, 72, 740, 104, 17)
        if message:
            self.bubble.say(message)
        else:
            self.announce_arrival()

    def is_open(self, index):
        """
        Check whether a stage can be played.

        Args:
            index (int): Position of the stage in LOCATIONS

        Returns:
            bool: True for finished stages and the current stage
        """
        return index <= self.state.level_index

    def locked_text(self, index):
        """
        Explain how many stages must be finished before a stage opens.

        Args:
            index (int): Position of a locked stage

        Returns:
            str: A sentence for Eli to say
        """
        left = index - self.state.level_index
        plural = "s" if left != 1 else ""
        return f"It is locked. Finish {left} more stage{plural} to open it."

    def announce_arrival(self):
        """Have Eli describe the selected stage and what the player can do."""
        location = LOCATIONS[self.to_index]
        if self.to_index > self.state.level_index:
            action = self.locked_text(self.to_index)
        elif self.to_index < self.state.level_index:
            action = "You finished this one. Press ENTER to practise it."
        else:
            action = "Press ENTER or click the stage again to begin."
        label = f"{SECTION_SINGULAR[self.section]} {location['number']}"
        self.bubble.say(f"{label}: {location['name']} "
                        f"({location['reference']}). {action}")

    def node_at(self, x, y):
        """
        Find which stage marker (if any) is at a screen position.

        Only the roadmap on show is checked.

        Args:
            x (float): Mouse x
            y (float): Mouse y

        Returns:
            int: The stage index, or None if no marker is there
        """
        for index in SECTION_INDEXES[self.section]:
            nx, ny = NODE_POSITIONS[index]
            if math.hypot(x - nx, y - ny) <= NODE_RADIUS + 6:
                return index
        return None

    def travel_to(self, index):
        """
        Send the avatar walking to an open stage.

        Args:
            index (int): The stage to walk to (must not be locked)
        """
        self.to_index = index
        self.avatar.set_target(*NODE_POSITIONS[index])
        self.arrival_pending = True
        self.state.sounds.play("click")
        self.bubble.say(f"Off we go to {LOCATIONS[index]['name']}!", 70)

    def show_locked_message(self, index):
        """
        Play the lock sound and have a saddened Eli explain the rule.

        Args:
            index (int): The locked stage the player tried to open
        """
        self.state.sounds.play("lock")
        self.guide.set_mood("sad", 1.5)
        self.bubble.say(f"{LOCATIONS[index]['name']}: "
                        f"{self.locked_text(index)}", 70)

    def switch_section(self, section):
        """
        Show the other roadmap, selecting the furthest open stage there.

        Args:
            section (str): "story" or "verse"
        """
        indexes = SECTION_INDEXES[section]
        if section == self.section or not indexes:
            return
        open_stages = [i for i in indexes if self.is_open(i)]
        target = open_stages[-1] if open_stages else indexes[0]

        self.section = section
        self.to_index = target
        self.hover_index = None
        self.arrival_pending = False
        # Put the avatar straight on the selected stage of the new roadmap
        self.avatar.center_x, self.avatar.center_y = NODE_POSITIONS[target]
        self.avatar.set_target(*NODE_POSITIONS[target])
        self.state.sounds.play("click")
        self.announce_arrival()

    def on_update(self, delta_time):
        """Move clouds and the avatar; announce when the avatar arrives."""
        self.time += delta_time
        for cloud in self.clouds:
            cloud.drift(delta_time)
        self.avatar.update_position(delta_time)

        # When a walk finishes, Eli says something about the new stage
        if self.arrival_pending and self.avatar.has_arrived():
            self.arrival_pending = False
            self.announce_arrival()

        self.bubble.update(delta_time)
        self.guide.update(delta_time, talking=not self.bubble.is_done())

    def on_draw(self):
        """Draw the scenery, road, stage markers, tabs, avatar and Eli."""
        self.window.clear(color=(135, 206, 235))
        draw_sky(self.time, self.section)
        self.clouds.draw()
        draw_land(self.time, self.section)
        self.draw_road()
        self.draw_nodes()
        self.avatar_list.draw()
        self.draw_name_tag()
        draw_top_bar(self.state, SECTION_NAMES[self.section])
        self.draw_tabs()
        self.guide.draw()
        self.bubble.draw()

    def draw_tabs(self):
        """Draw the two section tabs with how many stages are finished."""
        for section, (cx, cy, w, h) in self.tabs.items():
            indexes = SECTION_INDEXES[section]
            done = sum(1 for i in indexes if i < self.state.level_index)
            active = section == self.section
            draw_box(cx, cy, w, h, GOLD if active else PANEL, NAVY, 2)
            draw_label(f"{SECTION_NAMES[section]}   {done}/{len(indexes)}",
                       cx, cy, DARK if active else NAVY, 15, True)

    def draw_road(self):
        """Draw the path between stages: solid when open, thin when locked."""
        indexes = SECTION_INDEXES[self.section]
        for a, b in zip(indexes, indexes[1:]):
            x1, y1 = NODE_POSITIONS[a]
            x2, y2 = NODE_POSITIONS[b]
            if self.is_open(b):                          # both ends are open
                arcade.draw_line(x1, y1, x2, y2, PATH_BROWN, 9)
                arcade.draw_line(x1, y1, x2, y2, (214, 190, 140), 4)
            else:
                arcade.draw_line(x1, y1, x2, y2, (160, 165, 175), 3)

    def draw_nodes(self):
        """Draw every stage marker in its finished, current or locked style."""
        for i in SECTION_INDEXES[self.section]:
            x, y = NODE_POSITIONS[i]
            is_locked = not self.is_open(i)
            if is_locked:
                fill = LOCKED
            elif i == self.state.level_index:
                fill = GOLD
            else:
                fill = GREEN

            # The current stage gets a pulsing ring to attract attention
            if i == self.state.level_index:
                pulse = NODE_RADIUS + 6 + 3 * math.sin(self.time * 4)
                arcade.draw_circle_outline(x, y, pulse, WHITE, 3)

            # Ring around the stage that is selected, or under the mouse
            if i == self.to_index or (i == self.hover_index and not is_locked):
                arcade.draw_circle_outline(x, y, NODE_RADIUS + 11, NAVY, 3)

            # Circles for Bible Stories, books for Memory Verses
            if self.section == "story":
                arcade.draw_circle_filled(x, y, NODE_RADIUS, fill)
                arcade.draw_circle_outline(x, y, NODE_RADIUS, WHITE, 3)
            else:
                draw_book(x, y, fill)

            if is_locked:
                draw_padlock(x, y)
            else:
                draw_label(str(LOCATIONS[i]["number"]), x, y, DARK, 15, True)

    def draw_name_tag(self):
        """Draw a small label with the stage name above the hovered stage."""
        index = self.hover_index if self.hover_index is not None \
            else self.to_index
        x, y = NODE_POSITIONS[index]
        name = LOCATIONS[index]["name"]
        if not self.is_open(index):
            name += " (locked)"
        width = max(110, len(name) * 9 + 30)
        # Keep the tag fully on screen near the left and right edges
        tag_x = min(max(x, width / 2 + 5), SCREEN_WIDTH - width / 2 - 5)
        draw_box(tag_x, y + 42, width, 26, PANEL, NAVY, 2)
        draw_label(name, tag_x, y + 42, DARK, 12, True)

    def enter_location(self):
        """Open the story screen for the selected stage (if open and arrived)."""
        if not self.avatar.has_arrived():
            return
        if not self.is_open(self.to_index):
            self.show_locked_message(self.to_index)
            return
        # A stage before the current one is already finished: practice mode
        practice = self.to_index < self.state.level_index
        self.state.sounds.play("click")
        self.window.show_view(StoryView(self.state, self.to_index, practice))

    def on_mouse_motion(self, x, y, dx, dy):
        """Remember which stage the mouse is over (for the name tag)."""
        self.hover_index = self.node_at(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Switch tabs, select a stage, or play the selected stage."""
        for section, (cx, cy, w, h) in self.tabs.items():
            if point_in_box(x, y, cx, cy, w, h):
                self.switch_section(section)
                return

        index = self.node_at(x, y)
        if index is None:
            return
        if not self.is_open(index):                  # locked
            self.show_locked_message(index)
        elif index == self.to_index and self.avatar.has_arrived():
            self.enter_location()
        else:
            self.travel_to(index)

    def on_key_press(self, key, modifiers):
        """ENTER plays; LEFT/RIGHT move between stages; TAB swaps roadmaps."""
        if self.handle_global_key(key):
            return
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            self.enter_location()
        elif key == arcade.key.TAB:
            self.switch_section("verse" if self.section == "story" else "story")
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            indexes = SECTION_INDEXES[self.section]
            step = -1 if key == arcade.key.LEFT else 1
            new_position = indexes.index(self.to_index) + step
            if 0 <= new_position < len(indexes):
                target = indexes[new_position]
                if self.is_open(target):
                    self.travel_to(target)
                else:
                    self.show_locked_message(target)


# ─── STORY SCREEN ─────────────────────────────────────────────────────

class StoryView(BaseView):
    """Eli introduces a stage (and its lesson or tip) before the quiz."""

    def __init__(self, state, stage_index, practice=False):
        """
        Set up the story screen.

        Args:
            state (GameState): The shared game state
            stage_index (int): Which stage is being played
            practice (bool): True when replaying a finished stage
        """
        super().__init__(state)
        self.stage_index = stage_index
        self.practice = practice
        self.location = LOCATIONS[stage_index]
        self.guide = Guide(150, 105, 1.45)
        self.bubble = SpeechBubble(630, 320, 660, 340, 19)

        # The "lesson" is optional so custom stages without one still work
        text = self.location["story"]
        lesson = self.location.get("lesson", "")
        if lesson:
            text += "\n\n" + lesson
        self.bubble.say(text, 55)

    def on_update(self, delta_time):
        """Type out the story and move Eli's mouth while it is typing."""
        self.time += delta_time
        self.bubble.update(delta_time)
        self.guide.update(delta_time, talking=not self.bubble.is_done())

    def on_draw(self):
        """Draw the scenery, stage title, Eli, his words and the details."""
        section = self.location["section"]
        self.window.clear(color=(135, 206, 235))
        draw_sky(self.time, section)
        draw_land(self.time, section)
        draw_top_bar(self.state,
                     f"{SECTION_SINGULAR[section]} {self.location['number']}"
                     f" of {len(SECTION_INDEXES[section])}")

        draw_label(self.location["name"], 630, 545, NAVY, 32, True)
        draw_label(self.location["reference"], 630, 510, DARK, 16)

        self.guide.draw()
        self.bubble.draw()

        questions = min(QUESTIONS_PER_PLAY, len(self.location["questions"]))
        draw_box(630, 118, 660, 34, PANEL, NAVY, 2)
        draw_label(f"Questions: {questions}   |   Time per question: "
                   f"{self.location['time_limit']} seconds",
                   630, 118, RED, 16, True)

        if self.bubble.is_done():
            prompt = "Press ENTER or click to begin the quiz"
        else:
            prompt = "Press ENTER to skip the typing"
        draw_label(prompt, 630, 78, WHITE, 18, True)
        if self.practice:
            draw_label("PRACTICE MODE: no lives lost, no points",
                       630, 48, WHITE, 14, True)

    def advance(self):
        """First press skips the typing; the next press starts the quiz."""
        if not self.bubble.is_done():
            self.bubble.skip()
            return
        self.state.sounds.play("click")
        self.window.show_view(
            QuizView(self.state, self.stage_index, self.practice))

    def on_mouse_press(self, x, y, button, modifiers):
        """Skip or continue when the mouse is clicked."""
        self.advance()

    def on_key_press(self, key, modifiers):
        """Skip or continue when ENTER or SPACE is pressed."""
        if self.handle_global_key(key):
            return
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            self.advance()


# ─── QUIZ SCREEN ──────────────────────────────────────────────────────

class QuizView(BaseView):
    """
    Shows one question at a time with a countdown timer and feedback.

    The game never shows the right answer. A wrong choice turns red, and
    Eli tells the player which Bible chapter to go and read.
    """

    ANSWER_KEYS = (arcade.key.KEY_1, arcade.key.KEY_2,
                   arcade.key.KEY_3, arcade.key.KEY_4)

    def __init__(self, state, stage_index, practice=False):
        """
        Start the quiz for a stage.

        Args:
            state (GameState): The shared game state
            stage_index (int): Which stage is being played
            practice (bool): True for practice (no lives lost, no points)
        """
        super().__init__(state)
        self.stage_index = stage_index
        self.location = LOCATIONS[stage_index]
        self.practice = practice

        # Pick a random set of questions so each play is a little different
        bank = self.location["questions"]
        self.questions = random.sample(bank, min(QUESTIONS_PER_PLAY, len(bank)))
        self.question_index = 0
        self.mistakes = 0              # wrong answers in this stage
        self.particles = []            # confetti pieces
        self.flash_time = 0.0          # red flash after a wrong answer

        self.guide = Guide(70, 12, 0.5)
        self.bubble = SpeechBubble(560, 52, 810, 78, 17)
        self.load_question()

    def load_question(self):
        """Load the next question and shuffle its answer options."""
        question = self.questions[self.question_index]
        self.question_text = question["q"]
        # The chapter to read if missed; falls back to the stage's passage
        self.read = question.get("read") or self.location["reference"]
        self.correct_text = question["options"][0]   # first is always correct
        self.options = question["options"][:]        # copy, then shuffle
        random.shuffle(self.options)

        self.time_left = self.location["time_limit"]
        self.feedback = None            # message shown after answering
        self.feedback_timer = 0.0
        self.selected = None            # index of the chosen option
        self.last_tick = None           # last second a warning tick played

    def button_geometry(self, index):
        """
        Get the position and size of an answer button.

        Args:
            index (int): Which answer button (0 to 3)

        Returns:
            tuple: (center x, center y, width, height)
        """
        return (SCREEN_WIDTH / 2, 350 - index * 75, 800, 58)

    def on_update(self, delta_time):
        """Run the timers, confetti, flash and Eli's animation."""
        self.time += delta_time
        self.guide.update(delta_time, talking=(
            self.feedback is not None and not self.bubble.is_done()))
        self.bubble.update(delta_time)

        # Confetti: move every piece and drop the ones that faded away
        for piece in self.particles:
            piece.update(delta_time)
        self.particles = [p for p in self.particles if p.is_alive()]
        self.flash_time = max(0.0, self.flash_time - delta_time)

        if self.feedback is None:
            # Waiting for an answer: count the question timer down
            self.time_left -= delta_time
            seconds = math.ceil(self.time_left)
            # Tick once per second during the last five seconds
            if 0 < seconds <= 5 and seconds != self.last_tick:
                self.last_tick = seconds
                self.state.sounds.play("tick", 0.4)
            if self.time_left <= 0:
                self.time_left = 0
                self.submit_answer(None)          # None means "ran out of time"
        else:
            # Showing the result: count the message timer down
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.next_step()

    def on_draw(self):
        """Draw the timer bar, question, answer buttons, Eli and effects."""
        self.window.clear(color=(135, 206, 235))
        draw_sky(self.time, self.location["section"])
        draw_top_bar(self.state, self.location["name"])

        # Timer bar: green, then gold, then red as time runs out
        ratio = self.time_left / self.location["time_limit"]
        draw_box(SCREEN_WIDTH / 2, 552, 800, 16, GRAY)
        if ratio > 0:
            fill_width = 800 * ratio
            if ratio > 0.5:
                bar_color = GREEN
            elif ratio > 0.25:
                bar_color = GOLD
            else:
                bar_color = RED
            draw_box(100 + fill_width / 2, 552, fill_width, 16, bar_color)

        # Question panel. Long verses get a smaller font so they still fit.
        total = len(self.questions)
        draw_box(SCREEN_WIDTH / 2, 465, 800, 105, PANEL, NAVY, 3)
        label = f"Question {self.question_index + 1} of {total}"
        if self.practice:
            label += "   (practice)"
        draw_label(label, SCREEN_WIDTH / 2, 505, GRAY, 14)
        length = len(self.question_text)
        size = 22 if length <= 80 else 19 if length <= 140 else 17
        draw_label(self.question_text, SCREEN_WIDTH / 2, 460,
                   DARK, size, True, wrap_width=740)

        # Answer buttons. After answering, ONLY the player's own choice is
        # colored: green if it was right, red if it was wrong. The right
        # answer is never revealed after a mistake.
        for i, option in enumerate(self.options):
            cx, cy, w, h = self.button_geometry(i)
            color = NAVY
            if self.feedback is not None and i == self.selected:
                color = GREEN if option == self.correct_text else RED
            draw_box(cx, cy, w, h, color, WHITE, 2)
            draw_label(f"{i + 1}.  {option}", cx, cy, WHITE, 18, True)

        # Eli and what he says after an answer
        self.guide.draw()
        if self.feedback is not None:
            self.bubble.draw()

        # Effects on top: red flash and confetti
        if self.flash_time > 0:
            alpha = int(110 * self.flash_time / 0.35)
            draw_box(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                     SCREEN_HEIGHT, (229, 57, 53, alpha))
        for piece in self.particles:
            piece.draw()

    def submit_answer(self, choice):
        """
        Check the player's answer, update lives and score, react.

        A wrong answer or a timeout sends the player to read a Bible chapter
        and adds that chapter to the study list.

        Args:
            choice (int): Index of the chosen option, or None if time ran out
        """
        if self.feedback is not None:
            return                  # already answered this question

        self.selected = choice
        correct = choice is not None and self.options[choice] == self.correct_text
        if not self.practice:
            self.state.questions_answered += 1

        if correct:
            points = 10 + int(self.time_left)       # faster answers earn more
            if self.practice:
                message = random.choice(GUIDE_CORRECT)
            else:
                self.state.score += points
                self.state.correct_answers += 1
                message = f"{random.choice(GUIDE_CORRECT)} +{points} points"
            self.state.sounds.play("correct")
            self.guide.set_mood("happy", 2.0)
            spawn_confetti(self.particles, SCREEN_WIDTH / 2, 465, 35)
            self.feedback_timer = FEEDBACK_CORRECT_SECONDS
        else:
            self.mistakes += 1
            if not self.practice:
                self.state.lives -= 1
            # Remember the chapter so it appears in the study list later
            if self.read not in self.state.study_list:
                self.state.study_list.append(self.read)
            lines = GUIDE_TIMEOUT if choice is None else GUIDE_WRONG
            message = f"{random.choice(lines)} {reading_hint(self.read)}"
            self.state.sounds.play("wrong")
            self.guide.set_mood("sad", 2.5)
            self.flash_time = 0.35
            self.feedback_timer = FEEDBACK_WRONG_SECONDS

        self.feedback = message
        self.bubble.say(message, 80)

    def skip_feedback(self):
        """Move on early once the player has finished reading Eli's message."""
        if self.feedback is not None and self.bubble.is_done():
            self.feedback_timer = 0

    def next_step(self):
        """Move to the next question, finish the stage, or end the game."""
        if self.state.lives <= 0:
            self.window.show_view(ResultView(self.state, False))
            return

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.load_question()
        else:
            self.finish_stage()

    def finish_stage(self):
        """Handle the end of a stage: bonus life, unlock next, or victory."""
        self.state.sounds.play("stage_clear")

        # Practice never changes progress; just go back to the map
        if self.practice:
            self.window.show_view(MapView(
                self.state, self.stage_index, self.stage_index,
                "Good practice! Pick another open stage, or press the "
                "arrow keys to travel."))
            return

        # A stage with no mistakes earns an extra life (up to the maximum)
        message = "Stage complete!"
        if self.mistakes == 0 and self.state.lives < MAX_LIVES:
            self.state.lives += 1
            message = "A perfect stage! You earned an extra life."

        finished = self.stage_index
        self.state.level_index += 1             # unlock the next stage
        if self.state.level_index >= len(LOCATIONS):
            self.window.show_view(ResultView(self.state, True))
        else:
            next_stage = LOCATIONS[self.state.level_index]
            note = ""
            if next_stage["section"] != self.location["section"]:
                note = (f" The {SECTION_NAMES[next_stage['section']]} "
                        "section has opened!")
            self.window.show_view(MapView(
                self.state, finished, self.state.level_index,
                f"{message}{note} Next stop: {next_stage['name']}. "
                "Press ENTER when we arrive."))

    def on_mouse_press(self, x, y, button, modifiers):
        """Choose an answer by clicking, or skip the message after answering."""
        if self.feedback is not None:
            self.skip_feedback()
            return
        for i in range(len(self.options)):
            if point_in_box(x, y, *self.button_geometry(i)):
                self.submit_answer(i)

    def on_key_press(self, key, modifiers):
        """Choose an answer with 1 to 4, or skip the message with ENTER."""
        if self.handle_global_key(key):
            return
        if self.feedback is not None:
            if key in (arcade.key.ENTER, arcade.key.SPACE):
                self.skip_feedback()
            return
        if key in self.ANSWER_KEYS:
            self.submit_answer(self.ANSWER_KEYS.index(key))


# ─── RESULT SCREEN ────────────────────────────────────────────────────

class ResultView(BaseView):
    """The win or lose screen, including the passages the player should read."""

    def __init__(self, state, won):
        """
        Set up the result screen and play the matching sound.

        Args:
            state (GameState): The shared game state
            won (bool): True if the player finished every stage
        """
        super().__init__(state)
        self.won = won
        self.particles = []
        self.rain_timer = 0.0
        self.guide = Guide(150, 120, 1.3)
        self.guide.set_mood("happy" if won else "sad", 999)
        state.sounds.play("victory" if won else "lose")

    def on_update(self, delta_time):
        """Animate Eli and, after a win, rain confetti from the top."""
        self.time += delta_time
        self.guide.update(delta_time)
        if self.won:
            self.rain_timer -= delta_time
            if self.rain_timer <= 0:
                self.rain_timer = 0.25
                spawn_confetti(self.particles, random.uniform(80, 920),
                               600, 8)
        for piece in self.particles:
            piece.update(delta_time)
        self.particles = [p for p in self.particles if p.is_alive()]

    def on_draw(self):
        """Draw the final message, score, study list and replay instructions."""
        self.window.clear(color=(135, 206, 235))
        draw_sky(self.time)
        draw_land(self.time)
        draw_box(630, 340, 640, 440, PANEL, NAVY, 4)

        if self.won:
            stories = len(SECTION_INDEXES["story"])
            verses = len(SECTION_INDEXES["verse"])
            draw_label("Journey Complete!", 630, 520, GREEN, 44, True)
            draw_label(f"You finished {stories} Bible stories and "
                       f"{verses} memory verse sets.",
                       630, 470, DARK, 18)
        else:
            draw_label("Journey Ended", 630, 520, RED, 44, True)
            draw_label("You ran out of lives. Read, learn and try again!",
                       630, 470, DARK, 18)

        answered = self.state.questions_answered
        accuracy = (round(100 * self.state.correct_answers / answered)
                    if answered else 0)
        draw_label(f"Final Score: {self.state.score}", 630, 415, NAVY, 28, True)
        draw_label(f"Correct Answers: {self.state.correct_answers} of "
                   f"{answered}  ({accuracy}%)", 630, 370, DARK, 20)
        draw_label(f"Stages completed: {self.state.level_index} of "
                   f"{len(LOCATIONS)}", 630, 335, DARK, 18)

        # The study list: chapters of the questions that were missed
        study = self.state.study_list
        if study:
            shown = study[:8]
            text = ",  ".join(shown)
            if len(study) > len(shown):
                text += f"  and {len(study) - len(shown)} more"
            draw_label("Passages to read before your next try:",
                       630, 292, NAVY, 16, True)
            draw_label(text, 630, 250, DARK, 15, wrap_width=580)
        else:
            draw_label("You did not miss a single question!",
                       630, 270, GREEN, 18, True)

        draw_label("Press ENTER or click to return to the menu",
                   630, 165, NAVY, 18, True)

        self.guide.draw()
        for piece in self.particles:
            piece.draw()

    def go_to_menu(self):
        """Return to the title screen."""
        self.state.sounds.play("click")
        self.window.show_view(MenuView(self.state))

    def on_mouse_press(self, x, y, button, modifiers):
        """Return to the menu when the mouse is clicked."""
        self.go_to_menu()

    def on_key_press(self, key, modifiers):
        """Return to the menu when ENTER or SPACE is pressed."""
        if self.handle_global_key(key):
            return
        if key in (arcade.key.ENTER, arcade.key.SPACE):
            self.go_to_menu()


# ─── DATA VALIDATION ──────────────────────────────────────────────────

def validate_game_data():
    """
    Check every stage's data and stop with a clear message if it is wrong.

    This catches mistakes (a missing answer, a duplicated option) before the
    window opens, instead of crashing in the middle of a quiz.

    Raises:
        ValueError: Describing exactly which stage or question is wrong.
    """
    if not LOCATIONS:
        raise ValueError("BibleTales needs at least one location.")

    for level_number, location in enumerate(LOCATIONS, start=1):
        if not location.get("questions"):
            raise ValueError(f"Level {level_number} "
                             f"({location.get('name')}) has no questions.")
        if location.get("time_limit", 0) <= 0:
            raise ValueError(f"Level {level_number} must have a positive "
                             "time limit.")

        for question_number, question in enumerate(location["questions"],
                                                   start=1):
            options = question.get("options", [])
            if len(options) != 4 or len(set(options)) != 4:
                raise ValueError(
                    f"Level {level_number} ({location['name']}), question "
                    f"{question_number} must contain exactly four unique "
                    "answer options.")


# ─── PROGRAM START ────────────────────────────────────────────────────

def main():
    """Check the data, create the window, show the menu, run the game loop."""
    validate_game_data()            # catch data mistakes before opening
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    state = GameState()             # also loads all the sounds
    window.show_view(MenuView(state))
    arcade.run()                    # the game loop runs until the window closes


if __name__ == "__main__":
    main()