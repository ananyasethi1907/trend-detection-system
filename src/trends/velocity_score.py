from math import log


class VelocityScore:

    @staticmethod
    def calculate(post):

        score = 0

        ###################################################
        # Shares spread content the fastest
        ###################################################

        score += log(post.shares + 1) * 5

        ###################################################
        # Comments indicate active discussion
        ###################################################

        score += log(post.comments + 1) * 3

        ###################################################
        # Views indicate reach
        ###################################################

        score += log(post.views + 1)

        ###################################################
        # Cap the score
        ###################################################

        return min(round(score, 2), 30)