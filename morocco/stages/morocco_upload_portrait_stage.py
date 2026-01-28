from common.variable import Variable
from morocco.stages.abstract.morocco_upload_document_stage import MoroccoUploadDocumentStage
from morocco.util_types import MoroccoPayloadData


class MoroccoUploadPortraitStage(MoroccoUploadDocumentStage):
    def get_variables(self, data: MoroccoPayloadData):
        return [
            *super().get_variables(data),
            Variable(["category", "codeCategory"], "295"),
            Variable(["category", "code"], "PHT"),
        ]

    def get_file_path(self, data: MoroccoPayloadData) -> str:
        return data.documents.portrait_path
