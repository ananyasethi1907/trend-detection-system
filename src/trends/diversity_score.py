class DiversityScore:

    @staticmethod
    def calculate(post):

        score = 0

        ###################################################
        # Caption richness
        ###################################################

        if post.caption:

            words = len(post.caption.split())

            if words >= 30:

                score += 10

            elif words >= 15:

                score += 7

            elif words >= 5:

                score += 5

            else:

                score += 2

        ###################################################
        # Content type
        ###################################################

        if post.content_type:

            score += 3

        ###################################################
        # Geographic information
        ###################################################

        if post.country_code:

            score += 3

        if post.region:

            score += 2

        if post.city:

            score += 2

        ###################################################
        # Language detected
        ###################################################

        if post.language:

            score += 3

        ###################################################
        # Verified creator bonus
        #
        # (Can be improved later using Account table)
        ###################################################

        return min(score, 20)