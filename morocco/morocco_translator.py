from datetime import datetime

from processing.common.data_classes import DocumentData, ContactData, TravelData, EmploymentData
from processing.common.translator import Translator
from processing.morocco.util_types import MoroccoPayloadData, RequestPayloadData


class MoroccoTranslator(Translator[MoroccoPayloadData]):
    def __init__(self, *args, creation_request_id: str):
        super().__init__(*args)
        self.creation_request_id = creation_request_id

    def convert(self) -> MoroccoPayloadData:
        data = self.beneficiary
        return MoroccoPayloadData(
            passport=self._convert_passport_data(data['passport_data']),
            documents=DocumentData(portrait_path=data['passport_photo'], passport_path=data['passport_copy']),
            contact=ContactData(phone_number=data['phone_number'], email_address=self.EMAIL),
            travel=TravelData(date_of_arrival=datetime.strptime(data['travel_date'], '%d-%m-%Y'),
                              date_of_departure=datetime.strptime(data['departure_date'], '%d-%m-%Y')
                              ),
            employment=EmploymentData(occupation=data.get("occupation", '')),
            request=RequestPayloadData(request_id=self.creation_request_id)
        )
