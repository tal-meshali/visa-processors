from typing import Dict

from processing.common.util_types import TPayloadData
from processing.srilanka.stages.abstract.base_srilanka_stage import BaseSriLankaEVisaStage
from processing.srilanka.util_types import SriLankaVisaStages


class SriLankaInitialStage(BaseSriLankaEVisaStage):
    stage = SriLankaVisaStages.Initial

    def process_data(self, data: TPayloadData) -> Dict:
        return {
            "locale": "en_US"
        }
