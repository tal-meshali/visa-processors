from abc import ABC
from typing import Dict

from common.stages.template_stage import EVisaTemplateStage
from morocco.stages.abstract.morocco_evisa_stage import BaseMoroccoEVisaStage
from morocco.util_types import MoroccoPayloadData, MoroccoVisaTemplates


class MoroccoTemplateStage(BaseMoroccoEVisaStage,
                           EVisaTemplateStage[MoroccoPayloadData, MoroccoVisaTemplates], ABC):
    def process_data(self, data: MoroccoPayloadData) -> Dict:
        return self.process_template(data)
