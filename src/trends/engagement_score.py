from math import log


class EngagementScore:

    @staticmethod
    def calculate(post):

        score = 0

        score += log(post.likes + 1) * 2
        score += log(post.comments + 1) * 3
        score += log(post.shares + 1) * 4
        score += log(post.saves + 1) * 3
        score += log(post.views + 1)

        return score