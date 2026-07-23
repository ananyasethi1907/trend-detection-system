class CycleIdempotency:

    processed_cycles = set()

    @classmethod
    def already_processed(
        cls,
        cycle_id: str
    ):

        return (
            cycle_id
            in
            cls.processed_cycles
        )

    @classmethod
    def mark_processed(
        cls,
        cycle_id: str
    ):

        cls.processed_cycles.add(
            cycle_id
        )