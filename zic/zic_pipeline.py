from typing import List

from common.pipeline import MultiEVisaPipeline
from common.stages.evisa_stage import BaseEVisaStage
from tazania.util_types import TanzaniaPayloadData
from zic.stages.register_insurance_zic_stage import RegisterInsuranceZICStage
from zic.util_types import ZICInsurancePayloadData, ZICInsuranceStages


class ZICInsurancePipeline(MultiEVisaPipeline[TanzaniaPayloadData, ZICInsuranceStages]):
    def _get_stages(self) -> List[BaseEVisaStage[ZICInsurancePayloadData, ZICInsuranceStages]]:
        return [
            RegisterInsuranceZICStage(),
        ]
