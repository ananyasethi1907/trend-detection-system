from datetime import datetime


class FreshnessScore:

    @staticmethod
    def calculate(post):

        if post.published_at is None:
            return 0

        age_hours = (
            datetime.utcnow() - post.published_at
        ).total_seconds() / 3600

        if age_hours <= 1:
            return 30

        if age_hours <= 6:
            return 25

        if age_hours <= 12:
            return 20

        if age_hours <= 24:
            return 15

        if age_hours <= 48:
            return 10

        return 5