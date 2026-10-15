"""
questions.py - BibleTales story, lesson, and quiz data.

DATA RULES
----------
* Each dictionary in LOCATIONS represents one playable story level.
* ``reference`` gives the main Bible passage for the level.
* ``story`` is the short narrative shown before the quiz.
* ``lesson`` highlights a practical faith or character takeaway.
* ``questions`` contains the quiz questions for that level.
* IMPORTANT: the first answer passed to ``make_question`` is always correct.
  main.py shuffles the options when a question is loaded, so players cannot
  rely on the correct answer always appearing in the first position.

The data is kept separate from main.py so new levels and questions can be
added without changing the game's screen logic.
"""

def make_question(question, correct_answer, *distractors):
    """Build one quiz question using the game's expected data structure."""
    if len(distractors) < 3:
        raise ValueError("Every question must have at least three distractors.")
    options = [correct_answer, *distractors]
    if len(set(options)) != len(options):
        raise ValueError(f"Duplicate answer option in question: {question}")
    return {"q": question, "options": options}


LOCATIONS = [
    {
        "name": "Creation",
        "reference": "Genesis 1-2",
        "story": (
            "God creates the heavens and the earth, fills the world with life, "
            "and makes human beings in His image. He rests on the seventh day."
        ),
        "lesson": (
            "Lesson: Creation reminds us to care for God's world, value every "
            "person, and make time for rest."
        ),
        "time_limit": 20,
        "pos": (100, 180),
        "questions": [
            make_question("What did God create in the beginning?", "The heavens and the earth", "The temple and the city", "The sea and one mountain", "The sun and moon only"),
            make_question("What did God say when He saw the light?", "That it was good", "That it was too bright", "That it should disappear", "That it was unfinished"),
            make_question("What did God call the light?", "Day", "Morning star", "Sunlight", "Heaven"),
            make_question("What did God call the darkness?", "Night", "Evening", "Shadow", "The deep"),
            make_question("What did God place in the sky to mark signs, seasons, days, and years?", "The sun, moon, and stars", "Only clouds", "Mountains and rivers", "Angels with trumpets"),
            make_question("What creatures were told to fill the seas?", "Sea creatures", "Only birds", "Only cattle", "Trees"),
            make_question("On which day did God create human beings, according to Genesis 1?", "The sixth day", "The first day", "The fourth day", "The seventh day"),
            make_question("In whose image were human beings created?", "God's image", "Adam's image only", "The angels' image", "The image of the stars"),
            make_question("What responsibility did God give humanity concerning the earth?", "To rule over and care for living creation", "To destroy every plant", "To leave the earth immediately", "To worship the sun"),
            make_question("What did God do on the seventh day?", "Rested from His work", "Created another ocean", "Made Adam's clothes", "Built an ark"),
        ],
    },
    {
        "name": "Eden and the Fall",
        "reference": "Genesis 2-4",
        "story": (
            "Adam and Eve live in Eden, but the serpent tempts them to disobey "
            "God. Sin enters the story, and later Cain becomes jealous of Abel."
        ),
        "lesson": (
            "Lesson: Choices have consequences. Be honest about wrongdoing, "
            "resist temptation, and do not let jealousy control your actions."
        ),
        "time_limit": 20,
        "pos": (190, 360),
        "questions": [
            make_question("What was the name of the garden where Adam and Eve lived?", "Eden", "Gethsemane", "Carmel", "Sharon"),
            make_question("What was Adam instructed to do in the garden?", "Work it and take care of it", "Build a large ship", "Find the Promised Land", "Rule Egypt"),
            make_question("Which tree were Adam and Eve told not to eat from?", "The tree of the knowledge of good and evil", "The tree of life only", "The olive tree", "The cedar tree"),
            make_question("Which creature spoke to Eve in the account of the fall?", "The serpent", "A dove", "A lion", "A raven"),
            make_question("What did Adam and Eve realize after eating the forbidden fruit?", "That they were naked", "That they could fly", "That the garden had flooded", "That they had become kings"),
            make_question("What did Adam and Eve do when they heard God in the garden?", "They hid", "They built an altar", "They left for Egypt", "They climbed a mountain"),
            make_question("Who was Adam and Eve's first son mentioned in Genesis 4?", "Cain", "Seth", "Enoch", "Noah"),
            make_question("What was Abel's occupation?", "Shepherd", "Builder of ships", "King", "Tax collector"),
            make_question("Why was Cain angry with Abel?", "God looked with favor on Abel and his offering", "Abel had stolen a boat", "Abel had become Pharaoh", "Abel had hidden the ark"),
            make_question("What did Cain do to Abel?", "Killed him", "Sent him to Nineveh", "Made him a king", "Sold him to Pharaoh"),
        ],
    },
    {
        "name": "Noah's Ark",
        "reference": "Genesis 6-9",
        "story": (
            "The earth is filled with violence, but Noah finds favor with God. "
            "Noah builds an ark, brings his family and animals aboard, and "
            "survives the flood. God makes a covenant afterward."
        ),
        "lesson": (
            "Lesson: Faithfulness means obeying God even when a task is hard. "
            "God's covenant also reminds us to remember our responsibilities."
        ),
        "time_limit": 19,
        "pos": (280, 180),
        "questions": [
            make_question("Who built the ark?", "Noah", "Abraham", "Moses", "Joshua"),
            make_question("Why did Noah build the ark?", "God warned him about the coming flood", "He wanted to become a fisherman", "Pharaoh ordered him to", "He was preparing for a war"),
            make_question("How many sons did Noah have?", "Three", "One", "Two", "Twelve"),
            make_question("Which names belong to Noah's sons?", "Shem, Ham, and Japheth", "Cain, Abel, and Seth", "Saul, David, and Solomon", "Peter, James, and John"),
            make_question("What covered the earth during the flood?", "Water", "Sand", "Ash", "Snow"),
            make_question("How long did rain fall during the flood?", "Forty days and forty nights", "Seven hours", "Twelve days", "One hundred days"),
            make_question("Which bird returned with a fresh olive leaf?", "A dove", "An eagle", "A sparrow", "A peacock"),
            make_question("What did Noah send out before the dove?", "A raven", "A swan", "A rooster", "A parrot"),
            make_question("What sign did God give as a sign of His covenant with the earth?", "A rainbow", "A burning bush", "A pillar of salt", "A golden calf"),
            make_question("What did Noah do after leaving the ark?", "Built an altar to the Lord", "Crowned himself king of Egypt", "Built the walls of Jericho", "Returned to Eden"),
        ],
    },
    {
        "name": "Abraham's Promise",
        "reference": "Genesis 12, 15, 17, 21-22",
        "story": (
            "God calls Abram to leave his homeland and promises to make a great "
            "nation from him. Abram trusts God's promise, and Isaac is born in "
            "his old age."
        ),
        "lesson": (
            "Lesson: Trust can mean taking a step before you know the whole "
            "journey. Patience and faith help us hold on to God's promises."
        ),
        "time_limit": 18,
        "pos": (370, 370),
        "questions": [
            make_question("What was Abram's name changed to?", "Abraham", "Abimelech", "Aaron", "Asa"),
            make_question("What did God tell Abram to leave?", "His country, people, and father's household", "The ark", "The city of Jericho", "The land of Egypt after the plagues"),
            make_question("What did God promise to make Abraham?", "A great nation", "A ruler of Rome", "A builder of temples", "A captain of the Philistines"),
            make_question("What did God compare Abraham's descendants to in Genesis 15?", "The stars", "The fish in one river", "The trees of Eden", "The stones of Jericho"),
            make_question("Who was Abraham's wife?", "Sarah", "Rebekah", "Rachel", "Leah"),
            make_question("What was the name of Abraham and Sarah's promised son?", "Isaac", "Ishmael", "Jacob", "Joseph"),
            make_question("How old was Abraham when Isaac was born?", "One hundred years old", "Forty years old", "Seventy years old", "Thirty years old"),
            make_question("What did God ask Abraham to do as a test in Genesis 22?", "Offer Isaac as a sacrifice", "Build a tower in Babel", "Lead Israel out of Egypt", "Fight Goliath"),
            make_question("What did God provide instead of Isaac for the offering?", "A ram", "A dove", "A lamb from Egypt's palace", "A young bull from Pharaoh"),
            make_question("What does Abraham's story especially demonstrate?", "Trust in God's promise", "The importance of building city walls", "How to become king of Babylon", "How to cross the Red Sea"),
        ],
    },
    {
        "name": "Jacob and Joseph",
        "reference": "Genesis 25-50",
        "story": (
            "Jacob's family grows, and Joseph's brothers become jealous of him. "
            "Joseph is taken to Egypt, suffers unjustly, and later rises to "
            "authority, helping many people survive famine."
        ),
        "lesson": (
            "Lesson: Jealousy can harm families, but forgiveness and wise "
            "choices can help bring healing. Hard seasons do not have to be "
            "the end of a person's story."
        ),
        "time_limit": 18,
        "pos": (460, 180),
        "questions": [
            make_question("What was the name of Isaac's wife?", "Rebekah", "Rachel", "Leah", "Miriam"),
            make_question("What were the names of Isaac's twin sons?", "Jacob and Esau", "Cain and Abel", "Ephraim and Manasseh", "Moses and Aaron"),
            make_question("What new name was Jacob given after wrestling through the night?", "Israel", "Judah", "Benjamin", "Edom"),
            make_question("What special garment did Jacob give Joseph?", "A richly ornamented robe", "A crown of gold", "A suit of armor", "A priest's breastplate"),
            make_question("How many dreams about future events did Joseph tell his brothers and family in Genesis 37?", "Two", "One", "Three", "Seven"),
            make_question("Where was Joseph taken after his brothers sold him?", "Egypt", "Moab", "Nineveh", "Jerusalem"),
            make_question("Whose dreams did Joseph interpret while in prison?", "The cupbearer and the baker", "Moses and Aaron", "David and Saul", "Peter and John"),
            make_question("What did Pharaoh's dreams warn about?", "Seven years of plenty followed by seven years of famine", "A flood lasting forty days", "The fall of Jericho", "The birth of a new king in Bethlehem"),
            make_question("What position did Joseph receive in Egypt?", "A high position overseeing the land under Pharaoh", "Leader of the Philistine army", "King of Israel", "Chief builder of the ark"),
            make_question("How did Joseph respond when he later met his brothers?", "He eventually forgave them and provided food", "He sent them into the sea", "He refused to speak to anyone", "He made them build Jericho"),
        ],
    },
    {
        "name": "Moses and the Exodus",
        "reference": "Exodus 1-14",
        "story": (
            "God calls Moses to confront Pharaoh and lead the Israelites out "
            "of slavery. After the plagues, Israel leaves Egypt, and God opens "
            "a path through the sea."
        ),
        "lesson": (
            "Lesson: Courage is not the absence of fear; it is taking the "
            "right step while trusting God and seeking help when needed."
        ),
        "time_limit": 17,
        "pos": (550, 370),
        "questions": [
            make_question("Who was Moses' brother and spokesman?", "Aaron", "Caleb", "Joshua", "Gideon"),
            make_question("Who found baby Moses among the reeds by the Nile?", "Pharaoh's daughter", "Sarah", "Rahab", "Deborah"),
            make_question("What unusual sight did Moses see at Horeb?", "A bush that burned without being consumed", "A river turning to stone", "A ladder reaching the stars", "A city wall falling"),
            make_question("What did God tell Moses to remove because the ground was holy?", "His sandals", "His robe", "His staff", "His belt"),
            make_question("Who was the ruler of Egypt when Moses demanded Israel's release?", "Pharaoh", "Nebuchadnezzar", "Herod", "Caesar"),
            make_question("What was the final plague described before Israel's departure?", "The death of the firstborn", "Locusts only", "Darkness only", "Water turning to blood"),
            make_question("What meal did the Israelites eat before leaving Egypt?", "The Passover meal", "A harvest feast in Jericho", "A meal on Noah's ark", "A feast at Mount Carmel"),
            make_question("What guided Israel by day in the wilderness?", "A pillar of cloud", "A rainbow", "A flock of doves", "A golden statue"),
            make_question("What guided Israel by night?", "A pillar of fire", "A burning city", "The star of Bethlehem", "A lamp carried by Pharaoh"),
            make_question("What happened when Moses stretched out his hand over the sea?", "God divided the waters so Israel could cross", "The sea became a mountain of ice", "Ships arrived to carry everyone", "The Israelites returned to Egypt"),
        ],
    },
    {
        "name": "The Wilderness and God's Law",
        "reference": "Exodus 16-20; Numbers 13-14",
        "story": (
            "In the wilderness, God provides food and water and gives Israel "
            "His commandments at Mount Sinai. The people must learn trust, "
            "obedience, and faithful living together."
        ),
        "lesson": (
            "Lesson: Gratitude, honesty, rest, and care for others are part "
            "of faithful living. Remember what you have been given."
        ),
        "time_limit": 16,
        "pos": (640, 180),
        "questions": [
            make_question("What food did God provide on the ground in the wilderness?", "Manna", "Grapes from Canaan", "Fish from the Jordan", "Wheat from Egypt"),
            make_question("What birds came to the Israelite camp for food?", "Quail", "Eagles", "Peacocks", "Doves carrying olive leaves"),
            make_question("From what did Moses bring water at Horeb?", "A rock", "A golden bowl", "A fig tree", "A clay oven"),
            make_question("On which mountain did Israel receive the commandments?", "Mount Sinai", "Mount Carmel", "Mount Zion in David's time", "Mount Ararat"),
            make_question("How many commandments are commonly referred to as the Ten Commandments?", "Ten", "Five", "Twelve", "Forty"),
            make_question("Which commandment concerns honoring parents?", "Honor your father and your mother", "You shall not make bricks", "You shall build an altar every morning", "You shall count the stars"),
            make_question("What day was set apart as a Sabbath day of rest?", "The seventh day", "The first day only", "The third day", "The tenth day"),
            make_question("What idol did the people make while Moses was on the mountain?", "A golden calf", "A silver dove", "A bronze serpent in Eden", "A stone lion"),
            make_question("What did the spies explore when sent from the wilderness?", "The land of Canaan", "The land of Rome", "The garden of Eden", "The city of Nineveh"),
            make_question("What did Joshua and Caleb encourage the people to do?", "Trust God and go forward into the land", "Build another ark", "Return to Pharaoh", "Crown a new Egyptian king"),
        ],
    },
    {
        "name": "Jericho and the Judges",
        "reference": "Joshua 2, 6; Judges 4-7, 13-16",
        "story": (
            "Joshua leads Israel into the Promised Land. Jericho's walls fall "
            "after Israel follows God's instructions. Later, judges such as "
            "Deborah and Gideon lead the people, and Samson's strength becomes "
            "part of Israel's story."
        ),
        "lesson": (
            "Lesson: Courage and obedience matter more than appearances. "
            "Use gifts responsibly and remember that strength is not a "
            "substitute for wisdom."
        ),
        "time_limit": 15,
        "pos": (730, 370),
        "questions": [
            make_question("Who succeeded Moses as leader of Israel?", "Joshua", "Aaron", "Gideon", "Samuel"),
            make_question("Who hid the Israelite spies in Jericho?", "Rahab", "Delilah", "Jezebel", "Esther"),
            make_question("What happened to Jericho's walls after Israel followed God's instructions?", "They fell", "They turned to gold", "They floated away", "They became a river"),
            make_question("How many days did Israel march around Jericho before the final day's march?", "Six days", "One day", "Twelve days", "Forty days"),
            make_question("Who was a prophetess and judge in Israel?", "Deborah", "Rachel", "Miriam's daughter Zipporah", "Bathsheba"),
            make_question("What sign did Gideon ask God to give with a fleece?", "That dew would be on the fleece but not the ground, and then the reverse", "That the sea would freeze", "That a wall would be built overnight", "That the sun would never set"),
            make_question("How did Gideon's army become notably small before battle?", "God instructed him to reduce the number of soldiers", "All the soldiers sailed away", "The enemy captured every soldier", "Gideon sent them to build an ark"),
            make_question("What was the source of Samson's special strength in the story's sign?", "His uncut hair as part of his Nazirite vow", "A suit of armor", "A magic ring", "A golden crown"),
            make_question("Who betrayed Samson by learning the secret of his strength?", "Delilah", "Deborah", "Rahab", "Ruth"),
            make_question("What is a repeated theme in the book of Judges?", "Israel turns away, suffers, and cries out for deliverance", "Israel builds the ark", "Israel returns to Eden", "Israel rules the Roman Empire"),
        ],
    },
    {
        "name": "David and Goliath",
        "reference": "1 Samuel 16-17",
        "story": (
            "David, a young shepherd, visits Israel's army and hears Goliath "
            "mocking them. Trusting in the Lord, David faces the giant with a "
            "sling and a stone."
        ),
        "lesson": (
            "Lesson: Do not judge people only by their size or appearance. "
            "Courage grows when you remember what matters and use your gifts "
            "wisely."
        ),
        "time_limit": 14,
        "pos": (820, 180),
        "questions": [
            make_question("Who anointed David to become king?", "Samuel", "Nathan", "Elijah", "Ezra"),
            make_question("What was David's work before facing Goliath?", "Shepherd", "Potter", "Tax collector", "Fisherman"),
            make_question("Which people did Goliath belong to?", "The Philistines", "The Egyptians", "The Assyrians", "The Romans"),
            make_question("From which city was Goliath?", "Gath", "Bethlehem", "Jericho", "Nazareth"),
            make_question("What weapon did David use against Goliath?", "A sling and a stone", "A spear and shield", "A bow and arrow", "A chariot"),
            make_question("How many smooth stones did David choose from the stream?", "Five", "One", "Seven", "Twelve"),
            make_question("Why did David refuse to wear Saul's armor?", "He was not used to it", "It belonged to Goliath", "It was made of gold", "It was too small for Saul"),
            make_question("What did David say gave him confidence to face Goliath?", "The Lord who had delivered him before", "The size of Saul's army", "A secret weapon from Egypt", "A promise from Goliath"),
            make_question("What did David take from Goliath after defeating him?", "Goliath's sword", "His shepherd's staff", "A golden calf", "A stone tablet"),
            make_question("What lesson is often drawn from David's encounter with Goliath?", "Faith and courage can help us face intimidating challenges", "Only the tallest person can lead", "Battles are won by armor alone", "A shepherd cannot serve God"),
        ],
    },
    {
        "name": "Daniel and the Lions",
        "reference": "Daniel 1, 3, 6",
        "story": (
            "Daniel and his friends seek to remain faithful while living in "
            "a foreign empire. Daniel continues to pray despite a royal decree "
            "and is thrown into a den of lions, but God preserves him."
        ),
        "lesson": (
            "Lesson: Keep your integrity when doing what is right becomes "
            "difficult. Respect others, but do not abandon your deepest "
            "convictions under pressure."
        ),
        "time_limit": 13,
        "pos": (900, 370),
        "questions": [
            make_question("In which foreign empire did Daniel serve?", "Babylon", "Egypt", "Rome", "Philistia"),
            make_question("What were the names of Daniel's three friends in Daniel 1?", "Hananiah, Mishael, and Azariah", "Cain, Abel, and Seth", "Shem, Ham, and Japheth", "Peter, James, and John"),
            make_question("What new names were given to Daniel's three friends in Babylon?", "Shadrach, Meshach, and Abednego", "Saul, David, and Solomon", "Moses, Aaron, and Joshua", "Matthew, Mark, and Luke"),
            make_question("What did Daniel continue doing despite the decree against prayer?", "Praying to God", "Worshipping the king as a god", "Building a golden calf", "Refusing to eat ever again"),
            make_question("Where was Daniel thrown because he continued to pray?", "A den of lions", "A fiery furnace", "The Red Sea", "A prison beneath Jericho"),
            make_question("Who was king when Daniel was thrown into the lions' den in Daniel 6?", "Darius", "David", "Herod", "Pharaoh"),
            make_question("What did God do for Daniel in the lions' den?", "Sent an angel to shut the lions' mouths", "Turned the lions into sheep", "Made Daniel invisible forever", "Flooded the den"),
            make_question("What happened to Shadrach, Meshach, and Abednego when they refused to worship the image?", "They were thrown into a fiery furnace", "They were sent to build Jericho", "They crossed the Red Sea", "They were crowned kings"),
            make_question("What did Daniel and his friends demonstrate?", "Faithfulness and integrity under pressure", "The need to worship idols", "That prayer is always easy", "That wisdom is unnecessary"),
            make_question("What should a reader learn from Daniel's example?", "Remain faithful and act with integrity", "Never help people from another nation", "Trust only in political power", "Avoid prayer when it is difficult"),
        ],
    },
    {
        "name": "The Life and Teachings of Jesus",
        "reference": "Luke 2; Matthew 5-7; Mark 4; John 13",
        "story": (
            "Jesus is born in Bethlehem, teaches about God's kingdom, heals "
            "the sick, welcomes outsiders, and calls His followers to love "
            "God and their neighbors."
        ),
        "lesson": (
            "Lesson: Love is shown through mercy, humility, forgiveness, "
            "service, and practical care for people in need."
        ),
        "time_limit": 13,
        "pos": (820, 520),
        "questions": [
            make_question("In which town was Jesus born?", "Bethlehem", "Nazareth", "Jerusalem", "Capernaum"),
            make_question("Who was Jesus' mother?", "Mary", "Martha", "Elizabeth", "Anna"),
            make_question("Who was told by an angel that Jesus would be born to Mary?", "Joseph", "Zacchaeus", "Nicodemus", "Cornelius"),
            make_question("Where was baby Jesus laid after His birth, according to Luke 2?", "In a manger", "In a palace throne", "In a fishing boat", "In the temple's inner room"),
            make_question("What did Jesus call His followers to be in the world in Matthew 5?", "The salt of the earth and the light of the world", "Kings of every nation", "Judges of the Roman army", "Builders of the ark"),
            make_question("In the parable of the Good Samaritan, who acted as a neighbor to the injured man?", "The Samaritan who showed mercy", "The robbers", "The priest who passed by", "The innkeeper who ignored him"),
            make_question("What did Jesus teach His followers to do for their enemies?", "Love them and pray for those who persecute them", "Take revenge immediately", "Never speak to them", "Ask rulers to punish every neighbor"),
            make_question("What did Jesus do at the Last Supper to teach His disciples about service in John 13?", "Washed their feet", "Built a wall", "Called down a flood", "Crowned Peter king"),
            make_question("What did Jesus use to feed a large crowd in the account of the five thousand?", "Five loaves and two fish", "Seven baskets of dates", "A lamb and ten grapes", "Twelve loaves and no fish"),
            make_question("According to Jesus, which commandment is greatest?", "Love the Lord your God with all your heart, soul, and mind", "Become richer than your neighbor", "Never forgive anyone", "Seek praise from everyone"),
        ],
    },
    {
        "name": "The Cross and Resurrection",
        "reference": "Luke 22-24; John 19-20",
        "story": (
            "Jesus is arrested, crucified, and buried. On the third day, His "
            "followers discover the tomb is empty and hear the announcement "
            "that He has risen."
        ),
        "lesson": (
            "Lesson: The resurrection is central to Christian hope. This story "
            "also invites reflection on sacrifice, forgiveness, courage, and "
            "hope in the middle of grief."
        ),
        "time_limit": 12,
        "pos": (650, 520),
        "questions": [
            make_question("Who betrayed Jesus to the authorities?", "Judas Iscariot", "John the Baptist", "Barnabas", "Thomas"),
            make_question("Where did Jesus pray before His arrest?", "Gethsemane", "Mount Ararat", "The Valley of Elah", "The garden of Eden"),
            make_question("Who denied knowing Jesus three times?", "Peter", "Andrew", "Philip", "Matthew"),
            make_question("Which Roman governor questioned Jesus?", "Pontius Pilate", "Julius Caesar", "Cyrus", "Darius"),
            make_question("What was placed on Jesus' head as a cruel mockery?", "A crown of thorns", "A crown of olive leaves", "A golden helmet", "A wreath of roses"),
            make_question("Where was Jesus crucified?", "Golgotha", "Bethlehem", "Mount Sinai", "Jericho"),
            make_question("Who asked Pilate for Jesus' body and placed it in a tomb?", "Joseph of Arimathea", "Simon Peter", "Zacchaeus", "The Samaritan woman"),
            make_question("When did Jesus' followers find the tomb empty?", "On the first day of the week, early in the morning", "At the start of the flood", "On the seventh day of creation", "During the Exodus"),
            make_question("Who was among the first witnesses to the risen Jesus in John's Gospel?", "Mary Magdalene", "Delilah", "Jezebel", "Pharaoh's daughter"),
            make_question("What message did the resurrection bring to Jesus' followers?", "That Jesus had risen from the dead", "That the disciples should return to Egypt", "That Jericho had been rebuilt", "That the flood had begun"),
        ],
    },
]
