from datetime import datetime

from src.db.connection import SessionLocal
from src.db.models import Account, Post


class PostStorage:

    @staticmethod
    def upsert_account(post: dict):

        session = SessionLocal()

        try:

            account = session.get(
                Account,
                post["account_id"]
            )

            if account:

                account.account_name = post.get(
                    "account_name",
                    account.account_name
                )

                account.followers_count = post.get(
                    "followers_count",
                    account.followers_count
                )

                account.is_verified = post.get(
                    "is_verified",
                    account.is_verified
                )

                account.last_updated = (
                    datetime.utcnow()
                )

            else:

                account = Account(
                    account_id=post["account_id"],
                    account_name=post.get(
                        "account_name",
                        ""
                    ),
                    followers_count=post.get(
                        "followers_count",
                        0
                    ),
                    is_verified=post.get(
                        "is_verified",
                        False
                    ),
                    first_seen=datetime.utcnow(),
                    last_updated=datetime.utcnow()
                )

                session.add(account)

            session.commit()

        except Exception:

            session.rollback()
            raise

        finally:

            session.close()

    @staticmethod
    def upsert_post(post: dict):

        session = SessionLocal()

        try:

            existing_post = session.get(
                Post,
                post["post_id"]
            )

            if existing_post:

                existing_post.likes = post.get(
                    "likes",
                    existing_post.likes
                )

                existing_post.comments = post.get(
                    "comments",
                    existing_post.comments
                )

                existing_post.views = post.get(
                    "views",
                    existing_post.views
                )

                existing_post.shares = post.get(
                    "shares",
                    existing_post.shares
                )

                existing_post.saves = post.get(
                    "saves",
                    existing_post.saves
                )

                scraped_at = post.get("scraped_at")

                if isinstance(scraped_at, str):
                    scraped_at = datetime.fromisoformat(scraped_at)

                existing_post.scraped_at = scraped_at

                existing_post.updated_at = (
                    datetime.utcnow()
                )

            else:

                geo = post.get(
                    "geo",
                    {}
                )

                db_post = Post(

                    post_id=post["post_id"],

                    account_id=post[
                        "account_id"
                    ],

                    content_type=post.get(
                        "content_type"
                    ),

                    caption=post.get(
                        "caption"
                    ),

                    likes=post.get(
                        "likes",
                        0
                    ),

                    comments=post.get(
                        "comments",
                        0
                    ),

                    views=post.get(
                        "views",
                        0
                    ),

                    shares=post.get(
                        "shares",
                        0
                    ),

                    saves=post.get(
                        "saves",
                        0
                    ),

                    language=post.get(
                        "language"
                    ),

                    country_code=geo.get(
                        "country_code"
                    ),

                    region=geo.get(
                        "region"
                    ),

                    city=geo.get(
                        "city"
                    ),

                    geotag_confidence=geo.get(
                        "geotag_confidence"
                    ),

                    published_at=datetime.fromisoformat(
                        post["published_at"]
                    ),

                    scraped_at=datetime.fromisoformat(
                        post["scraped_at"]
                    )
                )

                session.add(
                    db_post
                )

            session.commit()

        except Exception:

            session.rollback()
            raise

        finally:

            session.close()

    @classmethod
    def store(
        cls,
        post: dict
    ):

        cls.upsert_account(
            post
        )

        cls.upsert_post(
            post
        )

    @staticmethod
    def get_posts():

        session = SessionLocal()

        try:

            return (
                session.query(
                    Post
                ).all()
            )

        finally:

            session.close()

    @staticmethod
    def get_topics():

        session = SessionLocal()

        try:

            from src.db.models import Topic

            return (
                session.query(
                    Topic
                ).all()
            )

        finally:

            session.close()