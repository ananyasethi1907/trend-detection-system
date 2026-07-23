from src.scoring.repository import (
    TrendScoreRepository
)


class TrendHandler:

    @staticmethod
    def get_trends(
        window: str,
        limit: int
    ):

        return (
            TrendScoreRepository
            .get_top_trends(
                window=window,
                limit=limit
            )
        )