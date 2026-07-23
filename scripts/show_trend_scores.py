from src.db.connection import SessionLocal
from src.db.models import (
    TrendScore,
    Topic
)


session = SessionLocal()

rows = (

    session.query(
        TrendScore,
        Topic
    )

    .join(
        Topic,
        TrendScore.topic_id == Topic.topic_id
    )

    .order_by(
        TrendScore.trend_score.desc()
    )

    .all()

)

print()

print("=" * 90)

for trend, topic in rows:

    print(

        f"{topic.canonical_name:35}"

        f"{trend.trend_score:8.2f}"

    )

session.close()