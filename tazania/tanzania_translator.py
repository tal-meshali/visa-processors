import os
from datetime import datetime
from typing import Dict, Any

from common.data_classes import PassportData, EmploymentData
from common.translator import Translator
from tazania.util_types import (
    TanzaniaPayloadData,
    TanzaniaContactData,
    TanzaniaTravelData,
    TanzaniaDocumentData,
    PersonalData
)


class TanzaniaTranslator(Translator):
    def convert(self, form_data: Dict) -> TanzaniaPayloadData:
        return TanzaniaPayloadData(
            passport=self._convert_passport_data(form_data['passport_data']),
            documents=TanzaniaDocumentData(
                portrait_path=form_data.get('passport_photo', ''),
                passport_path=form_data.get('passport_copy', ''),
                return_ticket_path=form_data.get("return_ticket", ""),
            ),
            contact=TanzaniaContactData(
                email_address=self.EMAIl,
                phone_number=form_data.get("phone_number", ""),
                physical_address=form_data.get("physical_address", ""),
                physical_address_city=form_data.get("physical_address_city", ""),
                physical_address_country=form_data.get("physical_address_country", "")
            ),
            travel=TanzaniaTravelData(
                date_of_arrival=self._format_datetime(form_data['travel_date']),
                date_of_departure=self._format_datetime(form_data['departure_date']),
                stay_address=form_data.get("stay_address", ""),
                destination=form_data.get("destination"),
                accommodation_type=form_data.get("accommodation_type", "Hotel"),
                date_of_last_visit=self._format_datetime(form_data["date_of_last_visit"]) if form_data.get(
                    "date_of_last_visit") else None
            ),
            employment=EmploymentData(occupation=form_data.get("occupation", '')),
            personal=PersonalData(
                marital_status=form_data.get("marital_status", "")
            )
        )
