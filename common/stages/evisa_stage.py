from abc import ABC, abstractmethod
from typing import Dict, Generic, Optional
import json
from requests import Session

from processing.common.util_types import TStage, TPayloadData


class BaseEVisaStage(Generic[TPayloadData, TStage], ABC):
    stage: TStage
    method = 'post'
    data_key: str

    def _get_headers(self, data: Dict) -> Optional[Dict]:
        return None

    def post_data(self, session: Session, data: Dict, files: Dict = None):
        response = session.request(self.method, self.stage.value, files=files,
                                   headers=self._get_headers(data), **{self.data_key: data})
        print(self.method, self.stage.name, response.status_code)
        return response

    @abstractmethod
    def process_data(self, data: TPayloadData) -> Dict:
        pass

    def process_files(self, data: TPayloadData) -> Optional[Dict]:
        pass

    @abstractmethod
    def handle(self, session: Session, data: TPayloadData):
        pass
