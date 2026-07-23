from src.clustering.story_similarity import (
    StorySimilarity
)


class StoryClusterer:

    def __init__(
        self,
        threshold=0.65
    ):

        self.threshold = threshold
        self.similarity = StorySimilarity()

    def cluster(
        self,
        topics
    ):

        clusters = []

        for topic in topics:

            best_cluster = None
            best_score = 0

            for cluster in clusters:

                scores = []

                for existing_topic in cluster["topics"]:

                    score = self.similarity.calculate(
                        topic,
                        existing_topic
                    )

                    scores.append(score)

                average_score = sum(scores) / len(scores)

                if average_score > best_score:

                    best_score = average_score
                    best_cluster = cluster

            if (
                best_cluster is not None
                and
                best_score >= self.threshold
            ):

                best_cluster["topics"].append(
                    topic
                )

            else:

                clusters.append(

                    {
                        "canonical": topic,
                        "topics": [topic]
                    }

                )

        return clusters