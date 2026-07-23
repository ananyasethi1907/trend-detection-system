from sentence_transformers import (
    SentenceTransformer
)


class TopicEmbedder:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed(
        self,
        text: str
    ):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )