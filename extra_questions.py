"""
extra_questions.py - Reading hints, extra questions and new Bible story stages.

questions.py holds the original twelve stages. This file adds to them
WITHOUT editing that file:

* BASE_READINGS gives every ORIGINAL question a Bible chapter to read. When a
  player answers wrongly, the game sends them to that chapter instead of
  giving the answer. The list for each stage must be in the SAME ORDER as
  the questions in questions.py.
* EXTRA_QUESTIONS adds more questions to stages that already exist.
* NEW_STAGES adds brand new stages. "after" says which stage each one
  follows, so the journey stays in Bible order.
* build_journey() merges everything into the final list of stages.

The rule from questions.py still applies: the FIRST answer given to a
question is the correct one. The game shuffles the answers.

HINT STYLE: hints name a whole chapter (or two), never a single verse, so the
player has to open the Bible and read for themselves.
"""

from questions import make_question


def ask(read, question, correct, *wrong):
    """
    Build a question that also remembers which chapter to read if it is missed.

    Args:
        read (str): The chapter(s) to read, for example "Genesis 1"
        question (str): The question text
        correct (str): The correct answer (always given first)
        *wrong: Three wrong answers

    Returns:
        dict: A question with "q", "options" and "read" keys
    """
    item = make_question(question, correct, *wrong)
    item["read"] = read
    return item


# ─── READING HINTS FOR THE ORIGINAL QUESTIONS ─────────────────────────
# One chapter per question, in the same order as questions.py.

BASE_READINGS = {
    "Creation": [
        "Genesis 1", "Genesis 1", "Genesis 1", "Genesis 1", "Genesis 1",
        "Genesis 1", "Genesis 1", "Genesis 1", "Genesis 1", "Genesis 2"],
    "Eden and the Fall": [
        "Genesis 2", "Genesis 2", "Genesis 2 and 3", "Genesis 3",
        "Genesis 3", "Genesis 3", "Genesis 4", "Genesis 4", "Genesis 4",
        "Genesis 4"],
    "Noah's Ark": [
        "Genesis 6", "Genesis 6", "Genesis 6", "Genesis 6", "Genesis 7",
        "Genesis 7", "Genesis 8", "Genesis 8", "Genesis 9", "Genesis 8"],
    "Abraham's Promise": [
        "Genesis 17", "Genesis 12", "Genesis 12", "Genesis 15",
        "Genesis 12 and 17", "Genesis 21", "Genesis 21", "Genesis 22",
        "Genesis 22", "Genesis 15 and 22"],
    "Jacob and Joseph": [
        "Genesis 24", "Genesis 25", "Genesis 32", "Genesis 37", "Genesis 37",
        "Genesis 37", "Genesis 40", "Genesis 41", "Genesis 41",
        "Genesis 45"],
    "Moses and the Exodus": [
        "Exodus 4", "Exodus 2", "Exodus 3", "Exodus 3", "Exodus 5",
        "Exodus 11 and 12", "Exodus 12", "Exodus 13", "Exodus 13",
        "Exodus 14"],
    "The Wilderness and God's Law": [
        "Exodus 16", "Exodus 16", "Exodus 17", "Exodus 19", "Exodus 20",
        "Exodus 20", "Exodus 20", "Exodus 32", "Numbers 13", "Numbers 14"],
    "Jericho and the Judges": [
        "Joshua 1", "Joshua 2", "Joshua 6", "Joshua 6", "Judges 4",
        "Judges 6", "Judges 7", "Judges 16", "Judges 16", "Judges 2"],
    "David and Goliath": [
        "1 Samuel 16", "1 Samuel 16 and 17", "1 Samuel 17", "1 Samuel 17",
        "1 Samuel 17", "1 Samuel 17", "1 Samuel 17", "1 Samuel 17",
        "1 Samuel 17", "1 Samuel 17"],
    "Daniel and the Lions": [
        "Daniel 1", "Daniel 1", "Daniel 1", "Daniel 6", "Daniel 6",
        "Daniel 6", "Daniel 6", "Daniel 3", "Daniel 3 and 6", "Daniel 6"],
    "The Life and Teachings of Jesus": [
        "Luke 2", "Luke 1 and 2", "Matthew 1", "Luke 2", "Matthew 5",
        "Luke 10", "Matthew 5", "John 13", "John 6", "Matthew 22"],
    "The Cross and Resurrection": [
        "Luke 22", "Luke 22", "Luke 22", "Luke 23", "John 19", "John 19",
        "Luke 23", "John 20", "John 20", "Luke 24"],
}

