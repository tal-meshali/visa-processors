from datetime import datetime

from morocco.util_types import *
from tazania.tanzania_pipeline import TanzaniaEVisaPipeline
from tazania.util_types import TanzaniaPayloadData, TanzaniaContactData, TanzaniaTravelData, PersonalData, \
    TanzaniaDocumentData

pipeline = TanzaniaEVisaPipeline()

data = TanzaniaPayloadData(
    passport=PassportData(
        passport_number="1234",
        first_name="ISRAEL",
        last_name="ISRAELI",
        sex="M",
        date_of_birth=datetime(2011, 7, 6),
        date_of_issue=datetime(2022, 8, 19),
        date_of_expiry=datetime(2027, 8, 18),
        place_of_birth="ISRAEL",
        nationality="ISRAELI",
    ),
    contact=TanzaniaContactData(
        email_address="a@gmail.com",
        phone_number="+972541234567",
        physical_address="Different Middle street",
        physical_address_city="Tel Aviv",
        physical_address_country="ISRAEL",
    ),
    # TODO: Enter countries resided
    personal=PersonalData(marital_status="Single"),
    employment=EmploymentData(employment_status="Employed"),
    # TODO: Enter port of entry, port of departure
    travel=TanzaniaTravelData(
        date_of_arrival=datetime(2025, 12, 21),
        date_of_departure=datetime(2025, 12, 31),
        stay_address="AAAA",
        date_of_last_visit=datetime(2022, 1, 1),
        destination="Zanzibar"
    ),
    documents=TanzaniaDocumentData(
        portrait_path="C:\\Users\\mesha\\Documents\\temp.png",
        passport_path="C:\\Users\\mesha\\Documents\\temp.png",
        return_ticket_path="C:\\Users\\mesha\\Downloads\\temp.pdf",
    ),
)

pipeline.run(data)
