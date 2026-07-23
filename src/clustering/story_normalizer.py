import re

import spacy


class StoryNormalizer:

    def __init__(self):

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

        self.replacements = {

            "marries": "marry",
            "married": "marry",
            "marriage": "marry",
            "wedding": "marry",

            "beats": "vs",
            "beat": "vs",
            "defeats": "vs",
            "defeat": "vs",
            "wins": "vs",
            "won": "vs",

            "launches": "launch",
            "launched": "launch",
            "launching": "launch",

            "releases": "release",
            "released": "release",
            "releasing": "release",

            "announces": "announce",
            "announced": "announce",

            "confirms": "confirm",
            "confirmed": "confirm"
        }

    def normalize(
        self,
        story: str
    ):

        story = story.lower()

        story = re.sub(

            r"[^\w\s]",

            "",

            story

        )

        words = []

        for word in story.split():

            words.append(

                self.replacements.get(

                    word,

                    word

                )

            )

        story = " ".join(
            words
        )

        doc = self.nlp(
            story
        )

        normalized = []

        for token in doc:

            normalized.append(
                token.lemma_
            )

        return " ".join(
            normalized
        )