from typing import List

from common.util_types import TPayloadData
from common.variable import Variable, MimicVariable
from tazania.stages.abstract.tanzania_template_stage import TanzaniaTemplateStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaVisaTemplates
from tazania.variables import TanzaniaDateVariable, TanzaniaOptionsVariable


class TanzaniaPersonalInfoStage(TanzaniaTemplateStage):
    stage = TanzaniaVisaStages.PersonalInfo
    template = TanzaniaVisaTemplates.PersonalInfo

    def get_variables(self, data: TPayloadData) -> List[Variable]:
        return [
            Variable(["Firstname"], data.passport.first_name),
            Variable(["Surname"], data.passport.last_name),
            Variable(["GenderID"], 1 if data.passport.sex == "M" else 2),
            TanzaniaDateVariable([""], data.passport.date_of_birth),
            MimicVariable(["BirthNationalityId"],
                          TanzaniaOptionsVariable(["BirthCountryID"], data.passport.place_of_birth, self.document)),

            Variable(["BirthCity"], data.contact.physical_address_city),
            TanzaniaOptionsVariable(["MaritalStatusID"], data.personal.marital_status, self.document),
            TanzaniaOptionsVariable(["CurrentNationalityID"], data.passport.nationality, self.document)
        ]
