from typing import Dict
from typing import List

import hashlib

from sentence_transformers import (
    SentenceTransformer
)


class EntityEmbedder:

    def __init__(self):

        self.model = (
            SentenceTransformer(
                "paraphrase-multilingual-MiniLM-L12-v2"
            )
        )

        self.cache = {}

    def _cache_key(
        self,
        entity_text: str,
        language: str
    ) -> str:

        raw = (
            f"{entity_text}:{language}"
        )

        return hashlib.md5(
            raw.encode()
        ).hexdigest()

    def embed_entity(
        self,
        entity_text: str,
        language: str = "en"
    ):

        key = self._cache_key(
            entity_text,
            language
        )

        if key in self.cache:

            return self.cache[key]

        embedding = self.model.encode(
            entity_text
        )

        self.cache[key] = embedding

        return embedding

    def embed_batch(
        self,
        entities: List[str],
        language: str = "en"
    ) -> Dict:

        unique_entities = list(
         dict.fromkeys(entities)
        )

        embeddings = self.model.encode(
            unique_entities
        )

        result = {}

        for entity, embedding in zip(
            unique_entities,
            embeddings
        ):

            key = self._cache_key(
                entity,
                language
            )

            self.cache[key] = embedding

            result[entity] = embedding

        return result