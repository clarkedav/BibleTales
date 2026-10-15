"""
memory_verses.py - The Memory Verse section of BibleTales.

This file holds nine sets of verses, in Bible order from Genesis to
Revelation. Each question shows a verse with one word or phrase missing, and
the player picks the right words. The wording follows the King James Version
(KJV), which is in the public domain.

HOW THE SECTION CONNECTS TO THE BIBLE STORIES
After every TWO Bible story stages, the next Memory Verse stage is placed in
the journey (story, story, verse, story, story, verse, and so on). Both
sections have their own roadmap on the map screen, but they share one
progress line: a verse stage opens only after the stages before it are done.

If a player misses a verse, the game sends them to read the whole chapter
that verse comes from. The chapter is worked out automatically from the
reference, for example "Psalm 23:4" becomes "Psalm 23".
"""

VERSES_PER_SECTION_STEP = 2      # one verse stage after every 2 story stages


def chapter_of(reference):
    """
    Turn a verse reference into its chapter.

    Args:
        reference (str): For example "Psalm 23:4" or "Numbers 6:24-26"

    Returns:
        str: The chapter only, for example "Psalm 23" or "Numbers 6"
    """
    return reference.split(":")[0]


def verse(reference, text, correct, *wrong):
    """
    Build a fill-in-the-blank verse question.

    Args:
        reference (str): Where the verse is, for example "Genesis 1:1"
        text (str): The verse with a "_____" where the missing words go
        correct (str): The missing words (always given first)
        *wrong: Three wrong choices

    Returns:
        dict: A question with "q", "options" and "read" keys
    """
    options = [correct, *wrong]
    if len(options) != 4 or len(set(options)) != 4:
        raise ValueError(f"Verse {reference} needs four different options.")
    return {
        "q": f'Complete the verse ({reference}, KJV):  "{text}"',
        "options": options,
        "read": chapter_of(reference),
    }


# ─── THE NINE VERSE SETS ──────────────────────────────────────────────