# ─── EXTRA QUESTIONS FOR EXISTING STAGES ──────────────────────────────

EXTRA_QUESTIONS = {
    "Creation": [
        ask("Genesis 1", "How many days of creative work are described in Genesis 1?", "Six days", "Seven days", "Three days", "Ten days"),
        ask("Genesis 1", "What did God create on the first day?", "Light", "The sun and moon", "Sea creatures", "Human beings"),
        ask("Genesis 2", "What did God use to form the first man, according to Genesis 2?", "Dust from the ground", "Stones from a mountain", "Water from the sea", "Fire from heaven"),
        ask("Genesis 2", "What did God breathe into the man so that he became a living being?", "The breath of life", "A flame of fire", "A name from heaven", "A song of praise"),
        ask("Genesis 1", "On which day did God create the plants and trees?", "The third day", "The first day", "The fifth day", "The seventh day"),
        ask("Genesis 1", "On which day did God create the birds and the sea creatures?", "The fifth day", "The second day", "The sixth day", "The third day"),
        ask("Genesis 1", "What did God give people to eat in Genesis 1?", "Seed-bearing plants and fruit from trees", "Only fish from the sea", "Only honey and bread", "Roasted meat from the flocks"),
    ],
    "Eden and the Fall": [
        ask("Genesis 2", "According to Genesis 2, what did God use to make the first woman?", "One of Adam's ribs", "Dust from the garden", "A branch from the tree", "Water from the river"),
        ask("Genesis 3", "What name did Adam give his wife?", "Eve", "Sarah", "Naomi", "Leah"),
        ask("Genesis 3", "What did God make for Adam and Eve to wear when they left the garden?", "Garments of skin", "Robes of silk", "Crowns of gold", "Cloaks of wool"),
        ask("Genesis 4", "Which son was born to Adam and Eve after Abel's death?", "Seth", "Noah", "Isaac", "Shem"),
        ask("Genesis 2", "Which two special trees stood in the middle of the garden?", "The tree of life and the tree of the knowledge of good and evil", "The olive tree and the fig tree", "The cedar tree and the palm tree", "The vine and the pomegranate"),
        ask("Genesis 3", "What did Adam and Eve sew together to cover themselves?", "Fig leaves", "Palm leaves", "Animal skins", "Cloth from Egypt"),
        ask("Genesis 4", "What did God ask Cain after Abel was killed?", "Where is your brother Abel?", "Why did you leave the garden?", "What have you built?", "Who is your father?"),
    ],
    "Noah's Ark": [
        ask("Genesis 6", "What kind of wood did God tell Noah to use for the ark?", "Gopher wood", "Cedar wood", "Olive wood", "Acacia wood"),
        ask("Genesis 7", "Who shut the door of the ark once Noah and the animals were inside?", "The Lord", "Noah", "Shem", "An angel"),
        ask("Genesis 8", "On which mountains did the ark come to rest?", "The mountains of Ararat", "Mount Sinai", "Mount Carmel", "Mount Zion"),
        ask("Genesis 7", "How old was Noah when the flood came?", "Six hundred years old", "One hundred twenty years old", "Three hundred years old", "Nine hundred fifty years old"),
        ask("Genesis 7", "Who went into the ark with Noah?", "His wife, his sons and their wives", "Only his three sons", "Abraham and Sarah", "His servants and neighbors"),
        ask("Genesis 9", "What did God promise after the flood?", "Never again to destroy all life with a flood", "To send a flood every hundred years", "To remove the rainbow", "To rebuild the ark"),
        ask("Genesis 9", "What did God tell Noah and his sons to do after the flood?", "Be fruitful, multiply and fill the earth", "Build a great tower", "Leave the land at once", "Count all the animals"),
    ],
    "Abraham's Promise": [
        ask("Genesis 12", "Which land did God promise to Abraham's descendants?", "Canaan", "Egypt", "Babylon", "Persia"),
        ask("Genesis 12", "Which nephew traveled with Abraham to Canaan?", "Lot", "Laban", "Esau", "Eli"),
        ask("Genesis 18", "How did Sarah react when she heard she would have a child in her old age?", "She laughed", "She wept", "She built an altar", "She sang a song"),
        ask("Genesis 14", "What did Abraham give to Melchizedek after the battle in Genesis 14?", "A tenth of everything", "A flock of sheep", "His sword", "A golden cup"),
        ask("Genesis 11", "From which city did Abram's family set out toward Canaan?", "Ur of the Chaldeans", "Babylon", "Nineveh", "Jericho"),
        ask("Genesis 15", "How did Abram respond when God promised him descendants like the stars?", "He believed the Lord", "He laughed and walked away", "He built a tower", "He asked for gold"),
        ask("Genesis 21", "What did Sarah say when Isaac was born?", "God has made me laugh", "God has made me queen", "God has given me a house", "God has sent me a servant"),
    ],
    "Jacob and Joseph": [
        ask("Genesis 35", "How many sons did Jacob have?", "Twelve", "Ten", "Seven", "Three"),
        ask("Genesis 28", "What did Jacob dream about at Bethel?", "A ladder reaching to heaven", "A great flood", "A burning bush", "A golden calf"),
        ask("Genesis 37", "How much did Joseph's brothers sell him for?", "Twenty shekels of silver", "Thirty pieces of silver", "Ten gold coins", "One talent of gold"),
        ask("Genesis 39", "Who falsely accused Joseph, which sent him to prison?", "Potiphar's wife", "Pharaoh's baker", "Reuben", "Benjamin"),
        ask("Genesis 25", "What did Esau trade his birthright for?", "A bowl of lentil stew", "A flock of sheep", "A bag of silver", "A field of wheat"),
        ask("Genesis 29", "Which woman did Jacob first work seven years to marry?", "Rachel", "Leah", "Rebekah", "Sarah"),
        ask("Genesis 43", "Who was Joseph's youngest brother, whom he asked his family to bring to Egypt?", "Benjamin", "Reuben", "Judah", "Simeon"),
    ],
    "Moses and the Exodus": [
        ask("Exodus 4", "What did Moses' staff become when he threw it on the ground?", "A snake", "A river", "A sword", "A tree"),
        ask("Exodus 7", "What was the first plague God sent on Egypt?", "Water turning to blood", "Frogs", "Darkness", "Locusts"),
        ask("Exodus 12", "What did the Israelites put on their doorposts at the first Passover?", "The blood of a lamb", "Olive oil", "Palm branches", "Gold dust"),
        ask("Exodus 2", "Who was Moses' sister who watched over him in the basket on the Nile?", "Miriam", "Zipporah", "Deborah", "Rahab"),
        ask("Exodus 1", "Into which river did Pharaoh order Hebrew baby boys to be thrown?", "The Nile", "The Jordan", "The Euphrates", "The Red Sea"),
        ask("Exodus 12", "What bread did Israel eat at Passover because they left in a hurry?", "Unleavened bread", "Honey cakes", "Roasted fish", "Figs and dates"),
        ask("Exodus 12", "What did Pharaoh say after the death of the firstborn?", "Go, leave my people and serve the Lord", "Stay and build me a city", "Send your children back", "Return with more gold"),
    ],
    "The Wilderness and God's Law": [
        ask("Numbers 14", "How long did Israel wander in the wilderness?", "Forty years", "Seven years", "Four hundred years", "Twelve years"),
        ask("Exodus 31", "What were the Ten Commandments written on?", "Stone tablets", "Gold plates", "Scrolls of papyrus", "Wooden boards"),
        ask("Exodus 40", "What was the portable tent where God's presence stayed with Israel called?", "The tabernacle", "The temple", "The synagogue", "The palace"),
        ask("Exodus 17", "Who held up Moses' hands during the battle against the Amalekites?", "Aaron and Hur", "Joshua and Caleb", "Miriam and Jethro", "Eleazar and Gershom"),
        ask("Exodus 32", "Who made the golden calf when the people grew impatient?", "Aaron", "Joshua", "Caleb", "Moses"),
        ask("Exodus 25", "Which sacred chest held the tablets of the law?", "The ark of the covenant", "The golden table", "The altar of incense", "The bronze basin"),
        ask("Exodus 34", "What happened to Moses' face after he spoke with God on the mountain?", "It shone brightly", "It turned pale", "It grew dark", "It was covered in ash"),
    ],
    "Jericho and the Judges": [
        ask("Joshua 2", "What did Rahab hang from her window to mark her house?", "A scarlet cord", "A white banner", "A golden lamp", "A blue curtain"),
        ask("Judges 7", "How many men did Gideon keep to fight the Midianites?", "Three hundred", "Ten thousand", "Thirty", "One thousand"),
        ask("Judges 7", "What did Gideon's men carry besides trumpets?", "Jars with torches inside", "Swords of gold", "Shields of bronze", "Slings and stones"),
        ask("Judges 16", "What did Samson push down in his final act?", "The pillars of the Philistine temple", "The walls of Jericho", "The tower of Babel", "Pharaoh's palace"),
        ask("Joshua 3", "What happened when the priests carrying the ark stepped into the Jordan River?", "The waters stopped flowing", "The river turned to blood", "A bridge appeared from heaven", "Boats arrived"),
        ask("Judges 4", "Who struck down the enemy commander Sisera?", "Jael", "Deborah", "Ruth", "Rahab"),
        ask("Judges 13", "Who announced Samson's birth to his mother?", "An angel of the Lord", "A prophet from Gilgal", "A Philistine king", "Joshua"),
    ],
    "David and Goliath": [
        ask("1 Samuel 10", "Who was the first king of Israel?", "Saul", "David", "Solomon", "Samuel"),
        ask("1 Samuel 16", "What was the name of David's father?", "Jesse", "Saul", "Abner", "Eli"),
        ask("1 Samuel 16", "What instrument did David play to calm King Saul?", "A harp", "A trumpet", "A drum", "A flute"),
        ask("1 Samuel 18", "Who was David's close friend, the son of King Saul?", "Jonathan", "Absalom", "Joab", "Abner"),
        ask("1 Samuel 17", "For how many days did Goliath challenge the army of Israel?", "Forty days", "Three days", "Seven days", "Twelve days"),
        ask("1 Samuel 17", "Which older brother spoke angrily to David on the battlefield?", "Eliab", "Jonathan", "Absalom", "Joab"),
        ask("1 Samuel 17", "What did Jesse send David to bring to his brothers?", "Roasted grain, bread and cheese", "Swords and shields", "Gold and silver", "Letters from King Saul"),
    ],
    "Daniel and the Lions": [
        ask("Daniel 1", "What did Daniel and his friends ask to eat instead of the king's food?", "Vegetables and water", "Roasted lamb and wine", "Honey cakes", "Fish and bread"),
        ask("Daniel 5", "At King Belshazzar's feast, what mysterious thing appeared on the wall?", "A hand writing words", "A burning bush", "A rainbow", "A lion's face"),
        ask("Daniel 3", "What did King Nebuchadnezzar build that everyone was ordered to worship?", "A golden statue", "A great temple", "A tower of bricks", "A silver altar"),
        ask("Daniel 3", "How many men did the king see walking in the fiery furnace?", "Four", "Three", "Two", "Seven"),
        ask("Daniel 1", "What new name did the Babylonians give Daniel?", "Belteshazzar", "Abednego", "Meshach", "Shadrach"),
        ask("Daniel 6", "Which way did Daniel face when he prayed three times a day?", "Toward Jerusalem", "Toward Babylon", "Toward the sea", "Toward the sun"),
        ask("Daniel 2", "Who explained King Nebuchadnezzar's dream about a great statue?", "Daniel", "Joseph", "Ezekiel", "Mordecai"),
    ],
    "The Life and Teachings of Jesus": [
        ask("Matthew 3", "Who baptized Jesus in the Jordan River?", "John the Baptist", "Peter", "Andrew", "Elijah"),
        ask("Luke 6", "How many apostles did Jesus choose?", "Twelve", "Seven", "Ten", "Seventy"),
        ask("John 2", "What did Jesus turn water into at the wedding in Cana?", "Wine", "Milk", "Oil", "Honey"),
        ask("Matthew 7", "In Jesus' parable, what did the wise man build his house on?", "A rock", "Sand", "A hill of gold", "A riverbank"),
        ask("Matthew 2", "Who traveled from the east to visit the child Jesus?", "Wise men", "Roman soldiers", "The Pharisees", "Fishermen"),
        ask("Mark 4", "What did Jesus calm on the Sea of Galilee?", "A great storm with wind and waves", "A flood in Egypt", "A fire in the temple", "A riot in the city"),
        ask("John 11", "Whom did Jesus raise from the dead after four days in the tomb?", "Lazarus", "Jairus' daughter", "Zacchaeus", "Nicodemus"),
    ],
    "The Cross and Resurrection": [
        ask("Matthew 26", "How many pieces of silver was Judas paid to betray Jesus?", "Thirty", "Twenty", "Ten", "One hundred"),
        ask("Matthew 26", "How did Judas show the soldiers which man was Jesus?", "With a kiss", "With a handshake", "With a torch", "With a shout"),
        ask("John 20", "Which disciple said he would not believe until he saw Jesus' wounds?", "Thomas", "Peter", "Matthew", "Philip"),
        ask("Luke 24", "On the day of the resurrection, Jesus walked with two disciples on the road to where?", "Emmaus", "Jericho", "Damascus", "Egypt"),
        ask("Luke 23", "What did Jesus say from the cross about those who crucified Him?", "Father, forgive them", "Let them be punished", "Call down fire from heaven", "Leave Me alone"),
        ask("John 19", "What did the soldiers cast lots for at the cross?", "Jesus' clothes", "The cross itself", "His crown of thorns", "The tomb"),
        ask("Luke 24", "What had been rolled away from the tomb when the women arrived?", "The stone", "The cloth", "The gate", "The roof"),
    ],
}

