class StoryClassifier:

    @staticmethod
    def classify(
        caption: str,
        keywords: list
    ):

        text = (
            caption.lower()
        )

        # Entertainment

        if any(
            word in text
            for word in [
                "teaser",
                "trailer",
                "starring",
                "movie",
                "film",
                "album",
                "song",
                "released",
                "release"
            ]
        ):

            return "entertainment"

        # Celebrity

        if any(
            word in text
            for word in [
                "married",
                "marriage",
                "engaged",
                "dating",
                "relationship",
                "divorce",
                "wedding"
            ]
        ):

            return "celebrity"

        # Sports

        if any(
            word in text
            for word in [
                "world cup",
                "cricket",
                "football",
                "match",
                "wins",
                "won",
                "team",
                "league",
                "ipl"
            ]
        ):

            return "sports"

        # Podcast

        if any(
            word in text
            for word in [
                "podcast",
                "episode",
                "conversation",
                "watch",
                "yt"
            ]
        ):

            return "podcast"

        # Marketing

        if any(
            word in text
            for word in [
                "campaign",
                "brand",
                "marketing",
                "advertising"
            ]
        ):

            return "marketing"

        # Politics

        if any(
            word in text
            for word in [
                "commission",
                "government",
                "minister",
                "court",
                "police"
            ]
        ):

            return "politics"

        return "general"