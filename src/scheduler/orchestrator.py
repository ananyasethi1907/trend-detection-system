from datetime import datetime

from src.config.loader import (
    ConfigLoader
)

from src.scoring.engine import (
    ScoringEngine
)


class ScoringOrchestrator:

    def __init__(self):

        loader = ConfigLoader()

        self.config = (
            loader.load_from_file(
                "scoring_config.json"
            )
        )

        self.engine = (
            ScoringEngine(
                config=self.config
            )
        )

    def run_cycle(
        self,
        window: str
    ):

        cycle_id = (
            datetime.utcnow()
            .isoformat()
        )

        results = (
            self.engine.score_window(
                window=window,
                cycle_id=cycle_id
            )
        )

        return results

    def run_all_windows(self):

        windows = [

            "1h",
            "6h",
            "24h",
            "7d"
        ]

        results = {}

        for window in windows:

            results[window] = (
                self.run_cycle(
                    window
                )
            )

        return results