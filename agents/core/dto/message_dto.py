import time

class MessageDTO:

    def __init__(self, sender: str=None, recipient: str=None, message: str=None, data: dict = None,
                 timestamp: str = None):
        self.recipient = recipient
        self.message = message
        self.data = data
        self.sender = sender

        if not timestamp:
            self.timestamp: str = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp
        }
