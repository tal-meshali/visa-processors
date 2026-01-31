import json
import os
from abc import abstractmethod
from mimetypes import guess_type
from typing import Dict, Optional

from common.variable import Variable
from common.util_methods import (
    assert_firebase_gcs_https_url,
    download_bytes_from_firebase_gcs_url,
    extract_bucket_and_blob_from_firebase_gcs_url,
)
from morocco.stages.abstract.morocco_template_stage import MoroccoTemplateStage
from morocco.util_types import MoroccoVisaTemplates, MoroccoPayloadData, MoroccoVisaStages


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
        document_url = self.get_file_path(data)
        assert_firebase_gcs_https_url(document_url)
        
        file_content = download_bytes_from_firebase_gcs_url(document_url)
        
        _, blob_path = extract_bucket_and_blob_from_firebase_gcs_url(document_url)
        document_name = os.path.basename(blob_path)
        
        return {
            "attachment": ("blob", json.dumps(blob_result).encode(), "application/json"),
            "file": (document_name, file_content, guess_type(document_name)[0])
        }
