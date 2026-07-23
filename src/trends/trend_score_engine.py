from src.trends.engagement_score import EngagementScore
from src.trends.freshness_score import FreshnessScore
from src.trends.velocity_score import VelocityScore
from src.trends.diversity_score import DiversityScore


class TopicTrendScoreEngine:

    @staticmethod
    def calculate(posts):

        """
        posts: list of Post ORM objects mapped to a single topic
        (i.e. all posts joined via post_topic_map for that topic_id).

        Reuses the existing per-post calculators unchanged and
        aggregates them into one topic-level trend score.
        """

        if not posts:

            return None

        engagement_total = 0

        freshness_best = 0

        velocity_values = []

        diversity_values = []

        account_ids = set()

        for post in posts:

            ###################################################
            # Engagement: summed across posts. A topic backed by
            # more engaged posts is a stronger trend -- this rewards
            # both engagement quality AND post volume together.
            #
            # NOTE: because this is a sum (not an average), a topic
            # with many posts will naturally score higher on this
            # component than a topic with one viral post, even if
            # per-post engagement is similar. That's a deliberate
            # choice, not an oversight -- flag if you'd rather average
            # instead, it's a one-line change.
            ###################################################

            engagement_total += EngagementScore.calculate(post)

            ###################################################
            # Freshness: take the MOST recent post's freshness, not
            # an average. A topic is "fresh" if it's still getting
            # new posts -- averaging in old posts would incorrectly
            # drag down a topic that's actively trending right now.
            ###################################################

            post_freshness = FreshnessScore.calculate(post)

            if post_freshness > freshness_best:

                freshness_best = post_freshness

            ###################################################
            # Velocity / Diversity: averaged across posts, since
            # these are per-post proxy scores (not true rate/spread
            # metrics) and summing them would just re-reward post
            # volume a second time on top of Engagement.
            ###################################################

            velocity_values.append(

                VelocityScore.calculate(post)

            )

            diversity_values.append(

                DiversityScore.calculate(post)

            )

            account_id = getattr(post, "account_id", None)

            if account_id is not None:

                account_ids.add(account_id)

        velocity_avg = sum(velocity_values) / len(velocity_values)

        diversity_avg = sum(diversity_values) / len(diversity_values)

        ###################################################
        # Account-spread bonus
        #
        # The existing DiversityScore measures content richness per
        # post (caption length, geo, language) -- it says nothing
        # about how many DIFFERENT accounts are posting about this
        # topic, which is the more natural meaning of "diversity" at
        # the topic level. This adds that signal on top rather than
        # replacing the existing score.
        ###################################################

        account_spread_bonus = min(

            len(account_ids) * 2,

            10

        )

        diversity_final = min(

            diversity_avg + account_spread_bonus,

            30

        )

        final_score = (

            engagement_total * 0.45 +

            freshness_best * 0.30 +

            velocity_avg * 0.15 +

            diversity_final * 0.10

        )

        return {

            "engagement": round(engagement_total, 2),

            "freshness": round(freshness_best, 2),

            "velocity": round(velocity_avg, 2),

            "diversity": round(diversity_final, 2),

            "post_count": len(posts),

            "unique_accounts": len(account_ids),

            "trend_score": round(final_score, 2)

        }