import dataclasses
from typing import Dict, List

from common.util_types import StageEnum, TemplateEnum
from tazania.util_types import TanzaniaPayloadData


@dataclasses.dataclass
class ArrivalSplashData:
    insurance_types: List[Dict]
    nationalities: Dict[str, str]
    countries: Dict[str, str]
    relationship_types: Dict[str, str]
    travel_purpose: Dict[str, str]
    genders: Dict[str, str]


class ZICInsuranceStages(StageEnum):
    ArrivalsSplash = "arrival/arrivals_splash"
    GetCaptcha = "captcha/get_captcha"
    Register = "arrival/register_insurance"

    @property
    def base_url(self):
        return "https://inbound.visitzanzibar.go.tz/api/"


class ZICInsuranceTemplates(TemplateEnum):
    Register = "register"
    Dependant = "dependant"

    @property
    def base_path(self):
        return "./zic/templates"


ZICInsurancePayloadData = List[TanzaniaPayloadData]
