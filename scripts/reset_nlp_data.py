from src.db.connection import SessionLocal
from src.db.models import (
    Topic,
    PostTopicMap,
    TrendScore
)

session = SessionLocal()

try:

    session.query(
        PostTopicMap
    ).delete()

    session.query(
        Topic
    ).delete()

    session.query(
        TrendScore
    ).delete()

    session.commit()

    print(
        "NLP data cleared"
    )

finally:

    session.close()