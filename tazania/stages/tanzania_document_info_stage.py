import os
from mimetypes import guess_type
from typing import Dict, Optional, List

from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData


class TanzaniaDocumentsUploadStage(BaseTanzaniaEVisaStage):
    stage = TanzaniaVisaStages.DocumentInfo

    @staticmethod
    def process_file(field_name: str, path: str, result: Dict):
        name = os.path.basename(path)
        with open(path, "rb") as f:
            result[field_name] = (os.path.basename(path), f.read(), guess_type(name)[0])

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
