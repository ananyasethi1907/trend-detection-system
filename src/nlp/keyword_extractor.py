import re
import spacy


STOP_CHUNKS = {

    "link in bio",
    "our bio",
    "the link",
    "this video",
    "the video",
    "latest post",
    "instagram",
    "page six",

    "everyone",
    "someone",
    "everything",
    "anything",

    "today",
    "tomorrow",
    "yesterday",

    "this",
    "that",
    "these",
    "those"
}


BAD_START_WORDS = {

    "which",
    "what",
    "who",
    "where",
    "when",
    "why",
    "how",

    "your",
    "my",
    "our",
    "their",
    "his",
    "her",

    "comment",
    "follow",
    "share",
    "tag",
    "like"
}


GENERIC_WORDS = {

    "month",
    "boyfriend",
    "girlfriend",
    "video",
    "post",
    "posts",
    "photo",
    "photos",
    "picture",
    "pictures",
    "comment",
    "comments",
    "bio",
    "caption",
    "people",
    "person",
    "makers",
    "everyone",
    "everything"
}


class KeywordExtractor:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

    def extract(
        self,
        caption
    ):

        if not caption:

            return []

        doc = self.nlp(
            caption
        )

        keywords = []

        seen = set()

        ##############################################

        # NOUN CHUNKS

        ##############################################

        for chunk in doc.noun_chunks:

            phrase = chunk.text.strip()

            phrase = re.sub(

                r"\s+",

                " ",

                phrase

            )

            lower = phrase.lower()

            if len(phrase) < 4:

                continue

            if lower in STOP_CHUNKS:

                continue

            words = lower.split()

            # Bad first word

            if words[0] in BAD_START_WORDS:

                continue

            # Mostly generic words

            generic = sum(

                1

                for word in words

                if word in GENERIC_WORDS

            )

            if generic >= len(words):

                continue

            # Must contain NOUN/PROPN

            if not any(

                token.pos_ in (

                    "NOUN",

                    "PROPN"

                )

                for token in chunk

            ):

                continue

            if lower in seen:

                continue

            seen.add(

                lower

            )

            keywords.append(

                phrase

            )

        ##############################################

        # NAMED ENTITIES

        ##############################################

        VALID_ENTITY_TYPES = {

            "PERSON",
            "ORG",
            "GPE",
            "LOC",
            "EVENT",
            "WORK_OF_ART",
            "PRODUCT"

        }

        for ent in doc.ents:

            # Ignore unwanted entity types
            if ent.label_ not in VALID_ENTITY_TYPES:

                continue

            text = ent.text.strip()

            # Remove leading articles
            text = re.sub(

                r"^(the|a|an)\s+",

                "",

                text,

                flags=re.IGNORECASE

            )

            lower = text.lower()

            if len(text) < 3:

                continue

            if lower in GENERIC_WORDS:

                continue

            if lower in seen:

                continue

            seen.add(

                lower

            )

            keywords.append(

                text

            )

        return keywords