from src.db.connection import SessionLocal
from src.db.models import (
    Post,
    Topic,
    PostTopicMap
)


class TopicPostService:

    @staticmethod
    def get_posts(topic_id: str):

        session = SessionLocal()

        try:

            posts = (

                session.query(Post)

                .join(

                    PostTopicMap,

                    Post.post_id == PostTopicMap.post_id

                )

                .filter(

                    PostTopicMap.topic_id == topic_id

                )

                .all()

            )

            return posts

        finally:

            session.close()

    @staticmethod
    def get_all_topics():

        session = SessionLocal()

        try:

            return (

                session.query(Topic)

                .all()

            )

        finally:

            session.close()