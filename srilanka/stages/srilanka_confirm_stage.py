from typing import List

from processing.common.variable import Variable
from processing.srilanka.stages.abstract.srilanka_template_stage import SriLankaTemplateStage
from processing.srilanka.util_types import SriLankaPayloadData, SriLankaVisaTemplates


class SriLankaConfirmStage(SriLankaTemplateStage):
    template = SriLankaVisaTemplates.Confirm

    def get_variables(self, data: SriLankaPayloadData) -> List[Variable]:
        return []
