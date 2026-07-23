class APIAuth:

    VALID_KEYS = {
        "demo-key"
    }

    @staticmethod
    def validate(
        api_key: str
    ):

        return (
            api_key
            in
            APIAuth.VALID_KEYS
        )