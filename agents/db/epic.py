from mongoengine import Document, StringField, ListField, ReferenceField

from agents.db.story import Story


class Epic(Document):

    description = StringField()
    stories = ListField(ReferenceField(Story))

