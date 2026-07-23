from sqlalchemy import text
import pandas as pd

from .database import engine


def execute_query(query, params=None):
    with engine.connect() as conn:
        return pd.read_sql(
            text(query),
            conn,
            params=params or {}
        )


# -------------------------------------------------
# Dashboard
# -------------------------------------------------

def get_dashboard_stats():

    posts = execute_query(
        "SELECT COUNT(*) AS count FROM posts"
    ).iloc[0]["count"]

    topics = execute_query(
        "SELECT COUNT(*) AS count FROM topics"
    ).iloc[0]["count"]

    accounts = execute_query(
        "SELECT COUNT(*) AS count FROM accounts"
    ).iloc[0]["count"]

    return {
        "posts": posts,
        "topics": topics,
        "accounts": accounts,
    }


def get_trends(limit=20):

    query = """
    SELECT
        t.canonical_name AS Topic,
        ts.trend_score AS "Trend Score",
        ts.momentum_score AS Momentum,
        ts.growth_rate AS "Growth Rate",
        ts.window AS Window,
        ts.trend_status AS Status
    FROM trend_scores ts
    JOIN topics t
        ON ts.topic_id = t.topic_id
    ORDER BY ts.trend_score DESC
    LIMIT :limit
    """

    return execute_query(
        query,
        {"limit": limit}
    )


def get_latest_posts(limit=20):

    query = """
    SELECT
        post_id,
        caption,
        likes,
        comments,
        views,
        published_at
    FROM posts
    ORDER BY published_at DESC
    LIMIT :limit
    """

    return execute_query(
        query,
        {"limit": limit}
    )


# -------------------------------------------------
# Topics
# -------------------------------------------------

def get_topics():

    query = """
    SELECT
        canonical_name,
        category,
        category_confidence,
        first_detected,
        last_active,
        inactive_count
    FROM topics
    ORDER BY canonical_name
    """

    return execute_query(query)


def get_topic_by_name(topic):

    query = """
    SELECT *
    FROM topics
    WHERE canonical_name = :topic
    """

    return execute_query(
        query,
        {"topic": topic}
    )


# -------------------------------------------------
# Accounts
# -------------------------------------------------

def get_accounts():

    query = """
    SELECT
        account_name,
        followers_count,
        is_verified,
        first_seen,
        last_updated
    FROM accounts
    ORDER BY followers_count DESC
    """

    return execute_query(query)


def get_account_posts(account):

    query = """
    SELECT
        p.*
    FROM posts p
    JOIN accounts a
        ON p.account_id = a.account_id
    WHERE a.account_name = :account
    ORDER BY p.published_at DESC
    """

    return execute_query(
        query,
        {"account": account}
    )


# -------------------------------------------------
# Analytics
# -------------------------------------------------

def get_category_distribution():

    query = """
    SELECT
        category,
        COUNT(*) AS count
    FROM topics
    GROUP BY category
    ORDER BY count DESC
    """

    return execute_query(query)


def get_daily_post_activity():

    query = """
    SELECT
        DATE(published_at) AS date,
        COUNT(*) AS posts
    FROM posts
    GROUP BY DATE(published_at)
    ORDER BY date
    """

    return execute_query(query)


def get_top_accounts(limit=10):

    query = """
    SELECT
        account_name,
        followers_count
    FROM accounts
    ORDER BY followers_count DESC
    LIMIT :limit
    """

    return execute_query(
        query,
        {"limit": limit}
    )


def get_top_trends(limit=10):

    query = """
    SELECT
        t.canonical_name,
        ts.trend_score
    FROM trend_scores ts
    JOIN topics t
        ON ts.topic_id = t.topic_id
    ORDER BY ts.trend_score DESC
    LIMIT :limit
    """

    return execute_query(
        query,
        {"limit": limit}
    )


def get_engagement_stats():

    query = """
    SELECT
        AVG(likes) AS avg_likes,
        AVG(comments) AS avg_comments,
        AVG(views) AS avg_views
    FROM posts
    """

    return execute_query(query)


# -------------------------------------------------
# Search
# -------------------------------------------------

def search_posts(keyword):

    query = """
    SELECT *
    FROM posts
    WHERE caption LIKE :keyword
    ORDER BY published_at DESC
    """

    return execute_query(
        query,
        {"keyword": f"%{keyword}%"}
    )


def search_topics(keyword):

    query = """
    SELECT *
    FROM topics
    WHERE canonical_name LIKE :keyword
    ORDER BY canonical_name
    """

    return execute_query(
        query,
        {"keyword": f"%{keyword}%"}
    )


def search_accounts(keyword):

    query = """
    SELECT *
    FROM accounts
    WHERE account_name LIKE :keyword
    ORDER BY followers_count DESC
    """

    return execute_query(
        query,
        {"keyword": f"%{keyword}%"}
    )