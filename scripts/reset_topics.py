from src.db.connection import SessionLocal
from src.db.models import Topic
from src.db.models import PostTopicMap


def reset_topics():

    session = SessionLocal()

    try:

        deleted_mappings = (
            session.query(
                PostTopicMap
            ).delete()
        )

        deleted_topics = (
            session.query(
                Topic
            ).delete()
        )

        session.commit()

        print(
            f"Deleted {deleted_topics} topics"
        )

        print(
            f"Deleted {deleted_mappings} mappings"
        )

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()


if __name__ == "__main__":

    reset_topics()