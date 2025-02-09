
import typing_extensions as typing

from agents.core.dto.llm_schema import FunctionSchema


class MessageSchema(typing.TypedDict):

    sender: str
    recipient: str
    message: str

    def __init__(self, sender: str, recipient: str, message: str):
        self.sender = sender
        self.recipient = recipient
        self.message = message

class MessageAgents(typing.TypedDict):
    messages: typing.List[MessageSchema]

    def __init__(self, messages: typing.List[MessageSchema]):
        self.messages = messages

class GenerateDataBaseActionsSchema(typing.TypedDict):
    actions: typing.List[FunctionSchema]
    summary: str

    def __init__(self, actions: typing.List[FunctionSchema], summary: str):
        self.actions = actions
        self.summary = summary

