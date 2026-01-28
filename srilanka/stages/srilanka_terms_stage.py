from typing import List

from common.variable import Variable
from srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from srilanka.util_types import SriLankaVisaTemplates, SriLankaPayloadData


class SriLankaTermsStage(SriLankaTemplateStage):
    template = SriLankaVisaTemplates.Terms

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        return []
