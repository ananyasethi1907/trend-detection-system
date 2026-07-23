from threading import Lock

from src.config.loader import ConfigLoader


class ConfigManager:

    def __init__(self):

        self._lock = Lock()

        self._loader = ConfigLoader()

        self._config = None

    def load(
        self,
        path: str
    ):

        with self._lock:

            self._config = (
                self._loader
                .load_from_file(path)
            )

    def reload(
        self,
        path: str
    ):

        with self._lock:

            self._config = (
                self._loader
                .load_from_file(path)
            )

    def get_config(self):

        return self._config