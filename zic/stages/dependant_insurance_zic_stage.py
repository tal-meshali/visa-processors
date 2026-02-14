from typing import List

from common.stages.template_stage import EVisaTemplateStage
from common.variable import Variable, DateVariable
from tazania.util_types import TanzaniaPayloadData
from zic.util_types import ZICInsuranceTemplates, ArrivalSplashData


class DependantInsuranceZICStage(EVisaTemplateStage[TanzaniaPayloadData, ZICInsuranceTemplates]):
    template = ZICInsuranceTemplates.Dependant

    def __init__(self, arrival_splash_data: ArrivalSplashData):
        self.arrival_splash_data = arrival_splash_data

    def get_variables(self, data: TanzaniaPayloadData) -> List[Variable]:
        return [
            Variable(['first_name'], data.passport.first_name),
            Variable(['last_name'], data.passport.last_name),
            Variable(['birth_place'], data.passport.place_of_birth),
            Variable(['passport'], data.passport.passport_number),
            DateVariable(['birth_date'], data.contact.phone_number, format_str="%Y-%m-%d"),
            Variable(['email'], data.contact.email_address),
            Variable(['telephone'], data.contact.phone_number),
            Variable(['nationality'], self.arrival_splash_data.nationalities[data.passport.nationality.lower()]),
            Variable(['gender'], self.arrival_splash_data.genders['male' if data.passport.sex == 'M' else 'female'])
        ]
