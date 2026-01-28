from typing import List

from processing.common.variable import Variable
from processing.tazania.stages.abstract.tanzania_template_stage import TanzaniaTemplateStage
from processing.tazania.util_types import TanzaniaVisaTemplates, TanzaniaPayloadData, TanzaniaVisaStages
from processing.tazania.variables import TanzaniaOptionsVariable, TanzaniaDateVariable


class TanzaniaPassportInfoStage(TanzaniaTemplateStage):
    stage = TanzaniaVisaStages.PassportInfo
    template = TanzaniaVisaTemplates.PassportInfo

    def get_variables(self, data: TanzaniaPayloadData) -> List[Variable]:
        return [
            Variable(['PassportNumber'], data.passport.passport_number),
            Variable(['City'], data.passport.issuing_country),
            TanzaniaOptionsVariable(["IssuedCountryID"], data.passport.issuing_country, self.document),
            TanzaniaDateVariable(['Issue'], data.passport.date_of_issue),
            TanzaniaDateVariable(['Expiry'], data.passport.date_of_expiry),
        ]
