from collections import defaultdict
from typing import Dict, List

from src.scoring.per_post import (
    calculate_post_score
)

from src.scoring.per_topic import (
    aggregate_topic_metrics,
    calculate_momentum,
    calculate_growth_rate,
    calculate_diversity,
    calculate_raw_topic_score
)

from src.scoring.normalizer import (
    normalize_scores
)

from src.scoring.state_classifier import (
    classify_state
)


class ScoringEngine:

    def __init__(
        self,
        config: Dict,
        db=None,
        redis=None
    ):

        self.config = config
        self.db = db
        self.redis = redis

    def score_post(
        self,
        post: Dict,
        window: str
    ) -> Dict:

        return calculate_post_score(
            post=post,
            age_hours=post["age_hours"],
            window=window,
            config=self.config
        )

    def score_topic(
        self,
        topic_name: str,
        posts: List[Dict],
        window: str,
        previous_cycle_data: Dict = None
    ) -> Dict:

        metrics = aggregate_topic_metrics(
            posts
        )

        previous_velocity = 0
        previous_post_count = 0

        if previous_cycle_data:

            previous_velocity = (
                previous_cycle_data.get(
                    "total_velocity",
                    0
                )
            )

            previous_post_count = (
                previous_cycle_data.get(
                    "post_count",
                    0
                )
            )

        metrics["momentum"] = (
            calculate_momentum(
                metrics[
                    "total_velocity"
                ],
                previous_velocity
            )
        )

        metrics["growth_rate"] = (
            calculate_growth_rate(
                metrics["post_count"],
                previous_post_count
            )
        )

        metrics["diversity_score"] = (
            calculate_diversity(
                posts
            )
        )

        raw_score = (
            calculate_raw_topic_score(
                metrics,
                self.config
            )
        )

        metrics["topic"] = topic_name

        metrics["raw_score"] = raw_score

        return metrics

    def score_window(
        self,
        posts: List[Dict],
        window: str,
        cycle_id: str
    ) -> List[Dict]:

        scored_posts = []

        for post in posts:

            post_metrics = (
                self.score_post(
                    post,
                    window
                )
            )

            merged_post = {
                **post,
                **post_metrics
            }

            scored_posts.append(
                merged_post
            )

        topic_groups = defaultdict(
            list
        )

        for post in scored_posts:

            topic_groups[
                post["topic"]
            ].append(post)

        topic_scores = []

        for topic_name, topic_posts in (
            topic_groups.items()
        ):

            min_posts = (
                self.config
                .get(
                    "quality",
                    {}
                )
                .get(
                    "min_posts_for_topic",
                    1
                )
            )

            if len(topic_posts) < min_posts:

                continue

            topic_result = (
                self.score_topic(
                    topic_name,
                    topic_posts,
                    window
                )
            )

            topic_scores.append(
                topic_result
            )

        topic_scores = (
            normalize_scores(
                topic_scores
            )
        )

        for topic in topic_scores:

            topic["trend_status"] = (
                classify_state(
                    metrics=topic,
                    previous_metrics={},
                    config=self.config
                )
            )

            topic["window"] = window

            topic["cycle_id"] = cycle_id

        topic_scores.sort(
            key=lambda x: x[
                "trend_score"
            ],
            reverse=True
        )

        return topic_scores