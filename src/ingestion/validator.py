from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import Tuple


class PostValidator:

    @staticmethod
    def validate_required_fields(
        post: Dict
    ) -> Tuple[bool, str]:

        required_fields = [

            "post_id",
            "account_id",
            "published_at",
            "scraped_at"
        ]

        for field in required_fields:

            if field not in post:

                return (
                    False,
                    f"Missing field: {field}"
                )

        return (
            True,
            ""
        )

    @staticmethod
    def validate_time_window(
        post: Dict
    ) -> Tuple[bool, str]:

        now = datetime.utcnow()

        published_at = datetime.fromisoformat(
            post["published_at"]
        )

        if (
            published_at
            >
            now + timedelta(hours=1)
        ):

            return (
                False,
                "Future post"
            )

        if (
            published_at
            <
            now - timedelta(days=7)
        ):

            return (
                False,
                "Older than 7 days"
            )

        return (
            True,
            ""
        )

    @staticmethod
    def validate_quality(
        post: Dict,
        config: Dict
    ) -> Tuple[bool, str]:

        min_followers = config[
            "quality"
        ][
            "min_followers"
        ]

        min_engagement = config[
            "quality"
        ][
            "min_engagement"
        ]

        if (
            post["followers_count"]
            <
            min_followers
        ):

            return (
                False,
                "Below follower threshold"
            )

        engagement = (

            post.get("likes", 0)
            +
            post.get("comments", 0)
            +
            post.get("views", 0)
        )

        if (
            engagement
            <
            min_engagement
        ):

            return (
                False,
                "Below engagement threshold"
            )

        return (
            True,
            ""
        )

    @classmethod
    def validate_post(
        cls,
        post: Dict,
        config: Dict
    ) -> Tuple[bool, str]:

        checks = [

            cls.validate_required_fields(
                post
            ),

            cls.validate_time_window(
                post
            ),

            cls.validate_quality(
                post,
                config
            )
        ]

        for is_valid, reason in checks:

            if not is_valid:

                return (
                    False,
                    reason
                )

        return (
            True,
            ""
        )