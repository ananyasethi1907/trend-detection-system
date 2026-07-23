class GeoAggregator:

    @staticmethod
    def aggregate(
        posts
    ):

        counts = {}

        for post in posts:

            country = (
                post.country_code
            )

            counts[country] = (
                counts.get(
                    country,
                    0
                ) + 1
            )

        return counts