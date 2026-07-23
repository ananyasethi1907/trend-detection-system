from sklearn.metrics.pairwise import cosine_similarity

import numpy as np


class TopicSimilarity:

    @staticmethod
    def similarity(
        vector1,
        vector2
    ):

        return cosine_similarity(

            np.array(
                vector1
            ).reshape(1, -1),

            np.array(
                vector2
            ).reshape(1, -1)

        )[0][0]