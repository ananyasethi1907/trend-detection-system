from datetime import datetime
from typing import Dict
from typing import List

import os

from dotenv import load_dotenv
from parsel import Selector
from scrapfly import (
    ScrapflyClient,
    ScrapeConfig
)

load_dotenv()

client = ScrapflyClient(
    key=os.getenv("SCRAPFLY_API_KEY")
)


def scrape_subreddit(
    subreddit: str
) -> Selector:

    result = client.scrape(

        ScrapeConfig(

            url=(
                f"https://www.reddit.com/r/{subreddit}/"
            ),

            asp=True,

            country="IN"

        )
    )

    return Selector(
        result.scrape_result[
            "content"
        ]
    )


def build_posts(
    selector: Selector
) -> List[Dict]:

    posts = []

    shreddit_posts = selector.xpath(
        "//shreddit-post"
    )

    for shreddit_post in shreddit_posts:

        title = shreddit_post.attrib.get(
            "post-title",
            ""
        )

        if not title:

            continue

        timestamp = shreddit_post.attrib.get(
            "created-timestamp"
        )

        published_at = datetime.utcnow().isoformat()

        if timestamp:

            try:

                published_at = datetime.strptime(
                    timestamp,
                    "%Y-%m-%dT%H:%M:%S.%f%z"
                ).replace(
                    tzinfo=None
                ).isoformat()

            except Exception:

                pass

        try:

            likes = int(
                shreddit_post.attrib.get(
                    "score",
                    0
                )
            )

        except:

            likes = 0

        try:

            comments = int(
                shreddit_post.attrib.get(
                    "comment-count",
                    0
                )
            )

        except:

            comments = 0

        author = shreddit_post.attrib.get(
            "author",
            "reddit"
        )

        post = {

            "post_id":
            shreddit_post.attrib.get(
                "id"
            ),

            "account_id":
            author,

            "account_name":
            author,

            "followers_count":
            0,

            "is_verified":
            False,

            "content_type":
            "reddit",

            "caption":
            title,

            "likes":
            likes,

            "comments":
            comments,

            "views":
            0,

            "shares":
            0,

            "saves":
            0,

            "language":
            shreddit_post.attrib.get(
                "post-language",
                "en"
            ),

            "geo":
            {},

            "published_at":
            published_at,

            "scraped_at":
            datetime.utcnow().isoformat(),

            "source":
            "reddit"

        }

        posts.append(
            post
        )

    return posts


def scrape_subreddits(
    subreddits: List[str]
) -> List[Dict]:

    all_posts = []

    for subreddit in subreddits:

        try:

            print(
                f"Scraping r/{subreddit}"
            )

            selector = (
                scrape_subreddit(
                    subreddit
                )
            )

            posts = (
                build_posts(
                    selector
                )
            )

            all_posts.extend(
                posts
            )

            print(
                f"Collected {len(posts)} posts"
            )

        except Exception as e:

            print(
                f"Failed r/{subreddit}: {e}"
            )

    return all_posts