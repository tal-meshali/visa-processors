from common.data_classes import PassportData, ContactData, DocumentData, EmploymentData, TravelData
from dataclasses import dataclass
from common.util_types import StageEnum, TemplateEnum


class MoroccoVisaStages(StageEnum):
    Login = "auth/api/login"
    GetRequest = 'api/api/demandeEvisa/dossierEVisa'
    InitiateBeneficiary = "api/api/conditionEvise/recherche/en"
    UpdateBeneficiary = "api/api/demandeEvisa/dossierDemandeEVisa"
    UploadDocuments = "api/api/v1"
    SubmitDocuments = "api/api/v1/checkRequiredAttEvisa/en"

    @property
    def base_url(self):
        return "https://api.acces-maroc.ma/"


class MoroccoVisaTemplates(TemplateEnum):
    Blob = "blob"
    Initial = "beneficiary_initial_request"
    Insert = "beneficiary_update_details"

    @property
    def base_path(self):
        return "./templates"


@dataclass
class RequestPayloadData:
    request_id: str
    beneficiary_id: str = None
    token: str = None


@dataclass
class MoroccoPayloadData:
    passport: PassportData
    contact: ContactData
    request: RequestPayloadData
    employment: EmploymentData
    travel: TravelData
    documents: DocumentData
