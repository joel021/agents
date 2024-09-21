from mongoengine import Document, StringField, DictField, ListField

class Instruction(Document):

    function = StringField()
    args = DictField()
    text = StringField()
    next_tasks = ListField(StringField())