# ─── BRAND NEW STAGES ─────────────────────────────────────────────────
# Each entry says which existing stage it follows. They are processed in
# order, so a new stage can also follow another new stage.

NEW_STAGES = [
    {
        "after": "Jericho and the Judges",
        "stage": {
            "name": "Ruth's Loyalty",
            "reference": "Ruth 1-4",
            "story": (
                "During the time of the judges, Naomi loses her husband and "
                "sons in Moab. Her daughter-in-law Ruth chooses to stay with "
                "her and follow her God. In Bethlehem, Ruth gathers grain in "
                "the fields of Boaz, who treats her with kindness."
            ),
            "lesson": (
                "Lesson: Loyalty and kindness change lives. Small acts of "
                "faithfulness can shape a whole family's future."
            ),
            "time_limit": 15,
            "questions": [
                ask("Ruth 1", "Who was Ruth's mother-in-law?", "Naomi", "Orpah", "Rahab", "Hannah"),
                ask("Ruth 1", "From which land did Ruth come?", "Moab", "Egypt", "Babylon", "Philistia"),
                ask("Ruth 1", "Which daughter-in-law of Naomi returned to her own people?", "Orpah", "Ruth", "Rahab", "Hannah"),
                ask("Ruth 1", "What famous promise did Ruth make to Naomi?", "Your people will be my people and your God my God", "I will return to Moab", "I will build you a house", "I will serve the king"),
                ask("Ruth 1", "To which town did Naomi and Ruth return?", "Bethlehem", "Jericho", "Nazareth", "Hebron"),
                ask("Ruth 2", "What work did Ruth do in the fields?", "She gathered leftover grain", "She tended sheep", "She built walls", "She sold fish"),
                ask("Ruth 2", "Who was the kind landowner who noticed Ruth?", "Boaz", "Eli", "Jesse", "Obed"),
                ask("Ruth 3 and 4", "What was Boaz to Naomi's family?", "A close relative who could redeem it", "A Philistine soldier", "A priest from Egypt", "A prophet from Gilgal"),
                ask("Ruth 4", "What was the name of the son of Ruth and Boaz?", "Obed", "Jesse", "David", "Solomon"),
                ask("Ruth 4", "Who was Ruth's famous great-grandson?", "David", "Solomon", "Samuel", "Saul"),
                ask("Ruth 1", "What name did Naomi ask to be called because of her sorrow?", "Mara", "Miriam", "Rachel", "Leah"),
                ask("Ruth 3", "What did Boaz give Ruth to take home to Naomi?", "Six measures of barley", "A golden ring", "A flock of sheep", "A jar of oil"),
                ask("Ruth 4", "Where did Boaz settle the matter of redeeming Ruth's family?", "At the town gate", "In the temple", "At the river", "In Moab"),
            ],
        },
    },
    {
        "after": "David and Goliath",
        "stage": {
            "name": "Solomon's Wisdom",
            "reference": "1 Kings 3-8",
            "story": (
                "David's son Solomon becomes king. When God offers him "
                "anything he wants, Solomon asks for wisdom to lead God's "
                "people. He later builds a magnificent temple in Jerusalem."
            ),
            "lesson": (
                "Lesson: Wisdom is worth more than wealth. Ask for guidance, "
                "listen carefully, and use leadership to serve others."
            ),
            "time_limit": 14,
            "questions": [
                ask("1 Kings 1", "Who was Solomon's father?", "David", "Saul", "Jesse", "Nathan"),
                ask("1 Kings 3", "What did Solomon ask God for?", "A wise and understanding heart", "Great wealth", "A long life", "Victory over his enemies"),
                ask("1 Kings 3", "What did God add to Solomon's wisdom as a gift?", "Riches and honor", "Control over the weather", "A new name", "An army of angels"),
                ask("1 Kings 3", "How did Solomon test the two women who both claimed a baby?", "He offered to divide the child with a sword", "He asked the elders to vote", "He sent them to a prophet", "He banished both women"),
                ask("1 Kings 6", "What great building did Solomon build in Jerusalem?", "The temple of the Lord", "A pyramid", "A tower to reach heaven", "A lighthouse"),
                ask("1 Kings 6", "How many years did it take to build the temple?", "Seven years", "Two years", "Forty years", "Twelve years"),
                ask("1 Kings 10", "Which queen traveled far to test Solomon's wisdom?", "The Queen of Sheba", "Queen Esther", "Queen Jezebel", "Queen Vashti"),
                ask("Proverbs 1", "Which Bible book contains many of Solomon's wise sayings?", "Proverbs", "Psalms", "Genesis", "Judges"),
                ask("1 Kings 8", "What happened when the ark was brought into the new temple?", "A cloud filled it with God's glory", "The walls split apart", "The ark was carried away", "Snow covered Jerusalem"),
                ask("Proverbs 9", "According to Proverbs 9:10, the fear of the Lord is the beginning of what?", "Wisdom", "Wealth", "War", "Winter"),
                ask("1 Kings 1", "Who was Solomon's mother?", "Bathsheba", "Abigail", "Michal", "Tamar"),
                ask("1 Kings 3", "Where did God appear to Solomon in a dream and offer him anything?", "Gibeon", "Bethel", "Mount Sinai", "Hebron"),
                ask("1 Kings 8", "Who dedicated the temple with a long prayer before all Israel?", "Solomon", "Hiram", "David", "Zadok"),
            ],
        },
    },
    {
        "after": "Solomon's Wisdom",
        "stage": {
            "name": "Elijah on Mount Carmel",
            "reference": "1 Kings 17-19",
            "story": (
                "King Ahab leads Israel to worship Baal. The prophet Elijah "
                "challenges the prophets of Baal on Mount Carmel to show who "
                "is the true God. Fire falls from heaven, and the people "
                "declare that the Lord is God."
            ),
            "lesson": (
                "Lesson: Stand for what is true even when you feel alone. "
                "God can speak in quiet moments, not only in loud ones."
            ),
            "time_limit": 14,
            "questions": [
                ask("1 Kings 18", "Who challenged the prophets of Baal on Mount Carmel?", "Elijah", "Elisha", "Isaiah", "Jeremiah"),
                ask("1 Kings 17", "Who was king of Israel in Elijah's time?", "Ahab", "David", "Herod", "Darius"),
                ask("1 Kings 17", "What did Elijah announce would stop falling on the land?", "Rain", "Snow", "Manna", "Hail"),
                ask("1 Kings 17", "Which creatures brought Elijah food by the brook Cherith?", "Ravens", "Doves", "Eagles", "Sparrows"),
                ask("1 Kings 17", "What happened to the widow's jar of flour and jug of oil?", "They never ran out", "They turned to gold", "They dried up", "They overflowed into a river"),
                ask("1 Kings 18", "On which mountain did Elijah face the prophets of Baal?", "Mount Carmel", "Mount Sinai", "Mount Ararat", "The Mount of Olives"),
                ask("1 Kings 18", "What did Elijah pray would fall on the altar?", "Fire from heaven", "Rain", "Manna", "Gold"),
                ask("1 Kings 18", "What did Elijah pour over the offering before he prayed?", "Water", "Oil", "Wine", "Milk"),
                ask("1 Kings 18", "What did the people say when the fire fell?", "The Lord, He is God!", "Baal is God!", "Ahab is king!", "Peace be with you!"),
                ask("1 Kings 19", "How did God speak to Elijah at Horeb after the wind, earthquake and fire?", "In a gentle whisper", "In a loud trumpet blast", "Through a burning bush", "In thunder and lightning"),
                ask("1 Kings 19", "Whom did God choose to take Elijah's place as prophet?", "Elisha", "Isaiah", "Jeremiah", "Amos"),
                ask("2 Kings 2", "How did Elijah leave the earth?", "A chariot of fire in a whirlwind", "A cloud covered him", "A great fish carried him", "A ladder was lowered"),
                ask("1 Kings 19", "Which wicked queen threatened Elijah's life?", "Jezebel", "Athaliah", "Esther", "Vashti"),
            ],
        },
    },
    {
        "after": "Elijah on Mount Carmel",
        "stage": {
            "name": "Jonah and the Great Fish",
            "reference": "Jonah 1-4",
            "story": (
                "God tells Jonah to warn the great city of Nineveh. Jonah "
                "runs the other way by ship, a storm rises, and he is "
                "swallowed by a great fish. After he prays and obeys, "
                "Nineveh listens and turns back to God."
            ),
            "lesson": (
                "Lesson: Running from a hard responsibility rarely helps. "
                "Mercy is for everyone, even when showing it is uncomfortable."
            ),
            "time_limit": 14,
            "questions": [
                ask("Jonah 1", "To which city did God send Jonah?", "Nineveh", "Babylon", "Jerusalem", "Damascus"),
                ask("Jonah 1", "Where did Jonah try to flee by ship?", "Tarshish", "Egypt", "Nineveh", "Bethlehem"),
                ask("Jonah 1", "What happened to the sea after Jonah boarded the ship?", "A great storm arose", "It froze", "It turned red", "It dried up"),
                ask("Jonah 1", "What did the sailors do to calm the storm?", "Threw Jonah into the sea", "Lowered the sails and waited", "Tied the ship to a rock", "Sailed straight to Nineveh"),
                ask("Jonah 1", "What swallowed Jonah?", "A great fish", "A giant octopus", "A sea serpent", "A crocodile"),
                ask("Jonah 1", "How long was Jonah inside the fish?", "Three days and three nights", "One day", "Seven days", "Forty days"),
                ask("Jonah 2", "What did Jonah do inside the fish?", "He prayed to God", "He fell asleep", "He cursed the sea", "He sent a letter"),
                ask("Jonah 3", "What message did Jonah bring to Nineveh?", "The city would be overthrown in forty days", "The city would receive great riches", "A new king would rule", "A flood was coming"),
                ask("Jonah 3", "How did the people of Nineveh respond?", "They repented and turned from evil", "They imprisoned Jonah", "They ignored him", "They built a wall"),
                ask("Jonah 4", "What did God provide to shade Jonah outside the city?", "A leafy plant", "A palm tree", "A cloud", "A stone wall"),
                ask("Jonah 1", "What was Jonah doing while the storm raged?", "Sleeping below deck", "Steering the ship", "Praying at the mast", "Swimming"),
                ask("Jonah 2", "Where did the fish put Jonah after he prayed?", "On dry land", "In Nineveh", "On another ship", "In the harbor"),
                ask("Jonah 4", "Why was Jonah upset after Nineveh was spared?", "God showed mercy to the city", "The fish had left him", "The city was destroyed", "The king jailed him"),
            ],
        },
    },
    {
        "after": "Daniel and the Lions",
        "stage": {
            "name": "Esther's Courage",
            "reference": "Esther 1-9",
            "story": (
                "Esther, a Jewish queen in Persia, learns of a plot to "
                "destroy her people. With her cousin Mordecai's "
                "encouragement, she bravely approaches the king, even though "
                "it could cost her life."
            ),
            "lesson": (
                "Lesson: Courage often means speaking up at the right time. "
                "You may be able to help others because of where you are."
            ),
            "time_limit": 13,
            "questions": [
                ask("Esther 2", "Who was Esther's cousin who raised her?", "Mordecai", "Haman", "Nehemiah", "Ezra"),
                ask("Esther 1", "In which empire did Esther become queen?", "Persia", "Egypt", "Rome", "Assyria"),
                ask("Esther 2", "Which king chose Esther as his queen?", "Xerxes (Ahasuerus)", "Nebuchadnezzar", "Herod", "Pharaoh"),
                ask("Esther 3", "Who plotted to destroy the Jewish people?", "Haman", "Mordecai", "Hegai", "Herod"),
                ask("Esther 4", "What did Esther ask the Jews to do before she approached the king?", "Fast for three days", "Build an altar", "March around the city", "Send gifts to Haman"),
                ask("Esther 4", "What did Esther say as she chose to go to the king?", "If I perish, I perish", "I will never return", "I will not go", "God has left us"),
                ask("Esther 5", "What did the king hold out to Esther when she approached?", "His golden scepter", "His royal sword", "A golden cup", "A scroll"),
                ask("Esther 5", "What did Esther invite the king and Haman to?", "A banquet", "A battle", "A wedding", "A hunt"),
                ask("Esther 7", "What happened to Haman in the end?", "He was hanged on the gallows he built for Mordecai", "He escaped to Egypt", "He became king", "He was forgiven and honored"),
                ask("Esther 9", "Which festival remembers the rescue of the Jews in Esther's time?", "Purim", "Passover", "Pentecost", "Hanukkah"),
                ask("Esther 1", "Which queen lost her position when she refused the king's command?", "Vashti", "Jezebel", "Sheba", "Athaliah"),
                ask("Esther 2", "What was Esther's Hebrew name?", "Hadassah", "Miriam", "Naomi", "Deborah"),
                ask("Esther 2", "What did Mordecai discover that saved the king's life?", "A plot to kill the king", "A hidden army", "A coming flood", "A theft in the treasury"),
            ],
        },
    },
    {
        "after": "The Cross and Resurrection",
        "stage": {
            "name": "The Early Church and Paul",
            "reference": "Acts 2, 9, 11, 16",
            "story": (
                "After Jesus returns to heaven, the Holy Spirit comes at "
                "Pentecost and the church grows. Saul, who once opposed "
                "believers, meets Jesus on the road to Damascus, becomes Paul, "
                "and carries the good news to many cities."
            ),
            "lesson": (
                "Lesson: People can change. Share good news with courage, "
                "forgive past mistakes, and keep serving through hardship."
            ),
            "time_limit": 12,
            "questions": [
                ask("Acts 2", "Which festival was happening when the Holy Spirit came in Acts 2?", "Pentecost", "Passover", "Purim", "Tabernacles"),
                ask("Acts 2", "What appeared above the disciples at Pentecost?", "Tongues of fire", "Rainbows", "Doves", "Stars"),
                ask("Acts 2", "Who preached to the crowd on the day of Pentecost?", "Peter", "Paul", "James", "Thomas"),
                ask("Acts 9", "What was Paul's name before he was known as Paul?", "Saul", "Silas", "Simon", "Stephen"),
                ask("Acts 9", "On the road to which city did Saul meet Jesus?", "Damascus", "Jericho", "Jerusalem", "Antioch"),
                ask("Acts 9", "What happened to Saul when Jesus spoke to him?", "A bright light blinded him", "He lost his voice", "He fell into the sea", "He became a king"),
                ask("Acts 9", "Who was sent to help Saul regain his sight?", "Ananias", "Barnabas", "Silas", "Timothy"),
                ask("Acts 13", "Who traveled with Paul on his first missionary journey?", "Barnabas", "Peter", "Joshua", "Nehemiah"),
                ask("Acts 16", "Which two men sang hymns in prison at midnight in Philippi?", "Paul and Silas", "Peter and John", "Daniel and Shadrach", "Aaron and Hur"),
                ask("Acts 11", "In which city were the followers of Jesus first called Christians?", "Antioch", "Rome", "Bethlehem", "Corinth"),
                ask("Acts 7", "Who became the first Christian martyr when he was stoned?", "Stephen", "Peter", "James", "Barnabas"),
                ask("Acts 10", "To which Roman centurion did Peter bring the good news?", "Cornelius", "Pilate", "Julius", "Festus"),
                ask("Acts 27", "What struck the ship on Paul's journey to Rome?", "A great storm", "A sea monster", "A fire", "A pirate attack"),
            ],
        },
    },
]


