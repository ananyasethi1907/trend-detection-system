from src.ingestion.storage import PostStorage

from src.nlp.entity_extractor import EntityExtractor

from src.nlp.keyword_extractor import KeywordExtractor

from src.nlp.topic_generator import TopicGenerator

from src.nlp.topic_assignment import TopicAssigner

def run_nlp():

    extractor = EntityExtractor()

    keyword_extractor = KeywordExtractor()

    posts = PostStorage.get_posts()

    print(

        f"Found {len(posts)} posts"

    )

    assigned = 0

    skipped = 0

    for post in posts:

        caption = post.caption or ""

        entities = extractor.extract(

            caption=caption,

            hashtags=[],

            language=post.language or "en"

        )

        keywords = keyword_extractor.extract(

            caption

        )

        topic = TopicGenerator.generate(

            caption=caption,

            entities=entities,

            keywords=keywords

        )

        print("\n" + "=" * 80)

        print("POST :", post.post_id)

        print("TOPIC:", topic)

        if topic is None:

            print("SKIPPED")

            skipped += 1

            continue

        TopicAssigner.assign_post_to_topic(

            post_id=post.post_id,

            topic_name=topic,

            entity_type="TOPIC",

            confidence=1.0

        )

        assigned += 1

    print("\n")

    print("=" * 80)

    print("Assigned :", assigned)

    print("Skipped  :", skipped)


if __name__ == "__main__":

    run_nlp()