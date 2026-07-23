from typing import Dict


REQUIRED_TOP_LEVEL_KEYS = [
    "engagement_factors",
    "authority_factors",
    "component_weights",
    "freshness",
    "velocity"
]


def validate_schema(config: Dict) -> bool:
    """
    Validate config structure.
    """

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in config:
            raise ValueError(
                f"Missing required config key: {key}"
            )

    return True