from abc import ABC, abstractmethod
from typing import Dict, Optional, List

from bs4 import BeautifulSoup
from requests import Session

from processing.common.stages.evisa_stage import BaseEVisaStage
from processing.tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData

AUTHENTICATION_FIELDS = [
    "__RequestVerificationToken",
    "appID",
    "ApplicationID",
    "ApplicationId",
    "UserId",
]


class BaseTanzaniaEVisaStage(BaseEVisaStage[TanzaniaPayloadData, TanzaniaVisaStages], ABC):
    document: BeautifulSoup = None
    data_key = "data"

    def set_document(self, session: Session) -> None:
        response = session.get(self.stage.value)
        print("\nGet", self.stage.name, response.status_code)
        self.document = BeautifulSoup(response.content.decode(), "html.parser")

    def get_extra_fields(self) -> List[str]:
        return [f"{self.stage.name}ID"]

    def extract_auth_fields_from_document(self):
        extracted_authentication_fields = {}
        fields_to_search = AUTHENTICATION_FIELDS + self.get_extra_fields()
        for field in fields_to_search:
            output = self.document.find("input", {"name": field})
            if output:
                extracted_authentication_fields[field] = output.get("value")

        return extracted_authentication_fields

    def handle(self, session: Session, data: TanzaniaPayloadData):
        self.set_document(session)
        authentication_fields = self.extract_auth_fields_from_document()
        processed_data = self.process_data(data)
        body = {
            **processed_data,
            **authentication_fields,
            "submitPI": "saveContinue",
        }
        processed_files = self.process_files(data)
        return self.post_data(session, body, files=processed_files)
