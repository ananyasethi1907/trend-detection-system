# src/scraper/instagram.py

import json

from datetime import datetime
from typing import Dict
from typing import List

from scrapfly import (
    ScrapflyClient,
    ScrapeConfig
)


SCRAPFLY_API_KEY = (
    "scp-test-dc52e22937664354ac0125a79ee215c0"
)

client = ScrapflyClient(
    key=SCRAPFLY_API_KEY
)


def scrape_profile(
    username: str
) -> Dict:

    result = client.scrape(

        ScrapeConfig(

            url=(
                "https://i.instagram.com/api/v1/"
                f"users/web_profile_info/"
                f"?username={username}"
            ),

            asp=True,

            country="US",

            headers={

                "x-ig-app-id":
                "936619743392459",

                "User-Agent":
                "Mozilla/5.0"
            }
        )
    )

    data = json.loads(
        result.scrape_result[
            "content"
        ]
    )

    return (
        data["data"]["user"]
    )


def build_posts(
    user: Dict
) -> List[Dict]:

    posts = []

    account_id = (
        user["id"]
    )

    account_name = (
        user["username"]
    )

    followers_count = (
        user["edge_followed_by"]["count"]
    )

    is_verified = (
        user.get(
            "is_verified",
            False
        )
    )

    edges = (

        user
        .get(
            "edge_owner_to_timeline_media",
            {}
        )
        .get(
            "edges",
            []
        )
    )

    for edge in edges:

        node = edge["node"]

        caption_edges = (

            node
            .get(
                "edge_media_to_caption",
                {}
            )
            .get(
                "edges",
                []
            )
        )

        caption = ""

        if caption_edges:

            caption = (
                caption_edges[0]
                ["node"]["text"]
            )

        post = {

            "post_id":
            str(
                node["id"]
            ),

            "account_id":
            account_id,

            "account_name":
            account_name,

            "followers_count":
            followers_count,

            "is_verified":
            is_verified,

            "content_type":
            node.get(
                "__typename",
                "GraphImage"
            ),

            "caption":
            caption,

            "likes":
            node.get(
                "edge_liked_by",
                {}
            ).get(
                "count",
                0
            ),

            "comments":
            node.get(
                "edge_media_to_comment",
                {}
            ).get(
                "count",
                0
            ),

            "views":
            node.get(
                "video_view_count",
                0
            ),

            "shares":
            0,

            "saves":
            0,

            "language":
            "en",

            "geo":
            {},

            "published_at":
            datetime.utcfromtimestamp(
                node[
                    "taken_at_timestamp"
                ]
            ).isoformat(),

            "scraped_at":
            datetime.utcnow().isoformat()
        }

        posts.append(
            post
        )

    return posts


def scrape_accounts(
    usernames: List[str]
) -> List[Dict]:

    all_posts = []

    for username in usernames:

        try:

            print(
                f"Scraping @{username}"
            )

            user = (
                scrape_profile(
                    username
                )
            )

            posts = (
                build_posts(
                    user
                )
            )

            all_posts.extend(
                posts
            )

            print(
                f"Collected "
                f"{len(posts)} posts"
            )

        except Exception as e:

            print(
                f"Failed "
                f"@{username}: {e}"
            )

    return all_posts