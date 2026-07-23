import re


CAMEL_MASH_PATTERN = re.compile(r"[a-z][A-Z]")


class TopicValidator:

    BANNED_PHRASES = {

        "full video",
        "link in bio",
        "comment below",
        "follow",
        "share",
        "subscribe",
        "viral",
        "trending",
        "reel",
        "explore",
        "aaj kya hua",
        "dating relationship"

    }

    BANNED_SINGLE_WORDS = {

        "video",
        "videos",
        "post",
        "posts",
        "page",
        "tweet",
        "tweets",
        "photo",
        "photos",
        "picture",
        "pictures"

    }

    @staticmethod
    def is_valid(topic: str):

        if topic is None:
            return False

        topic = " ".join(topic.split()).strip()

        if len(topic) < 3:
            return False

        if len(topic.split()) > 8:
            return False

        lower = topic.lower()

        ####################################################
        # URLs / Hashtags
        ####################################################

        if "#" in topic:
            return False

        if "http" in lower:
            return False

        ####################################################
        # Emojis
        ####################################################

        if re.search(
            r"[\U00010000-\U0010ffff]",
            topic
        ):
            return False

        ####################################################
        # Malformed topics
        ####################################################

        if topic.startswith(("[", "(", "{")):
            return False

        if topic.endswith(("]", ")", "}")):
            return False

        ####################################################
        # Stray quotes / slashes anywhere in the string
        #
        # Legitimate topics essentially never contain a literal double
        # quote or a slash -- these show up when a candidate is actually
        # a raw fragment of caption/credit text (e.g. a quote that was
        # never closed, or an image-credit-style "A/B" mashup) rather
        # than a clean topic phrase. Catches cases like:
        #   Peacock/ "Love Island USA
        #   Heated Rivalry" star Francois Arnaud
        ####################################################

        if '"' in topic:
            return False

        if any(
            char in topic
            for char in ('\u201c', '\u201d')
        ):
            return False

        if "/" in topic:
            return False

        ####################################################
        # CamelCase word mashups
        #
        # A lowercase letter immediately followed by an uppercase letter
        # within a single token (no space) means two or more words got
        # concatenated without a space somewhere upstream -- almost
        # always a broken/malformed candidate rather than a real topic.
        # Catches cases like:
        #   TheEstablished
        #   NakedAndAfraid
        ####################################################

        for word in topic.split():

            if CAMEL_MASH_PATTERN.search(word):
                return False

        ####################################################
        # Remove leading articles
        ####################################################

        if lower.startswith("the "):
            return False

        ####################################################
        # Too little text
        ####################################################

        letters = sum(
            c.isalpha()
            for c in topic
        )

        if letters < 3:
            return False

        ####################################################
        # Engagement bait
        ####################################################

        for phrase in TopicValidator.BANNED_PHRASES:

            if phrase in lower:
                return False

        ####################################################
        # Single generic word
        ####################################################

        if lower in TopicValidator.BANNED_SINGLE_WORDS:
            return False

        ####################################################
        # Only generic words
        ####################################################

        words = re.findall(
            r"[A-Za-z']+",
            lower
        )

        if words:

            generic = sum(

                1

                for word in words

                if word in TopicValidator.BANNED_SINGLE_WORDS

            )

            if generic == len(words):
                return False

        ####################################################
        # Mostly punctuation
        ####################################################

        punctuation = sum(

            1

            for c in topic

            if not c.isalnum() and not c.isspace()

        )

        if punctuation > len(topic) * 0.4:
            return False

        ####################################################
        # Starts with lowercase article/pronoun
        ####################################################

        bad_start = {

            "the",
            "this",
            "that",
            "these",
            "those",
            "my",
            "your",
            "our",
            "their",
            "his",
            "her",
            "its"

        }

        first = lower.split()[0]

        if first in bad_start:
            return False

        ####################################################
        # Looks good
        ####################################################

        return True