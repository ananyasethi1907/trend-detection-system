from src.db.connection import (
    SessionLocal
)

from src.db.models import (
    TrendScore
)


class TrendScoreStorage:

    @staticmethod
    def save_score(
        topic_id: str,
        window: str,
        cycle_id: str,
        trend_score: float,
        trend_status: str,
        growth_rate: float,
        momentum_score: float,
        velocity: float
    ):

        session = SessionLocal()

        try:

            score = TrendScore(

                topic_id=topic_id,

                window=window,

                cycle_id=cycle_id,

                trend_score=trend_score,

                trend_status=
                trend_status,

                growth_rate=
                growth_rate,

                momentum_score=
                momentum_score,

                velocity=
                velocity
            )

            session.add(score)

            session.commit()

        finally:

            session.close()