import uuid

from src.db.connection import SessionLocal
from src.db.models import (
    Topic,
    PostTopicMap
)


class TopicAssigner:

    @staticmethod
    def get_or_create_topic(
        topic_name: str,
        category: str = "other"
    ):

        session = SessionLocal()

        try:

            topic = (
                session.query(Topic)
                .filter(
                    Topic.canonical_name
                    == topic_name
                )
                .first()
            )

            if topic:
                return topic.topic_id

            topic_id = str(
                uuid.uuid4()
            )

            topic = Topic(
                topic_id=topic_id,
                canonical_name=topic_name,
                category=category
            )

            session.add(topic)

            session.commit()

            return topic_id

        finally:

            session.close()

    @staticmethod
    def assign_post_to_topic(
        post_id: str,
        topic_name: str,
        entity_type: str,
        confidence: float
    ):

        session = SessionLocal()

        try:

            topic_id = (
                TopicAssigner
                .get_or_create_topic(
                    topic_name
                )
            )

            existing = (
                session.query(
                    PostTopicMap
                )
                .filter(
                    PostTopicMap.post_id
                    == post_id,
                    PostTopicMap.topic_id
                    == topic_id
                )
                .first()
            )

            if existing:
                return

            mapping = PostTopicMap(
                post_id=post_id,
                topic_id=topic_id,
                entity_type=entity_type,
                entity_confidence=confidence
            )

            session.add(mapping)

            session.commit()

        finally:

            session.close()