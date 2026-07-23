from datetime import datetime
from datetime import timedelta


class BackfillManager:

    @staticmethod
    def find_missing_cycles():

        return []

    @staticmethod
    def backfill():

        missing_cycles = (
            BackfillManager
            .find_missing_cycles()
        )

        return missing_cycles