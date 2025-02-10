from mongoengine import Document, StringField, DictField

from agents.db.status import Status

class Message(Document):

    sender = StringField()
    recipient = StringField()
    message = StringField()
    data = DictField()
    timestamp = StringField()

    @staticmethod
    def from_dict(data: dict):

        message = Message(sender=data.get("sender", None),
                          recipient=data.get("recipient", None),
                          message=data.get("message", None),
                          data=data.get("data", None),
                          timestamp=data.get("timestamp", None)
                        )
        return message

    def to_dict(self):

        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp
        }
