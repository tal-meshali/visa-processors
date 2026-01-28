from abc import ABC
from typing import Dict, Optional

from requests import Session

from common.stages.evisa_stage import BaseEVisaStage
from srilanka.util_types import SriLankaPayloadData, SriLankaVisaStages


class BaseSriLankaEVisaStage(BaseEVisaStage[SriLankaPayloadData, SriLankaVisaStages], ABC):
    data_key = "data"

    def _get_headers(self, data: Dict) -> Optional[Dict]:
        return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}

    def handle(self, session: Session, data: SriLankaPayloadData):
        # self.set_document(session)
        processed_data = self.process_data(data)
        processed_files = self.process_files(data)
        return self.post_data(session, processed_data, files=processed_files)