# ─── MERGING EVERYTHING TOGETHER ──────────────────────────────────────

def build_journey(base_locations):
    """
    Combine the original stages with reading hints, extra questions and new stages.

    Args:
        base_locations (list): The LOCATIONS list from questions.py

    Returns:
        list: The complete list of Bible story stages in order, as new
        dictionaries (the original list is not changed)

    Raises:
        ValueError: If a stage name in this file does not exist, which
        usually means a typo in a name.
    """
    known_names = {location["name"] for location in base_locations}

    # Catch typos early: every key must be a real stage name
    for table in (EXTRA_QUESTIONS, BASE_READINGS):
        for name in table:
            if name not in known_names:
                raise ValueError(
                    f"extra_questions.py: there is no stage named '{name}' "
                    "in questions.py")

    # Step 1: copy every original stage, attach reading hints, add extras
    journey = []
    for location in base_locations:
        readings = BASE_READINGS.get(location["name"])
        originals = location["questions"]
        if readings and len(readings) != len(originals):
            print(f"[warning] '{location['name']}' has {len(originals)} "
                  f"questions but {len(readings)} reading hints, so its "
                  "hints will use the stage reference instead.")
            readings = None

        questions = []
        for i, question in enumerate(originals):
            item = dict(question)
            if readings:
                item["read"] = readings[i]
            questions.append(item)

        merged = dict(location)
        merged["questions"] = questions + EXTRA_QUESTIONS.get(
            location["name"], [])
        journey.append(merged)

    # Step 2: insert each new stage right after the stage it follows
    for entry in NEW_STAGES:
        names = [stage["name"] for stage in journey]
        if entry["after"] not in names:
            raise ValueError(
                f"extra_questions.py: cannot place "
                f"'{entry['stage']['name']}' after '{entry['after']}'")
        journey.insert(names.index(entry["after"]) + 1, entry["stage"])

    return journey