VERSE_STAGES = [
    {
        "name": "Verses of Beginnings",
        "reference": "Genesis",
        "story": (
            "Every journey has a first step. These verses come from the "
            "book of Genesis, where God begins His story with the world, "
            "with people, and with a promise."
        ),
        "lesson": (
            "Tip: Say each verse out loud three times, then try writing it "
            "from memory."
        ),
        "time_limit": 25,
        "questions": [
            verse("Genesis 1:1", "In the beginning God created the _____ and the earth.", "heaven", "light", "waters", "sun"),
            verse("Genesis 1:5", "And God called the light _____, and the darkness he called Night.", "Day", "Morning", "Sun", "Heaven"),
            verse("Genesis 1:28", "Be fruitful, and multiply, and _____ the earth, and subdue it:", "replenish", "plant", "guard", "divide"),
            verse("Genesis 1:31", "And God saw every thing that he had made, and, behold, it was very _____.", "good", "bright", "great", "new"),
            verse("Genesis 2:18", "And the LORD God said, It is not good that the man should be _____; I will make him an help meet for him.", "alone", "silent", "idle", "hungry"),
            verse("Genesis 9:13", "I do set my _____ in the cloud, and it shall be for a token of a covenant between me and the earth.", "bow", "sword", "staff", "crown"),
            verse("Genesis 12:2", "And I will make of thee a great _____, and I will bless thee, and make thy name great; and thou shalt be a blessing:", "nation", "city", "kingdom", "army"),
            verse("Genesis 22:14", "In the mount of the LORD it shall be _____.", "seen", "built", "found", "known"),
            verse("Genesis 50:20", "But as for you, ye thought evil against me; but God meant it unto _____, to bring to pass, as it is this day, to save much people alive.", "good", "joy", "peace", "glory"),
        ],
    },
    {
        "name": "Verses of the Law",
        "reference": "Exodus to Deuteronomy",
        "story": (
            "At Mount Sinai and in the wilderness, God taught His people how "
            "to live. These verses come from Exodus, Leviticus, Numbers and "
            "Deuteronomy."
        ),
        "lesson": (
            "Tip: Break a long verse into small pieces and learn one piece "
            "at a time."
        ),
        "time_limit": 25,
        "questions": [
            verse("Exodus 14:14", "The LORD shall _____ for you, and ye shall hold your peace.", "fight", "work", "care", "stand"),
            verse("Exodus 20:3", "Thou shalt have no other _____ before me.", "gods", "kings", "masters", "idols"),
            verse("Exodus 20:8", "Remember the sabbath day, to keep it _____.", "holy", "quiet", "free", "safe"),
            verse("Exodus 20:12", "Honour thy father and thy mother: that thy days may be _____ upon the land which the LORD thy God giveth thee.", "long", "good", "many", "happy"),
            verse("Leviticus 19:18", "...but thou shalt love thy neighbour as _____: I am the LORD.", "thyself", "a brother", "the stranger", "a friend"),
            verse("Numbers 6:24", "The LORD bless thee, and _____ thee:", "keep", "guide", "save", "heal"),
            verse("Numbers 6:26", "The LORD lift up his countenance upon thee, and give thee _____.", "peace", "joy", "rest", "mercy"),
            verse("Deuteronomy 6:5", "And thou shalt love the LORD thy God with all thine heart, and with all thy soul, and with all thy _____.", "might", "wealth", "wisdom", "labour"),
            verse("Deuteronomy 8:3", "...that he might make thee know that man doth not live by _____ only...", "bread", "water", "meat", "wine"),
            verse("Deuteronomy 31:6", "Be strong and of a good courage, fear not, nor be afraid of them: for the LORD thy God, he it is that doth go with thee; he will not _____ thee, nor forsake thee.", "fail", "judge", "hide", "blame"),
        ],
    },
    {
        "name": "Verses of Courage",
        "reference": "Joshua to Esther",
        "story": (
            "Judges, kings, prophets and queens needed courage to follow God. "
            "These verses come from Joshua through Esther."
        ),
        "lesson": (
            "Tip: Write a verse on a card and read it each morning for a week."
        ),
        "time_limit": 24,
        "questions": [
            verse("Joshua 1:9", "Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou _____: for the LORD thy God is with thee whithersoever thou goest.", "dismayed", "troubled", "weary", "angry"),
            verse("Joshua 24:15", "...but as for me and my house, we will _____ the LORD.", "serve", "obey", "honour", "hear"),
            verse("Ruth 1:16", "...whither thou goest, I will go; and where thou lodgest, I will _____:", "lodge", "sleep", "sit", "walk"),
            verse("1 Samuel 15:22", "Behold, to obey is better than _____, and to hearken than the fat of rams.", "sacrifice", "wisdom", "silver", "praise"),
            verse("1 Samuel 16:7", "...for man looketh on the outward appearance, but the LORD looketh on the _____.", "heart", "mind", "soul", "hands"),
            verse("1 Kings 3:9", "Give therefore thy servant an _____ heart to judge thy people, that I may discern between good and bad:", "understanding", "obedient", "humble", "loyal"),
            verse("2 Chronicles 7:14", "If my people, which are called by my name, shall humble themselves, and pray, and seek my face, and turn from their wicked ways; then will I _____ from heaven, and will forgive their sin, and will heal their land.", "hear", "speak", "look", "come"),
            verse("Nehemiah 8:10", "...for the joy of the LORD is your _____.", "strength", "song", "peace", "shield"),
            verse("Esther 4:14", "...and who knoweth whether thou art come to the kingdom for such a _____ as this?", "time", "day", "place", "season"),
        ],
    },
    {
        "name": "Verses of the Psalms",
        "reference": "Psalms",
        "story": (
            "The Psalms are songs and prayers that Israel sang to God. These "
            "verses are some of the most loved in all of Scripture."
        ),
        "lesson": (
            "Tip: Pray a verse back to God in your own words after you "
            "learn it."
        ),
        "time_limit": 24,
        "questions": [
            verse("Psalm 19:1", "The heavens declare the glory of God; and the _____ sheweth his handywork.", "firmament", "mountain", "ocean", "moon"),
            verse("Psalm 23:1", "The LORD is my _____; I shall not want.", "shepherd", "king", "rock", "light"),
            verse("Psalm 23:4", "Yea, though I walk through the valley of the shadow of death, I will fear no _____: for thou art with me;", "evil", "man", "harm", "night"),
            verse("Psalm 27:1", "The LORD is my light and my salvation; whom shall I _____?", "fear", "love", "trust", "seek"),
            verse("Psalm 34:8", "O taste and see that the LORD is _____: blessed is the man that trusteth in him.", "good", "near", "just", "kind"),
            verse("Psalm 46:1", "God is our refuge and strength, a very present _____ in trouble.", "help", "friend", "guide", "hope"),
            verse("Psalm 46:10", "Be _____, and know that I am God:", "still", "strong", "humble", "ready"),
            verse("Psalm 118:24", "This is the day which the LORD hath made; we will _____ and be glad in it.", "rejoice", "work", "sing", "pray"),
            verse("Psalm 119:105", "Thy word is a _____ unto my feet, and a light unto my path.", "lamp", "torch", "sword", "staff"),
            verse("Psalm 121:1", "I will lift up mine eyes unto the _____, from whence cometh my help.", "hills", "skies", "clouds", "stars"),
        ],
    },
    {
        "name": "Verses of Wisdom",
        "reference": "Proverbs and Ecclesiastes",
        "story": (
            "Proverbs and Ecclesiastes teach us how to live wisely day by "
            "day. These short verses are easy to carry in your heart."
        ),
        "lesson": (
            "Tip: Choose one verse for the week and look for ways to live "
            "it out."
        ),
        "time_limit": 23,
        "questions": [
            verse("Proverbs 1:7", "The fear of the LORD is the beginning of _____: but fools despise wisdom and instruction.", "knowledge", "wealth", "life", "peace"),
            verse("Proverbs 3:5", "Trust in the LORD with all thine _____; and lean not unto thine own understanding.", "heart", "mind", "soul", "strength"),
            verse("Proverbs 3:6", "In all thy ways acknowledge him, and he shall _____ thy paths.", "direct", "guard", "make", "bless"),
            verse("Proverbs 15:1", "A soft answer turneth away _____: but grievous words stir up anger.", "wrath", "sorrow", "pride", "hunger"),
            verse("Proverbs 17:17", "A friend loveth at all times, and a brother is born for _____.", "adversity", "friendship", "comfort", "glory"),
            verse("Proverbs 18:10", "The name of the LORD is a strong _____: the righteous runneth into it, and is safe.", "tower", "shield", "mountain", "house"),
            verse("Proverbs 22:6", "Train up a child in the way he should go: and when he is old, he will not _____ from it.", "depart", "wander", "fall", "hide"),
            verse("Proverbs 27:17", "Iron sharpeneth iron; so a man sharpeneth the countenance of his _____.", "friend", "brother", "enemy", "father"),
            verse("Ecclesiastes 3:1", "To every thing there is a _____, and a time to every purpose under the heaven:", "season", "reason", "moment", "day"),
        ],
    },
    {
        "name": "Verses of the Prophets",
        "reference": "Isaiah to Micah",
        "story": (
            "The prophets spoke God's words of warning and hope. These "
            "verses come from Isaiah, Jeremiah, Lamentations and Micah."
        ),
        "lesson": (
            "Tip: Learn the reference with the verse so you can find it "
            "again in your Bible."
        ),
        "time_limit": 22,
        "questions": [
            verse("Isaiah 9:6", "...and his name shall be called Wonderful, Counsellor, The mighty God, The everlasting Father, The Prince of _____.", "Peace", "Kings", "Life", "Glory"),
            verse("Isaiah 26:3", "Thou wilt keep him in perfect _____, whose mind is stayed on thee: because he trusteth in thee.", "peace", "health", "safety", "joy"),
            verse("Isaiah 40:31", "...they shall mount up with wings as _____; they shall run, and not be weary; and they shall walk, and not faint.", "eagles", "doves", "ravens", "sparrows"),
            verse("Isaiah 41:10", "Fear thou not; for I am with thee: be not _____; for I am thy God:", "dismayed", "afraid", "troubled", "angry"),
            verse("Isaiah 53:5", "...he was bruised for our iniquities... and with his stripes we are _____.", "healed", "saved", "free", "forgiven"),
            verse("Jeremiah 29:11", "For I know the thoughts that I think toward you, saith the LORD, thoughts of _____, and not of evil, to give you an expected end.", "peace", "wealth", "victory", "rest"),
            verse("Jeremiah 33:3", "Call unto me, and I will _____ thee, and shew thee great and mighty things, which thou knowest not.", "answer", "teach", "bless", "follow"),
            verse("Lamentations 3:23", "They are new every _____: great is thy faithfulness.", "morning", "night", "week", "year"),
            verse("Micah 6:8", "...and what doth the LORD require of thee, but to do justly, and to love mercy, and to walk _____ with thy God?", "humbly", "closely", "daily", "boldly"),
        ],
    },
    {
        "name": "Verses of the Savior",
        "reference": "Matthew, Mark and Luke",
        "story": (
            "Jesus taught crowds on hillsides and friends around tables. "
            "These verses come from the first three Gospels."
        ),
        "lesson": (
            "Tip: Imagine Jesus saying the verse to you, and answer Him in "
            "prayer."
        ),
        "time_limit": 22,
        "questions": [
            verse("Matthew 5:16", "Let your _____ so shine before men, that they may see your good works, and glorify your Father which is in heaven.", "light", "love", "faith", "joy"),
            verse("Matthew 6:33", "But seek ye first the kingdom of God, and his _____; and all these things shall be added unto you.", "righteousness", "wisdom", "glory", "mercy"),
            verse("Matthew 7:7", "Ask, and it shall be _____ you; seek, and ye shall find; knock, and it shall be opened unto you:", "given", "shown", "sent", "told"),
            verse("Matthew 11:28", "Come unto me, all ye that labour and are heavy laden, and I will give you _____.", "rest", "peace", "bread", "joy"),
            verse("Matthew 22:37", "Thou shalt love the Lord thy God with all thy heart, and with all thy soul, and with all thy _____.", "mind", "body", "wealth", "time"),
            verse("Matthew 28:19", "Go ye therefore, and teach all _____, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost:", "nations", "people", "men", "cities"),
            verse("Mark 10:27", "...with men it is impossible, but not with God: for with God all things are _____.", "possible", "known", "simple", "given"),
            verse("Luke 1:37", "For with God nothing shall be _____.", "impossible", "forgotten", "hidden", "wasted"),
            verse("Luke 2:11", "For unto you is born this day in the city of David a _____, which is Christ the Lord.", "Saviour", "King", "Prophet", "Shepherd"),
            verse("Luke 6:31", "And as ye would that men should do to you, do ye also to them _____.", "likewise", "freely", "gladly", "always"),
        ],
    },
    {
        "name": "Verses of Life",
        "reference": "John, Acts and Romans",
        "story": (
            "John shows us who Jesus is, Acts shows the church beginning, "
            "and Romans explains the good news. These verses come from "
            "those three books."
        ),
        "lesson": (
            "Tip: Learn John 3:16 first. Many people call it the heart of "
            "the Bible's message."
        ),
        "time_limit": 21,
        "questions": [
            verse("John 1:1", "In the beginning was the _____, and the Word was with God, and the Word was God.", "Word", "Light", "Truth", "Life"),
            verse("John 3:16", "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have _____ life.", "everlasting", "abundant", "new", "peaceful"),
            verse("John 13:34", "A new commandment I give unto you, That ye _____ one another; as I have loved you, that ye also love one another.", "love", "help", "honour", "teach"),
            verse("John 14:6", "Jesus saith unto him, I am the way, the truth, and the _____: no man cometh unto the Father, but by me.", "life", "light", "door", "word"),
            verse("Acts 1:8", "But ye shall receive _____, after that the Holy Ghost is come upon you:", "power", "peace", "wisdom", "gifts"),
            verse("Romans 3:23", "For all have sinned, and come short of the _____ of God;", "glory", "love", "law", "mercy"),
            verse("Romans 6:23", "For the wages of sin is death; but the _____ of God is eternal life through Jesus Christ our Lord.", "gift", "grace", "love", "word"),
            verse("Romans 8:28", "And we know that all things work _____ for good to them that love God, to them who are the called according to his purpose.", "together", "always", "out", "well"),
            verse("Romans 10:9", "...and shalt believe in thine heart that God hath _____ him from the dead, thou shalt be saved.", "raised", "called", "taken", "sent"),
        ],
    },
    {
        "name": "Verses of Hope",
        "reference": "1 Corinthians to Revelation",
        "story": (
            "The letters of the New Testament encourage believers to keep "
            "going, and Revelation ends the Bible with hope. Your journey "
            "through the verses ends here."
        ),
        "lesson": (
            "Tip: Keep a notebook of the verses you have learned and review "
            "it often."
        ),
        "time_limit": 20,
        "questions": [
            verse("1 Corinthians 13:13", "And now abideth faith, hope, charity, these three; but the greatest of these is _____.", "charity", "faith", "hope", "patience"),
            verse("2 Corinthians 5:17", "Therefore if any man be in Christ, he is a new _____: old things are passed away; behold, all things are become new.", "creature", "man", "heart", "spirit"),
            verse("Ephesians 2:8", "For by _____ are ye saved through faith; and that not of yourselves: it is the gift of God:", "grace", "works", "love", "mercy"),
            verse("Philippians 4:13", "I can do all things through Christ which _____ me.", "strengtheneth", "loveth", "teacheth", "calleth"),
            verse("1 Thessalonians 5:17", "Pray without _____.", "ceasing", "delay", "fear", "doubt"),
            verse("2 Timothy 1:7", "For God hath not given us the spirit of _____; but of power, and of love, and of a sound mind.", "fear", "doubt", "pride", "sorrow"),
            verse("Hebrews 11:1", "Now faith is the _____ of things hoped for, the evidence of things not seen.", "substance", "promise", "hope", "wonder"),
            verse("James 1:5", "If any of you lack _____, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him.", "wisdom", "faith", "strength", "patience"),
            verse("1 John 4:8", "He that loveth not knoweth not God; for God is _____.", "love", "light", "truth", "life"),
            verse("Revelation 3:20", "Behold, I stand at the door, and _____: if any man hear my voice, and open the door, I will come in to him,", "knock", "call", "wait", "watch"),
            verse("Revelation 21:4", "And God shall wipe away all _____ from their eyes; and there shall be no more death,", "tears", "sorrow", "pain", "fear"),
        ],
    },
]


