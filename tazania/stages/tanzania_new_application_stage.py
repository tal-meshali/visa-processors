from typing import Dict

from requests import Session

from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData


class TanzaniaNewApplicationStage(BaseTanzaniaEVisaStage):
    stage = TanzaniaVisaStages.NewApplication

    def extract_auth_fields_from_document(self):
        result = super().extract_auth_fields_from_document()
        print("AppID:", self.document.find(attrs={"id": "appID"}).getText())
        return result

    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return {}

    def post_data(self, session: Session, data: Dict, files: Dict = None):
        pass
