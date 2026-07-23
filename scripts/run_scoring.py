from datetime import datetime

from src.config.loader import (
    ConfigLoader
)

from src.db.connection import (
    SessionLocal
)

from src.db.models import (
    Post,
    Account,
    Topic,
    PostTopicMap
)

from src.scoring.engine import (
    ScoringEngine
)

from src.scoring.storage import (
    TrendScoreStorage
)


def build_scoring_posts():

    session = SessionLocal()

    try:

        rows = (

            session.query(

                Post,
                Account,
                Topic

            )

            .join(
                Account,
                Post.account_id
                ==
                Account.account_id
            )

            .join(
                PostTopicMap,
                Post.post_id
                ==
                PostTopicMap.post_id
            )

            .join(
                Topic,
                PostTopicMap.topic_id
                ==
                Topic.topic_id
            )

            .all()
        )

        posts = []

        now = datetime.utcnow()

        for (

            post,
            account,
            topic

        ) in rows:

            age_hours = (

                now
                -
                post.published_at

            ).total_seconds() / 3600

            posts.append({

                "post_id":
                    post.post_id,

                "topic":
                    topic.canonical_name,

                "likes":
                    post.likes,

                "comments":
                    post.comments,

                "views":
                    post.views,

                "shares":
                    post.shares,

                "saves":
                    post.saves,

                "age_hours":
                    age_hours,

                "account_id":
                    account.account_id,

                "followers_count":
                    account.followers_count,

                "is_verified":
                    account.is_verified,

                "manipulation_flag":
                    False
            })

        return posts

    finally:

        session.close()


def run_scoring():

    loader = ConfigLoader()

    config = loader.load_from_file(
        "scoring_config.json"
    )

    posts = build_scoring_posts()

    print(
        f"Scoring {len(posts)} post-topic pairs"
    )

    engine = ScoringEngine(
        config=config
    )

    results = engine.score_window(

        posts=posts,

        window="24h",

        cycle_id=
        datetime.utcnow().isoformat()
    )

    print("\nTop Trends:\n")

    for result in results[:20]:

        print(

            f"{result['topic']} | "

            f"{result['trend_score']:.2f} | "

            f"{result['trend_status']}"
        )

    for result in results:

        TrendScoreStorage.save_score(

            topic_id=
            result["topic"],

            window=
            result["window"],

            cycle_id=
            result["cycle_id"],

            trend_score=
            result["trend_score"],

            trend_status=
            result["trend_status"],

            growth_rate=
            result["growth_rate"],

            momentum_score=
            result["momentum"],

            velocity=
            result["total_velocity"]
        )


if __name__ == "__main__":

    run_scoring()