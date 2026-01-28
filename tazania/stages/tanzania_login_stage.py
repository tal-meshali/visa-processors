from typing import List

from processing.common.variable import Variable
from processing.tazania.stages.abstract.tanzania_recaptcha_stage import BaseTanzaniaReCaptchaStage
from processing.tazania.stages.abstract.tanzania_template_stage import TanzaniaTemplateStage
from processing.tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData, TanzaniaVisaTemplates


class TanzaniaLoginStage(BaseTanzaniaReCaptchaStage, TanzaniaTemplateStage):
    stage = TanzaniaVisaStages.Start
    template = TanzaniaVisaTemplates.Start

    def get_variables(self, data: TanzaniaPayloadData) -> List[Variable]:
        return [Variable(['Email'], data.contact.email_address),
                Variable(["PassportNumber"], data.passport.passport_number)]
