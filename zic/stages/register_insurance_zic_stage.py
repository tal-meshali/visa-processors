from typing import Dict, List

from requests import Session

from common.stages.template_stage import EVisaTemplateStage
from common.variable import Variable, DateVariable
from tazania.util_types import TanzaniaPayloadData
from zic.captcha import crack_captcha
from zic.stages.abstract.base_zic_stage import BaseZICStage
from zic.stages.dependant_insurance_zic_stage import DependantInsuranceZICStage
from zic.util_methods import handle_arrivals_splash, get_insurance_type
from zic.util_types import ZICInsurancePayloadData, ZICInsuranceTemplates, ArrivalSplashData, ZICInsuranceStages


class RegisterInsuranceZICStage(BaseZICStage, EVisaTemplateStage[ZICInsurancePayloadData, ZICInsuranceTemplates]):
    template = ZICInsuranceTemplates.Register
    stage = ZICInsuranceStages.Register
    arrival_splash_data: ArrivalSplashData

    def handle(self, session: Session, data: ZICInsurancePayloadData):
        print(f"Started handling {self.stage.name}")
        self.arrival_splash_data = handle_arrivals_splash(session)
        processed_data = self.process_data(data)
        processed_data['captcha'] = crack_captcha(session)
        processed_files = self.process_files(data)
        response = self.post_data(session, processed_data, files=processed_files)
        print(response.json())

    def get_dependants(self, initial_passport_number, data: ZICInsurancePayloadData):
        dependant_stage = DependantInsuranceZICStage(self.arrival_splash_data)
        dependants = []

        for beneficiary in data:
            if beneficiary.passport.passport_number == initial_passport_number:
                continue

            dependants.append(dependant_stage.process_template(beneficiary))

        return dependants

    def get_variables(self, data: ZICInsurancePayloadData) -> List[Variable]:
        oldest_beneficiary: TanzaniaPayloadData = min(data,
                                                      key=lambda beneficiary: beneficiary.passport_data.date_of_birth)
        return [
            Variable(['txt_first_name'], oldest_beneficiary.passport.first_name),
            Variable(['txt_last_name'], oldest_beneficiary.passport.last_name),
            Variable(['txt_passport'], oldest_beneficiary.passport.passport_number),
            Variable(['txt_birth_place'], oldest_beneficiary.passport.place_of_birth),
            Variable(['email'], oldest_beneficiary.contact.email_address),
            Variable(['mobile_number'], oldest_beneficiary.contact.phone_number),
            DateVariable(['dat_birth_date'], oldest_beneficiary.passport.date_of_birth, format_str="%Y-%m-%d"),
            DateVariable(['dat_arrival_date'], oldest_beneficiary.travel.date_of_arrival, format_str="%Y-%m-%d"),
            DateVariable(['dat_departure_date'], oldest_beneficiary.travel.date_of_departure, format_str="%Y-%m-%d"),
            Variable(['gender'], self.arrival_splash_data.genders['male' if oldest_beneficiary.passport.sex == 'M' else 'female']),
            DateVariable(['txt_insurance'], get_insurance_type(len(data), self.arrival_splash_data.insurance_types)),
            Variable(['int_has_dependants'], int(len(data) > 1))
        ]

    def process_data(self, data: ZICInsurancePayloadData) -> Dict:
        result = self.process_template(data)
        result['dependants'] = self.get_dependants(result['txt_passport'], data)

        return result
