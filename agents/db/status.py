from enum import Enum


class Status(Enum):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    ERROR = 'ERROR'

    @staticmethod
    def from_keyword(keyword: str) -> 'Status':
        try:
            return Status[keyword.upper()]
        except Exception as e:
            return Status.TODO
