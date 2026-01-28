from abc import ABC
from typing import Dict

from processing.common.stages.template_stage import EVisaTemplateStage
from processing.tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from processing.tazania.util_types import TanzaniaPayloadData, TanzaniaVisaTemplates


class TanzaniaTemplateStage(BaseTanzaniaEVisaStage,
                            EVisaTemplateStage[TanzaniaPayloadData, TanzaniaVisaTemplates], ABC):
    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return self.process_template(data)
