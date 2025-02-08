
class Message:

    def __init__(self, sender: str, recipient: str, message: str, data: dict = None):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "message": self.message,
            "data": self.data
        }
