class APICache:

    cache = {}

    @classmethod
    def get(
        cls,
        key
    ):

        return cls.cache.get(
            key
        )

    @classmethod
    def set(
        cls,
        key,
        value
    ):

        cls.cache[key] = value