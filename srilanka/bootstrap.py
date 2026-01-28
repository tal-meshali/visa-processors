from common.data_classes import PassportData
from srilanka.srilanka_pipeline import SriLankaEVisaPipeline
from srilanka.util_types import SriLankaPayloadData, SriLankaTravelData, SriLankaContactData, \
    SriLankaRequestData
from datetime import datetime

pipeline = SriLankaEVisaPipeline()

pipeline.run(SriLankaPayloadData(
    passport=PassportData(
        passport_number="12346664",
        first_name="ISRAEL",
        last_name="ISRAELI",
        sex="M",
        date_of_birth=datetime(2011, 7, 6),
        date_of_issue=datetime(2022, 8, 19),
        date_of_expiry=datetime(2027, 8, 18),
        place_of_birth="ISRAEL",
        nationality="ISRAELI",
    ),
    contact=SriLankaContactData(
        email_address="a@gmail.com",
        phone_number="0521234567",
        address="ADDRESS",
        city="CITY"
    ),
    travel=SriLankaTravelData(
        date_of_arrival=datetime(2025, 12, 31),
        date_of_departure=datetime(2026, 1, 29)
    ), request=SriLankaRequestData(amount_of_days=30))
)
