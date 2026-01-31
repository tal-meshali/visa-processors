import os
from mimetypes import guess_type
from typing import Dict, Optional, List

from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData
from common.util_methods import (
    assert_firebase_gcs_https_url,
    download_bytes_from_firebase_gcs_url,
    extract_bucket_and_blob_from_firebase_gcs_url,
)


class TanzaniaDocumentsUploadStage(BaseTanzaniaEVisaStage):
    stage = TanzaniaVisaStages.DocumentInfo

    @staticmethod
    def process_file(field_name: str, url: str, result: Dict):
        assert_firebase_gcs_https_url(url)
        _, blob_path = extract_bucket_and_blob_from_firebase_gcs_url(url)
        name = os.path.basename(blob_path) or field_name
        content = download_bytes_from_firebase_gcs_url(url)
        result[field_name] = (name, content, guess_type(name)[0])

    def process_files(
            self, data: TanzaniaPayloadData
    ) -> Optional[Dict]:
        files = {}
        self.process_file("Photo", data.documents.portrait_path, files)
        self.process_file("Passport", data.documents.passport_path, files)
        self.process_file(self.document.find("input", {"accept": ".pdf"}).get("name"),
                          data.documents.return_ticket_path,
                          files)
        return files

    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return {self.document.find("input", {"value": "9"}).get("name"): "9"}

    def get_extra_fields(self) -> List[str]:
        return super().get_extra_fields() + ["PhotoID", "PassportID", "SupportDocsDocuments.index"]
