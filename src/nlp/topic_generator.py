from src.nlp.candidate_generator import CandidateGenerator
from src.nlp.canonical_selector import CanonicalSelector
from src.nlp.topic_validator import TopicValidator


class TopicGenerator:

    @staticmethod
    def generate(

        caption,

        entities,

        keywords

    ):

        candidates = CandidateGenerator.generate(

            entities,

            keywords

        )

        if not candidates:

            return None

        topic = CanonicalSelector.select(

            candidates,

            entities,

            caption

        )

        if not TopicValidator.is_valid(

            topic

        ):

            return None

        return topic