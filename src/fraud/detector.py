class FraudDetector:

    @staticmethod
    def like_view_ratio(
        likes: int,
        views: int,
        threshold: float = 0.9
    ):

        ratio = (
            likes /
            (views + 1)
        )

        return ratio > threshold

    @staticmethod
    def engagement_anomaly(
        engagement: int,
        mean: float,
        std: float,
        sigma: float = 4.0
    ):

        return (
            engagement >
            mean +
            sigma * std
        )