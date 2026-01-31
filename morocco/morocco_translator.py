from datetime import datetime
from typing import Optional, Dict, Any

from google.cloud import firestore
from common.data_classes import DocumentData, ContactData, TravelData, EmploymentData, PassportData
from common.translator import Translator
from morocco.extract_visa_request_id import VisaRequestIdExtractor
from morocco.util_types import MoroccoPayloadData, RequestPayloadData


class MoroccoTranslator(Translator[MoroccoPayloadData]):
    def __init__(self):
        super().__init__()
        self.creation_request_id = VisaRequestIdExtractor().get_and_remove_request_id()

    def convert(self, form_data: Dict) -> MoroccoPayloadData:
        return MoroccoPayloadData(
            passport=self._convert_passport_data(form_data['passport_data']),
            documents=DocumentData(
                portrait_path=form_data.get('passport_photo', ''),
                passport_path=form_data.get('passport_copy', '')
            ),
            contact=ContactData(
                phone_number=form_data.get('phone_number', ''),
                email_address=self.EMAIl
            ),
            travel=TravelData(
                date_of_arrival=self._format_datetime(form_data['travel_date']),
                date_of_departure=self._format_datetime(form_data['departure_date']),
            ),
            employment=EmploymentData(occupation=form_data.get("occupation", '')),
            request=RequestPayloadData(request_id=self.creation_request_id)
        )
