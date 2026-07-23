from typing import Dict
import math


def calculate_engagement(
    post: Dict,
    config: Dict
) -> float:

    engagement = 0.0

    for metric, weight in config[
        "engagement_factors"
    ].items():

        engagement += (
            weight *
            post.get(metric, 0)
        )

    return engagement


def calculate_authority(
    post: Dict,
    config: Dict
) -> float:

    verified_bonus = config[
        "authority_factors"
    ]["verified_bonus"]

    followers_weight = config[
        "authority_factors"
    ]["followers_weight"]

    authority = (
        (1 if post["is_verified"] else 0)
        * verified_bonus
    )

    authority += (
        post["followers_count"]
        * followers_weight
    )

    return authority


def calculate_velocity(
    engagement: float,
    age_hours: float,
    config: Dict
) -> float:

    min_age = config[
        "velocity"
    ]["min_age_hours"]

    age_hours = max(
        age_hours,
        min_age
    )

    return engagement / age_hours


def calculate_freshness(
    age_hours: float,
    window: str,
    config: Dict
) -> float:

    half_life = config[
        "freshness"
    ]["half_life_hours"][window]

    freshness = math.pow(
        2,
        (-age_hours / half_life)
    )

    return freshness


def calculate_post_score(
    post: Dict,
    age_hours: float,
    window: str,
    config: Dict
) -> Dict:

    engagement = calculate_engagement(
        post,
        config
    )

    authority = calculate_authority(
        post,
        config
    )

    velocity = calculate_velocity(
        engagement,
        age_hours,
        config
    )

    freshness = calculate_freshness(
        age_hours,
        window,
        config
    )

    weights = config[
        "component_weights"
    ]

    post_score = (
        engagement
        * weights["engagement"]
    )

    post_score += (
        velocity
        * weights["velocity"]
    )

    post_score += (
        authority
        * weights["authority"]
    )

    post_score += (
        freshness
        * weights["freshness"]
    )

    if post.get(
        "manipulation_flag",
        False
    ):
        post_score *= config[
            "fraud"
        ]["penalty"]

    return {
        "engagement": engagement,
        "authority": authority,
        "velocity": velocity,
        "freshness": freshness,
        "post_score": post_score
    }