from datetime import datetime


class Tracer:

    @staticmethod
    def trace(
        event
    ):

        print(
            datetime.utcnow(),
            event
        )