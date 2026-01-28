from typing import Dict

from processing.tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from processing.tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData


class TanzaniaDeclarationStage(BaseTanzaniaEVisaStage):
    stage = TanzaniaVisaStages.Declaration

    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return {"Declaration": ""}
