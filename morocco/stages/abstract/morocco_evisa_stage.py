from abc import ABC, abstractmethod
from typing import Dict, Optional

from requests import Session, Response

from common.stages.evisa_stage import BaseEVisaStage
from morocco.util_types import MoroccoPayloadData, MoroccoVisaStages

MOROCCO_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"


class BaseMoroccoEVisaStage(BaseEVisaStage[MoroccoPayloadData, MoroccoVisaStages], ABC):
    USER_AGENT = MOROCCO_USER_AGENT
    data_key = "json"

    def handle(self, session: Session, data: MoroccoPayloadData):
        print(f"Started handling {self.stage.name}")
        processed_data = self.process_data(data)
        processed_files = self.process_files(data)
        response = self.post_data(session, processed_data, files=processed_files)
        self.process_response(session, data, response)

    def process_response(self, session: Session, data: MoroccoPayloadData, response: Response):
        pass

    def _get_headers(self, data: Dict) -> Optional[Dict]:
        return None if data is None else {"Content-Type": "application/json"}
