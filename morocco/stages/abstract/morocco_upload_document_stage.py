import json
import os
from abc import abstractmethod
from mimetypes import guess_type
from typing import Dict, Optional

from processing.common.variable import Variable
from processing.morocco.stages.abstract.morocco_template_stage import MoroccoTemplateStage
from processing.morocco.util_types import MoroccoVisaTemplates, MoroccoPayloadData, MoroccoVisaStages
from services.gcs_service import gcs_service


class MoroccoUploadDocumentStage(MoroccoTemplateStage):
    stage = MoroccoVisaStages.UploadDocuments
    template = MoroccoVisaTemplates.Blob

    @abstractmethod
    def get_file_path(self, data: MoroccoPayloadData) -> str:
        pass

    def get_variables(self, data: MoroccoPayloadData):
        return [
            Variable(["description"], os.path.basename(self.get_file_path(data))),
            Variable(["attachableId"], data.request.beneficiary_id),
        ]

    def process_data(self, data: MoroccoPayloadData) -> Dict:
        pass

    def process_files(self, data: MoroccoPayloadData) -> Optional[Dict]:
        blob_result = super().process_template(data)
        document_path = self.get_file_path(data)
        document_name = os.path.basename(document_path)

        return {"attachment": ("blob", json.dumps(blob_result).encode(), "application/json"),
                "file": (document_name, gcs_service.get_item(document_path), guess_type(document_name)[0])}
