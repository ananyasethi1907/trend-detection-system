from typing import List, Dict


EPSILON = 1e-9


def normalize_scores(
    topic_scores: List[Dict]
) -> List[Dict]:

    if not topic_scores:
        return topic_scores

    raw_scores = [
        topic["raw_score"]
        for topic in topic_scores
    ]

    window_min = min(raw_scores)

    window_max = max(raw_scores)

    for topic in topic_scores:

        topic["trend_score"] = (
            100
            * (
                topic["raw_score"]
                - window_min
            )
            /
            (
                window_max
                - window_min
                + EPSILON
            )
        )

    return topic_scores