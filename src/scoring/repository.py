from src.db.connection import (
    SessionLocal
)

from src.db.models import (
    TrendScore
)


class TrendScoreRepository:

    @staticmethod
    def get_top_trends(
        window: str,
        limit: int = 20
    ):

        session = SessionLocal()

        try:

            return (
                session.query(
                    TrendScore
                )
                .filter(
                    TrendScore.window
                    == window
                )
                .order_by(
                    TrendScore.trend_score.desc()
                )
                .limit(limit)
                .all()
            )

        finally:

            session.close()