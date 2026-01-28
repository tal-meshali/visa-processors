from abc import ABC
from typing import Dict

from common.stages.template_stage import EVisaTemplateStage
from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from tazania.util_types import TanzaniaPayloadData, TanzaniaVisaTemplates


class TanzaniaTemplateStage(BaseTanzaniaEVisaStage,
                            EVisaTemplateStage[TanzaniaPayloadData, TanzaniaVisaTemplates], ABC):
    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return self.process_template(data)
