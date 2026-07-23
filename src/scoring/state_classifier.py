def classify_state(
    metrics,
    previous_metrics,
    config
):

    thresholds = config[
        "state_thresholds"
    ]

    trend_score = metrics[
        "trend_score"
    ]

    velocity = metrics[
        "total_velocity"
    ]

    growth_rate = metrics[
        "growth_rate"
    ]

    post_count = metrics[
        "post_count"
    ]

    momentum = metrics[
        "momentum"
    ]

    previous_score = previous_metrics.get(
        "trend_score",
        0
    )

    score_delta = (
        trend_score
        - previous_score
    )

    viral = (

        trend_score >
        thresholds[
            "viral_score_threshold"
        ]

        and

        velocity >
        thresholds[
            "viral_velocity_threshold"
        ]
    )

    emerging = (

        post_count <
        thresholds[
            "emerging_max_posts"
        ]

        and

        growth_rate >
        thresholds[
            "emerging_min_growth_rate"
        ]
    )

    rising = (

        score_delta >
        thresholds[
            "rising_score_delta"
        ]

        and

        momentum > 0
    )

    stable = (

        abs(score_delta)
        <=
        thresholds[
            "stable_band"
        ]
    )

    cooling = (

        score_delta
        <
        -thresholds[
            "rising_score_delta"
        ]

        and

        trend_score
        >
        thresholds[
            "viral_score_threshold"
        ] * 0.5
    )

    declining = (

        score_delta
        <
        -thresholds[
            "rising_score_delta"
        ]

        and

        trend_score
        <=
        thresholds[
            "viral_score_threshold"
        ] * 0.5
    )

    if viral:
        return "viral"

    if emerging:
        return "emerging"

    if rising:
        return "rising"

    if stable:
        return "stable"

    if cooling:
        return "cooling"

    if declining:
        return "declining"

    return "stable"