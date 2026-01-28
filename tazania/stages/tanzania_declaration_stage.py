from typing import Dict

from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData


class TanzaniaDeclarationStage(BaseTanzaniaEVisaStage):
    stage = TanzaniaVisaStages.Declaration

    def process_data(self, data: TanzaniaPayloadData) -> Dict:
        return {"Declaration": ""}
