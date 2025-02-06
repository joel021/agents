from mongoengine import Document, StringField, ListField, ReferenceField, EnumField

from agents.db.data_model import entity_list_to_dict_list
from agents.db.status import Status
from agents.db.story import Story


class Epic(Document):

    title = StringField()
    status = EnumField(Status, default=Status.TODO) # DONE,TO_DO,PROGRESS
    description = StringField()
    stories = ListField(ReferenceField(Story))
    summary = StringField()

    @staticmethod
    def from_dict(data: dict):
        Status
        epic = Epic(title=data.get("title", None),
                    status=Status.from_keyword(data.get("status", None)),
                    description=data.get("description", None),
                    summary=data.get("summary", None))

        return epic

    def to_dict(self):

        return {
            "title": self.title,
            "status": str(self.status).upper(),
            "description": self.description,
            "summary": self.summary,
            "stories": entity_list_to_dict_list(self.stories),
        }
