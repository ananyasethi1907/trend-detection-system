from typing import Dict
from typing import List
from typing import Tuple

from src.config.loader import (
    ConfigLoader
)

from src.ingestion.validator import (
    PostValidator
)

from src.ingestion.enricher import (
    PostEnricher
)

from src.ingestion.storage import (
    PostStorage
)


class PostIngester:

    def __init__(self):

        loader = ConfigLoader()

        self.config = (
            loader.load_from_file(
                "scoring_config.json"
            )
        )

    def consume_batch(
        self,
        batch: List[Dict]
    ) -> Tuple[
        List[str],
        List[str]
    ]:

        successful_ids = []

        failed_ids = []

        for post in batch:

            try:

                valid, reason = (
                    PostValidator.validate_post(
                        post,
                        self.config
                    )
                )

                if not valid:

                    failed_ids.append(
                        post.get(
                            "post_id",
                            "unknown"
                        )
                    )

                    continue

                enriched_post = (
                    PostEnricher.enrich(
                        post
                    )
                )

                PostStorage.store(
                    enriched_post
                )

                successful_ids.append(
                    post["post_id"]
                )

            except Exception:

                failed_ids.append(
                    post.get(
                        "post_id",
                        "unknown"
                    )
                )

        return (
            successful_ids,
            failed_ids
        )