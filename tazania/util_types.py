from enum import Enum
from common.data_classes import *
from common.util_types import StageEnum, TemplateEnum
from dataclasses import dataclass


class TanzaniaVisaStages(StageEnum):
    Start = "start"
    NewApplication = "newapplication"
    ContinueApplication = "continueapplication"
    PersonalInfo = "personalinfo"
    ContactInfo = "contactinfo"
    PassportInfo = "passportinfo"
    TravelInfo = "travelinfo"
    DocumentInfo = "documentinfo"
    Declaration = "declaration"

    @property
    def base_url(self):
        return "https://visa.immigration.go.tz/"


class TanzaniaVisaTemplates(TemplateEnum):
    PersonalInfo = "personal_info"
    PassportInfo = "passport_info"
    ContactInfo = "contact_info"
    TravelInfo = "travel_info"
    Start = "start"

    @property
    def base_path(self):
        return "./templates"


@dataclass
class TanzaniaTravelData(TravelData):
    stay_address: str
    destination: str  # "Tanzania Mainland" / "Zanzibar"
    accommodation_type: str = "Hotel"  # / "Motel" / "Apartment" / "Private Residence"
    date_of_last_visit: datetime = None


@dataclass
class TanzaniaContactData(ContactData):
    physical_address: str
    physical_address_city: str
    physical_address_country: str


@dataclass
class TanzaniaDocumentData(DocumentData):
    return_ticket_path: str


@dataclass
class PersonalData:
    marital_status: str
    spouse_name: str = None
    spouse_nationality: str = None


@dataclass
class TanzaniaPayloadData:
    passport: PassportData
    contact: TanzaniaContactData
    personal: PersonalData
    employment: EmploymentData
    travel: TanzaniaTravelData
    documents: TanzaniaDocumentData


class EmploymentStatus(Enum):
    Employed = "עובד"
    Independent = "עצמאי"
    Soldier = "חייל"
    Student = "סטודנט"
    Retired = "פנסיונר"
    Other = "לא עובד / אחר"
