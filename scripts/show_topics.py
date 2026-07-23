from src.ingestion.storage import PostStorage

topics = PostStorage.get_topics()

print(f"Total topics: {len(topics)}\n")

for topic in topics:
    print(topic.canonical_name)