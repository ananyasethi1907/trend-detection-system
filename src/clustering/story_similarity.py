from src.clustering.embedder import (
    TopicEmbedder
)

from src.clustering.similarity import (
    TopicSimilarity
)

from src.clustering.story_normalizer import (
    StoryNormalizer
)

from src.nlp.entity_extractor import (
    EntityExtractor
)

from src.nlp.keyword_extractor import (
    KeywordExtractor
)


class StorySimilarity:

    def __init__(self):

        self.embedder = TopicEmbedder()

        self.normalizer = (
            StoryNormalizer()
        )

        self.entity_extractor = (
            EntityExtractor()
        )

        self.keyword_extractor = (
            KeywordExtractor()
        )

    def entity_overlap(
        self,
        story1,
        story2
    ):

        entities1 = {

            entity[0].lower()

            for entity in self.entity_extractor.extract(

                caption=story1,

                hashtags=[],

                language="en"

            )

        }

        entities2 = {

            entity[0].lower()

            for entity in self.entity_extractor.extract(

                caption=story2,

                hashtags=[],

                language="en"

            )

        }

        if not entities1 or not entities2:

            return 0.0

        intersection = len(

            entities1.intersection(
                entities2
            )

        )

        union = len(

            entities1.union(
                entities2
            )

        )

        return intersection / union

    def keyword_overlap(
        self,
        story1,
        story2
    ):

        keywords1 = {

            keyword.lower()

            for keyword in self.keyword_extractor.extract(
                story1
            )

        }

        keywords2 = {

            keyword.lower()

            for keyword in self.keyword_extractor.extract(
                story2
            )

        }

        if not keywords1 or not keywords2:

            return 0.0

        intersection = len(

            keywords1.intersection(
                keywords2
            )

        )

        union = len(

            keywords1.union(
                keywords2
            )

        )

        return intersection / union

    def calculate(
        self,
        story1,
        story2
    ):

        # Normalize stories first

        normalized_story1 = (
            self.normalizer.normalize(
                story1
            )
        )

        normalized_story2 = (
            self.normalizer.normalize(
                story2
            )
        )

        # Embedding similarity

        vector1 = self.embedder.embed(
            normalized_story1
        )

        vector2 = self.embedder.embed(
            normalized_story2
        )

        embedding_score = (

            TopicSimilarity.similarity(

                vector1,

                vector2

            )

        )

        # Entity overlap

        entity_score = (

            self.entity_overlap(

                normalized_story1,

                normalized_story2

            )

        )

        # Keyword overlap

        keyword_score = (

            self.keyword_overlap(

                normalized_story1,

                normalized_story2

            )

        )

        # Hybrid similarity score

        final_score = (

            0.60 * embedding_score +

            0.25 * entity_score +

            0.15 * keyword_score

        )

        return final_score