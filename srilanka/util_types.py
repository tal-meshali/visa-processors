from dataclasses import dataclass

from processing.common.data_classes import PassportData, ContactData, TravelData
from processing.common.util_types import StageEnum, TemplateEnum


class SriLankaVisaStages(StageEnum):
    Initial = 'slvisa/visainfo/apply.jsp'
    Request = 'etaslvisa/etaNavServ'

    @property
    def base_url(self):
        return "https://eta.gov.lk/"


class SriLankaVisaTemplates(TemplateEnum):
    Contact = "contact"
    Confirm = "confirm"
    Terms = 'terms'
    Create = 'create'

    @property
    def base_path(self):
        return "./templates"


@dataclass
class SriLankaContactData(ContactData):
    city: str
    address: str


@dataclass
class SriLankaTravelData(TravelData):
    country_resided_in: str = "ISR"


@dataclass
class SriLankaRequestData:
    amount_of_days: int


@dataclass
class SriLankaPayloadData:
    passport: PassportData
    contact: SriLankaContactData
    travel: SriLankaTravelData
    request: SriLankaRequestData
