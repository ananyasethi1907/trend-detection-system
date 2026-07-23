import re


class TopicQuality:

    SPAM_PATTERNS = [

        "your month",
        "birth month",
        "comment below",
        "tag your",
        "tag a friend",
        "follow for",
        "like and share",
        "guess",
        "choose one",
        "which one",
        "which guy",
        "which girl",
        "your boyfriend",
        "your girlfriend",
        "your type",
        "rate this",
        "viral template"
    ]

    EVENT_WORDS = {

        "wins",
        "win",
        "beats",
        "beat",
        "launch",
        "launched",
        "release",
        "released",
        "marriage",
        "married",
        "wedding",
        "dies",
        "death",
        "announces",
        "announcement",
        "joins",
        "debut",
        "championship",
        "world cup",
        "election",
        "earthquake",
        "flood"
    }

    @staticmethod
    def score(
        candidate,
        entities
    ):

        score = 0

        candidate_lower = candidate.lower()

        # -------------------
        # Spam detection
        # -------------------

        for pattern in TopicQuality.SPAM_PATTERNS:

            if pattern in candidate_lower:

                return -100

        # -------------------
        # Length
        # -------------------

        words = candidate.split()

        if 2 <= len(words) <= 6:

            score += 15

        elif len(words) == 1:

            score += 5

        else:

            score -= 10

        # -------------------
        # Entity bonus
        # -------------------

        for entity in entities:

            if entity[0].lower() in candidate_lower:

                score += 25

        # -------------------
        # Event words
        # -------------------

        for word in TopicQuality.EVENT_WORDS:

            if word in candidate_lower:

                score += 20

        # -------------------
        # Proper capitalization
        # -------------------

        if re.search(

            r"[A-Z]",

            candidate

        ):

            score += 5

        return score