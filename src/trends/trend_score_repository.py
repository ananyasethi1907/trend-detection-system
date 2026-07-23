from src.db.connection import SessionLocal
from src.db.models import TrendScore

from datetime import datetime


class TrendScoreRepository:

    @staticmethod
    def save(

        topic_id: str,

        score: dict,

        window: str = "24h"

    ):

        session = SessionLocal()

        try:

            trend = TrendScore(

                topic_id=topic_id,

                window=window,

                cycle_id=datetime.utcnow().strftime(
                    "%Y%m%d%H"
                ),

                trend_score=score["trend_score"],

                confidence_score=1.0,

                trend_status="ACTIVE",

                score_delta=0,

                growth_rate=0,

                momentum_score=0,

                velocity=score["velocity"]

            )

            session.add(trend)

            session.commit()

        finally:

            session.close()