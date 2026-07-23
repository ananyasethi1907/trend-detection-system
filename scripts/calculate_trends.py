from src.trends.topic_post_service import TopicPostService
from src.trends.trend_score_engine import TopicTrendScoreEngine
from src.trends.trend_score_repository import TrendScoreRepository


def calculate_trends():

    topics = TopicPostService.get_all_topics()

    print(f"\nFound {len(topics)} topics\n")

    calculated = 0

    for topic in topics:

        posts = TopicPostService.get_posts(
            topic.topic_id
        )

        if not posts:
            continue

        score = TopicTrendScoreEngine.calculate(
            posts
        )

        if score is None:
            continue

        TrendScoreRepository.save(

            topic_id=topic.topic_id,

            score=score

        )

        calculated += 1

        print("=" * 70)

        print("Topic:", topic.canonical_name)

        print("Posts:", score["post_count"])

        print("Accounts:", score["unique_accounts"])

        print("Trend Score:", score["trend_score"])

    print("\n")

    print(f"Calculated trend scores for {calculated} topics")


if __name__ == "__main__":

    calculate_trends()