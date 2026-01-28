from datetime import datetime
from dataclasses import dataclass


@dataclass
class PassportData:
    first_name: str
    last_name: str
    passport_number: str
    place_of_birth: str
    date_of_birth: datetime
    date_of_issue: datetime
    date_of_expiry: datetime
    sex: str  # M / F
    nationality: str
    issuing_country = "ISRAEL"


@dataclass
class ContactData:
    phone_number: str
    email_address: str


@dataclass
class EmploymentData:
    employment_status: str = None
    employer_name: str = None
    occupation: str = None


@dataclass
class TravelData:
    date_of_arrival: datetime
    date_of_departure: datetime


@dataclass
class DocumentData:
    portrait_path: str
    passport_path: str
