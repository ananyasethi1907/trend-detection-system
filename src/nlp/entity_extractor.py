from typing import List
from typing import Tuple

import re
import spacy


STOP_WORDS = {

    "today",
    "week",
    "month",
    "year",
    "years",
    "latest",
    "watch",
    "instagram",
    "youtube",
    "photo",
    "photos",
    "image",
    "images",
    "video",
    "summer",
    "winter",
    "spring",
    "autumn",
    "episode",
    "season",
    "story",
    "stories",
    "news"
}


BLACKLIST = {

    "Getty Images",
    "BACKGRID",
    "FilmMagic",
    "Shutterstock",
    "GC Images",
    "Page Six",
    "Instagram",
    "YouTube",
    "Youtube"
}


VALID_ENTITY_TYPES = {

    "PERSON",
    "ORG",
    "EVENT",
    "PRODUCT",
    "WORK_OF_ART"
}


GENERIC_SLANG_WORDS = {

    "mindset",
    "vibes",
    "vibe",
    "energy",
    "era",
    "aesthetic",
    "core",
    "fit",
    "drip",
    "rizz",
    "baddies",
    "baddie"

}


class EntityExtractor:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract_entities(
        self,
        caption: str
    ) -> List[
        Tuple[
            str,
            str,
            str,
            float
        ]
    ]:

        if not caption:

            return []

        doc = self.nlp(
            caption
        )

        results = []

        seen = set()

        for entity in doc.ents:

            text = (
                entity.text
                .strip()
            )

            # only keep useful entity types
            if (
                entity.label_
                not in VALID_ENTITY_TYPES
            ):
                continue

            # blacklist
            if text in BLACKLIST:
                continue

            # remove handles
            if "@" in text:
                continue

            # remove image credits
            if "/" in text:
                continue

            # remove broken strings
            if '"' in text:
                continue

            # remove hashtags
            if "#" in text:
                continue

            # remove urls
            if (
                "http" in text.lower()
                or
                "www." in text.lower()
            ):
                continue

            # remove emoji-heavy entities
            if any(
                ord(char) > 10000
                for char in text
            ):
                continue

            # Real named entities (orgs, events, works of art) are almost
            # always written with at least one capital letter in the
            # original caption -- they're proper nouns. spaCy's small model
            # frequently mislabels casual all-lowercase slang/phrases (e.g.
            # "genz mindset") as WORK_OF_ART/ORG/EVENT on informal caption
            # text. This is a general structural filter against that whole
            # failure mode, not a denylist of specific bad phrases.
            #
            # Scoped to skip PERSON: slang-mislabeling almost never produces
            # a PERSON tag, and real people's names are the category most
            # often typed in stylized lowercase by users (e.g. "karan
            # kundrra"). Applying this check to PERSON would reject those
            # legitimate names along with the slang.
            is_lowercase = not any(
                char.isupper()
                for char in text
            )

            if is_lowercase:

                if entity.label_ != "PERSON":
                    continue

                words = text.lower().split()

                if len(words) > 3:
                    continue

                if any(
                    word in GENERIC_SLANG_WORDS
                    for word in words
                ):
                    continue

            # remove stop words
            if (
                text.lower()
                in STOP_WORDS
            ):
                continue

            # too short
            if len(text) < 3:
                continue

            # remove single short words
            if (
                len(text.split()) == 1
                and
                len(text) < 5
            ):
                continue

            # remove entities with too many digits
            digit_count = sum(
                c.isdigit()
                for c in text
            )

            if digit_count > 2:
                continue

            # deduplicate
            normalized = (
                text.lower()
            )

            if (
                normalized
                in seen
            ):
                continue

            seen.add(
                normalized
            )

            results.append(

                (
                    text,
                    entity.label_,
                    "ner",
                    1.0
                )
            )

        return results

    def extract_hashtags(
        self,
        hashtags: List[str]
    ):

        results = []

        seen = set()

        for hashtag in hashtags:

            cleaned = (
                hashtag
                .lower()
                .replace(
                    "#",
                    ""
                )
                .strip()
            )

            if len(cleaned) < 3:
                continue

            if (
                cleaned
                in STOP_WORDS
            ):
                continue

            if (
                cleaned
                in seen
            ):
                continue

            seen.add(
                cleaned
            )

            results.append(

                (
                    cleaned,
                    "hashtag",
                    "hashtag",
                    0.9
                )
            )

        return results

    def extract(
        self,
        caption: str,
        hashtags: List[str],
        language: str
    ):

        entities = (
            self.extract_entities(
                caption
            )
        )

        hashtag_entities = (
            self.extract_hashtags(
                hashtags
            )
        )

        return (
            entities
            +
            hashtag_entities
        )