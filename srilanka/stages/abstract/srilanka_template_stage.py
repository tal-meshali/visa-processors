from abc import ABC
from typing import Dict

from common.stages.template_stage import EVisaTemplateStage
from srilanka.stages.abstract.base_srilanka_stage import BaseSriLankaEVisaStage
from srilanka.util_types import SriLankaPayloadData, SriLankaVisaTemplates, SriLankaVisaStages


class SriLankaTemplateStage(BaseSriLankaEVisaStage,
                            EVisaTemplateStage[SriLankaPayloadData, SriLankaVisaTemplates], ABC):
    stage = SriLankaVisaStages.Request

    def process_data(self, data: SriLankaPayloadData) -> Dict:
        return self.process_template(data)
