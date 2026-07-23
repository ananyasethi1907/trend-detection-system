class Metrics:

    @staticmethod
    def record(
        metric_name,
        value
    ):

        print(
            f"[METRIC] "
            f"{metric_name}: "
            f"{value}"
        )