from abc import ABC
from typing import Dict

from processing.common.stages.template_stage import EVisaTemplateStage
from processing.srilanka.stages.abstract.base_srilanka_stage import BaseSriLankaEVisaStage
from processing.srilanka.util_types import SriLankaPayloadData, SriLankaVisaTemplates, SriLankaVisaStages


class SriLankaTemplateStage(BaseSriLankaEVisaStage,
                            EVisaTemplateStage[SriLankaPayloadData, SriLankaVisaTemplates], ABC):
    stage = SriLankaVisaStages.Request

    def process_data(self, data: SriLankaPayloadData) -> Dict:
        return self.process_template(data)
