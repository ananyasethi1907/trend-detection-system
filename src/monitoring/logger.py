class AppLogger:

    @staticmethod
    def info(
        message
    ):

        print(
            f"[INFO] {message}"
        )

    @staticmethod
    def error(
        message
    ):

        print(
            f"[ERROR] {message}"
        )