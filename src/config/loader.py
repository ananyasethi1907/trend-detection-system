import json

from typing import Any
from typing import Dict

from src.config.schema import validate_schema


class ConfigLoader:

    def __init__(self):
        self._config = {}

    def load_from_file(
        self,
        path: str
    ) -> Dict[str, Any]:

        with open(path, "r") as file:
            config = json.load(file)

        validate_schema(config)

        self._config = config

        return config

    def validate_schema(
        self,
        config: Dict
    ) -> bool:

        return validate_schema(config)

    def get_factor(
        self,
        path: str,
        default: Any = None
    ) -> Any:

        keys = path.split(".")

        value = self._config

        try:

            for key in keys:
                value = value[key]

            return value

        except (
            KeyError,
            TypeError
        ):
            return default