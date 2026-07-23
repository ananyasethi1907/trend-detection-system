from transformers import pipeline


class SentimentAnalyzer:

    def __init__(self):

        self.model = pipeline(
            "sentiment-analysis"
        )

    def analyze(
        self,
        text: str
    ):

        if not text:

            return {
                "positive": 0.0,
                "neutral": 1.0,
                "negative": 0.0
            }

        result = self.model(
            text[:512]
        )[0]

        label = result["label"]
        score = result["score"]

        if label.upper() == "POSITIVE":

            return {
                "positive": score,
                "neutral": 1 - score,
                "negative": 0
            }

        return {
            "positive": 0,
            "neutral": 1 - score,
            "negative": score
        }