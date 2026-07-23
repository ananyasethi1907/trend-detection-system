from src.nlp.topic_ranker import TopicRanker


class CanonicalSelector:

    @staticmethod
    def select(
        candidates,
        entities
    ):

        if not candidates:

            return None

        ranked = []

        for candidate in candidates:

            score = TopicRanker.score(

                candidate,

                entities

            )

            ranked.append(

                (

                    score,

                    candidate

                )

            )

        ranked.sort(

            reverse=True

        )

        return ranked[0][1]