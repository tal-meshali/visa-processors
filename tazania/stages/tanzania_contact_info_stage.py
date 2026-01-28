from typing import Dict, List

from common.variable import Variable, MimicVariable
from tazania.stages.abstract.tanzania_template_stage import TanzaniaTemplateStage
from tazania.util_methods import get_employment_type, get_employment_data
from tazania.util_types import TanzaniaPayloadData, TanzaniaVisaStages, TanzaniaVisaTemplates
from tazania.variables import TanzaniaOptionsVariable


class TanzaniaContactInfoStage(TanzaniaTemplateStage):
    stage = TanzaniaVisaStages.ContactInfo
    template = TanzaniaVisaTemplates.ContactInfo

    def get_variables(self, data: TanzaniaPayloadData) -> List[Variable]:
        return [
            Variable(['MobileNo'], data.contact.phone_number),
            Variable(['Email'], data.contact.email_address),
            MimicVariable(["PermanentAddress"],
                          Variable(["PresentAddress"], data.contact.physical_address)),
            MimicVariable(["PermanentCountryID"],
                          TanzaniaOptionsVariable(["PresentCountryID"], data.contact.physical_address_country,
                                                  self.document)),
            # Unbelievable
            MimicVariable(["PermanetCity"],
                          Variable(["PresentCity"], data.contact.physical_address_city)),
            TanzaniaOptionsVariable(["EmploymentStatusID"], get_employment_type(data), self.document)
        ]

    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        processed_data = super().process_data(data)
        processed_data.update(get_employment_data(data))
        return processed_data
