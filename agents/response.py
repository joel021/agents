

class Response:

    def __init__(self, msg: str | None, error: bool):
        self.msg: str = msg
        self.error: bool = error

    def __str__(self):
        return f"Response(msg='{self.msg}', error={self.error})"

