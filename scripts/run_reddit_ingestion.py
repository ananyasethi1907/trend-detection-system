import json

from src.scraper.reddit import (
    scrape_subreddits
)

from src.ingestion.validator import (
    PostValidator
)

from src.ingestion.storage import (
    PostStorage
)

from src.config.loader import (
    ConfigLoader
)


def run_ingestion():

    loader = ConfigLoader()

    config = loader.load_from_file(
        "scoring_config.json"
    )

    with open(
        "src/config/seed_subreddits.json",
        "r"
    ) as file:

        subreddits = json.load(
            file
        )["subreddits"]

    posts = scrape_subreddits(
        subreddits
    )

    print(
        f"Collected {len(posts)} posts"
    )

    stored = 0

    for post in posts:

        is_valid, reason = (
            PostValidator.validate_post(
                post,
                config
            )
        )

        if not is_valid:

            print(
                f"Skipped: {reason}"
            )

            continue

        PostStorage.store(
            post
        )

        stored += 1

    print(
        f"Stored {stored} posts"
    )


if __name__ == "__main__":

    run_ingestion()