from src.geo.lookup_table import (
    COUNTRY_MAPPING
)


class GeoInference:

    @staticmethod
    def infer_country(
        country_code: str
    ):

        return COUNTRY_MAPPING.get(
            country_code,
            "Unknown"
        )