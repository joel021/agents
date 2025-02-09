from agents.db.message import Message


class MessageService:

    def save(self, message: dict) -> Message:

        return Message.from_dict(message).save()

    def read_messages(self):

        return Message.objects.all()

