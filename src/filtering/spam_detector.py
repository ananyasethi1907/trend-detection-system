import re


class SpamDetector:

    LOW_VALUE_PATTERNS = [

        r"your\s+birth\s+month",
        r"your\s+boyfriend",
        r"your\s+girlfriend",
        r"which\s+one\s+are\s+you",
        r"which\s+guy",
        r"which\s+girl",
        r"choose\s+one",
        r"pick\s+one",
        r"comment\s+below",
        r"comment\s+your",
        r"tag\s+your",
        r"tag\s+a\s+friend",
        r"share\s+with",
        r"rate\s+this",
        r"guess\s+your",
        r"what\s+would\s+you",
        r"what\s+type",
        r"what\s+kind",
        r"how\s+many",
        r"relatable",
        r"only\s+real",
        r"100%\s+true",
        r"follow\s+for\s+more",
        r"dm\s+us",
        r"link\s+in\s+bio"
    ]

    LOW_VALUE_WORDS = {

        "baddie",
        "shawty",
        "boyfriend",
        "girlfriend",
        "month",
        "comment",
        "follow",
        "viral",
        "explore",
        "relatable",
        "guess",
        "choose",
        "pick",
        "tag",
        "rate"
    }

    @staticmethod
    def is_spam(
        caption: str
    ) -> bool:

        if not caption:
            return True

        text = caption.lower()

        # Pattern matching

        for pattern in SpamDetector.LOW_VALUE_PATTERNS:

            if re.search(pattern, text):

                return True

        # Too many emojis

        emoji_count = sum(

            ord(char) > 10000

            for char in caption

        )

        if emoji_count >= 8:

            return True

        # Too many repeated words

        words = re.findall(

            r"[a-zA-Z]+",

            text

        )

        if not words:

            return True

        unique_ratio = len(

            set(words)

        ) / len(words)

        if unique_ratio < 0.45:

            return True

        # Engagement bait

        spam_score = sum(

            word in SpamDetector.LOW_VALUE_WORDS

            for word in words

        )

        if spam_score >= 4:

            return True

        return False