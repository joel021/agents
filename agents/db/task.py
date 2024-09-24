import typing
from mongoengine import Document, ListField, DictField, StringField, EnumField

from agents.db.status import Status


class Task(typing.TypedDict, Document):

    title = StringField()
    status = EnumField(Status, default=Status.TODO)
    specification = StringField() #What to do
    instructions = ListField(DictField()) #Set of instructions performed
    summary = StringField() #How have done

    def is_done(self):
        return self.status == Status.DONE
