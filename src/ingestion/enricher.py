from typing import Dict

from langdetect import detect


class PostEnricher:

    @staticmethod
    def normalize_metrics(
        post: Dict
    ) -> Dict:

        if post.get("shares") is None:
            post["shares"] = 0

        if post.get("saves") is None:
            post["saves"] = 0

        return post

    @staticmethod
    def detect_language(
        post: Dict
    ) -> Dict:

        if post.get("language"):

            return post

        caption = post.get(
            "caption",
            ""
        )

        if not caption:

            post["language"] = None

            return post

        try:

            post["language"] = (
                detect(caption)
            )

        except Exception:

            post["language"] = None

        return post

    @staticmethod
    def infer_geo(
        post: Dict,
        hashtag_lookup: Dict = None,
        account_history: Dict = None
    ) -> Dict:

        geo = post.get("geo")

        if (
            geo
            and
            geo.get(
                "geotag_confidence",
                0
            )
            >= 0.95
        ):

            return post

        hashtags = post.get(
            "hashtags",
            []
        )

        if hashtag_lookup:

            for hashtag in hashtags:

                location = (
                    hashtag_lookup.get(
                        hashtag.lower()
                    )
                )

                if location:

                    post["geo"] = location

                    return post

        if account_history:

            account_id = post.get(
                "account_id"
            )

            location = (
                account_history.get(
                    account_id
                )
            )

            if location:

                post["geo"] = location

                return post

        if "geo" not in post:

            post["geo"] = {

                "country_code": None,

                "region": None,

                "city": None,

                "geotag_confidence": None
            }

        return post

    @classmethod
    def enrich(
        cls,
        post: Dict,
        hashtag_lookup: Dict = None,
        account_history: Dict = None
    ) -> Dict:

        post = cls.normalize_metrics(
            post
        )

        post = cls.detect_language(
            post
        )

        post = cls.infer_geo(
            post,
            hashtag_lookup,
            account_history
        )

        return post