from typing import List

from common.variable import Variable
from srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from srilanka.util_types import SriLankaPayloadData, SriLankaVisaTemplates


class SriLankaConfirmStage(SriLankaTemplateStage):
    template = SriLankaVisaTemplates.Confirm

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        return []
