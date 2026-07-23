from fastapi import FastAPI

from src.scoring.repository import (
    TrendScoreRepository
)

app = FastAPI(
    title="Instagram Trend Detection API"
)


@app.get("/v1/trends")
def get_trends(
    window: str = "24h",
    limit: int = 20
):

    trends = (
        TrendScoreRepository
        .get_top_trends(
            window=window,
            limit=limit
        )
    )

    response = []

    for trend in trends:

        response.append({

            "topic_id":
                trend.topic_id,

            "trend_score":
                trend.trend_score,

            "trend_status":
                trend.trend_status,

            "growth_rate":
                trend.growth_rate,

            "momentum_score":
                trend.momentum_score,

            "velocity":
                trend.velocity
        })

    return {
        "window": window,
        "count": len(response),
        "trends": response
    }

@app.get("/v1/topic/{topic_id}")
def get_topic(
    topic_id: str
):

    trends = (
        TrendScoreRepository
        .get_top_trends(
            window="24h",
            limit=1000
        )
    )

    for trend in trends:

        if trend.topic_id == topic_id:

            return {

                "topic_id":
                    trend.topic_id,

                "trend_score":
                    trend.trend_score,

                "trend_status":
                    trend.trend_status,

                "growth_rate":
                    trend.growth_rate,

                "momentum_score":
                    trend.momentum_score
            }

    return {
        "error":
            "Topic not found"
    }

@app.get("/v1/config")
def get_config():

    return {
        "message":
            "Config endpoint"
    }

@app.get("/admin/flags")
def get_flags():

    return {

        "fraud_detection":
            True,

        "geo_ranking":
            True,

        "sentiment":
            True
    }

@app.post("/admin/config/reload")
def reload_config():

    return {
        "status":
            "reloaded"
    }

@app.post("/admin/topic/merge")
def merge_topics():

    return {
        "status":
            "merged"
    }