from datetime import datetime

from processing.morocco.morocco_pipeline import MoroccoEVisaPipeline
from processing.morocco.util_types import *

pipeline = MoroccoEVisaPipeline()

data = MoroccoPayloadData(
    passport=PassportData(
        passport_number="12345670",
        first_name="SEVENTH",
        last_name="SUR",
        sex="M",
        date_of_birth=datetime(2011, 7, 6),
        date_of_issue=datetime(2022, 8, 19),
        date_of_expiry=datetime(2027, 8, 18),
        place_of_birth="ISRAEL",
        nationality="ISRAELI",
    ),
    contact=ContactData(
        email_address="moredite1@gmail.com",
        phone_number="+972541234567"
    ),
    request=RequestPayloadData(
        request_id="ISR-25-010735"
    ),
    employment=EmploymentData(employment_status=""),
    travel=TravelData(date_of_arrival=datetime(2025, 12, 20), date_of_departure=datetime(2025, 12, 25)),
    documents=DocumentData(portrait_path=r"C:\Users\mesha\Documents\temp.png",
                           passport_path=r"C:\XboxGames\Minecraft for Windows\Content\data\resource_packs\vanilla\textures\ui\sidebar_icons\Jurassic_packicon_0.jpg"),
)

pipeline.run(data)
