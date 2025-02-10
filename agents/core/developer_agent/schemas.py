
import typing_extensions as typing


class GenerateSoftwareArtifactsSchema(typing.TypedDict):
    artifact_code: str
    summary: str
    valid: bool

def __init__(self, artifact_code: str, summary: str,valid: bool):
        self.artifact_code = artifact_code
        self.summary = summary
        self.valid = valid
