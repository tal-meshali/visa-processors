from abc import ABC

from common.stages.evisa_stage import BaseEVisaStage
from zic.util_types import ZICInsurancePayloadData, ZICInsuranceStages


class BaseZICStage(BaseEVisaStage[ZICInsurancePayloadData, ZICInsuranceStages], ABC):
    data_key = "data"
