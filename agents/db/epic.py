from mongoengine import Document, StringField, ListField, ReferenceField, EnumField

from agents.db.status import Status
from agents.db.story import Story


class Epic(Document):

    title = StringField()
    status = EnumField(Status, default=Status.TODO) # DONE,TO_DO,PROGRESS
    description = StringField()
    stories = ListField(ReferenceField(Story))
    summary = StringField()

