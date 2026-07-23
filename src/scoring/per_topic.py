from typing import Dict, List
import math


EPSILON = 1e-9


def aggregate_topic_metrics(
    scored_posts: List[Dict]
) -> Dict:

    total_engagement = sum(
        post["engagement"]
        for post in scored_posts
    )

    total_velocity = sum(
        post["velocity"]
        for post in scored_posts
    )

    avg_authority = (
        sum(
            post["authority"]
            for post in scored_posts
        )
        / len(scored_posts)
    )

    avg_freshness = (
        sum(
            post["freshness"]
            for post in scored_posts
        )
        / len(scored_posts)
    )

    post_count = len(
        scored_posts
    )

    unique_accounts = len(
        set(
            post["account_id"]
            for post in scored_posts
        )
    )

    return {

        "total_engagement": total_engagement,

        "total_velocity": total_velocity,

        "avg_authority": avg_authority,

        "avg_freshness": avg_freshness,

        "post_count": post_count,

        "unique_accounts": unique_accounts
    }


def calculate_momentum(
    total_velocity: float,
    previous_velocity: float
) -> float:

    if previous_velocity <= 0:

        return 1.0

    return (

        total_velocity
        - previous_velocity

    ) / max(
        previous_velocity,
        EPSILON
    )


def calculate_growth_rate(
    current_post_count: int,
    previous_post_count: int
) -> float:

    return (

        current_post_count
        - previous_post_count

    ) / max(
        previous_post_count,
        1
    )


def calculate_diversity(
    scored_posts: List[Dict]
) -> float:

    post_count = len(
        scored_posts
    )

    account_counts = {}

    for post in scored_posts:

        account_id = post[
            "account_id"
        ]

        account_counts[
            account_id
        ] = (

            account_counts.get(
                account_id,
                0
            )
            + 1
        )

    hhi = 0

    for count in account_counts.values():

        share = count / post_count

        hhi += share ** 2

    diversity_score = 1 - hhi

    return diversity_score


def calculate_raw_topic_score(
    topic_metrics: Dict,
    config: Dict
) -> float:

    weights = config[
        "component_weights"
    ]

    # Compress huge values so they don't dominate
    engagement = math.log1p(
        topic_metrics[
            "total_engagement"
        ]
    )

    velocity = math.log1p(
        topic_metrics[
            "total_velocity"
        ]
    )

    authority = math.log1p(
        topic_metrics[
            "avg_authority"
        ]
    )

    raw_score = 0

    raw_score += (
        engagement
        * weights["engagement"]
    )

    raw_score += (
        velocity
        * weights["velocity"]
    )

    raw_score += (
        topic_metrics[
            "momentum"
        ]
        * weights["momentum"]
    )

    raw_score += (
        topic_metrics[
            "avg_freshness"
        ]
        * weights["freshness"]
    )

    raw_score += (
        authority
        * weights["authority"]
    )

    raw_score += (
        topic_metrics[
            "diversity_score"
        ]
        * weights["diversity"]
    )

    raw_score += (
        topic_metrics[
            "growth_rate"
        ]
        * weights["growth_rate"]
    )

    raw_score += (
        topic_metrics[
            "post_count"
        ]
        * weights["topic_volume"]
    )

    # Optional confidence boost for topics
    # discussed by multiple accounts
    if topic_metrics[
        "unique_accounts"
    ] > 1:

        raw_score *= 1.15

    return raw_score