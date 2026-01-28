from abc import ABC, abstractmethod
from typing import List, Generic

from requests import Session

from processing.common.stages.evisa_stage import BaseEVisaStage
from processing.common.util_types import TPayloadData, TStage


class EVisaPipeline(Generic[TPayloadData, TStage], ABC):
    def __init__(self):
        self.stages = self._get_stages()

    @abstractmethod
    def _get_stages(self) -> List[BaseEVisaStage[TPayloadData, TStage]]:
        pass

    def run(self, data: TPayloadData):
        session = Session()
        for stage in self.stages:
            stage.handle(session, data)
