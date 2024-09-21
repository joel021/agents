from mongoengine import Document, ListField, DictField, StringField


class Task(Document):

    description = StringField()
    instructions = ListField(DictField())