# ─── MIXING THE VERSE STAGES INTO THE JOURNEY ─────────────────────────

def add_memory_verse_stages(story_stages):
    """
    Place a Memory Verse stage after every two Bible story stages.

    Every stage also receives a "section" ("story" or "verse") and a
    "number" (its position inside its own section) for the map screen.

    Args:
        story_stages (list): The Bible story stages in order

    Returns:
        list: The full journey: story, story, verse, story, story, verse...
        If verse stages are left over, they are added at the end.
    """
    journey = []
    waiting = list(VERSE_STAGES)         # verse stages not placed yet
    story_count = 0

    for stage in story_stages:
        story_stage = dict(stage)
        story_stage["section"] = "story"
        journey.append(story_stage)
        story_count += 1

        # After every second story stage, bring in the next verse stage
        if story_count % VERSES_PER_SECTION_STEP == 0 and waiting:
            verse_stage = dict(waiting.pop(0))
            verse_stage["section"] = "verse"
            journey.append(verse_stage)

    for leftover in waiting:             # any verse stages that did not fit
        verse_stage = dict(leftover)
        verse_stage["section"] = "verse"
        journey.append(verse_stage)

    # Number the stages inside each section (Bible Story 1, 2, 3 ...)
    counters = {"story": 0, "verse": 0}
    for stage in journey:
        counters[stage["section"]] += 1
        stage["number"] = counters[stage["section"]]

    return journey