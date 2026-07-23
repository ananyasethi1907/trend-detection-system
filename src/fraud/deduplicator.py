import hashlib


class ContentDeduplicator:

    @staticmethod
    def generate_hash(
        text: str
    ):

        if not text:
            return None

        return hashlib.md5(
            text.lower().strip().encode()
        ).hexdigest()

    @staticmethod
    def is_duplicate(
        text: str,
        existing_hashes: set
    ):

        content_hash = (
            ContentDeduplicator
            .generate_hash(text)
        )

        return (
            content_hash
            in
            existing_hashes
        )