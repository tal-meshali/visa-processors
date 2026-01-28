from typing import List

from processing.common.variable import Variable
from processing.srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from processing.srilanka.util_types import SriLankaVisaTemplates, SriLankaPayloadData


class SriLankaTermsStage(SriLankaTemplateStage):
    template = SriLankaVisaTemplates.Terms

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        return []
