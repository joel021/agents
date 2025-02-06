
class DataModel:

    @staticmethod
    def from_dict(data: dict):
        raise NotImplementedError("From dict not implemented")

    def to_dict(self) -> dict:
        raise NotImplementedError("To dict not implemented")


def entity_list_to_dict_list(entity_list: list[DataModel]) -> list[dict]:
    list_dict_entities = []

    for entity in entity_list:
        list_dict_entities.append(entity.to_dict())

    return list_dict_entities

