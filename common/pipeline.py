from abc import ABC, abstractmethod
from typing import List, Generic, Dict, TypeVar

from requests import Session

from common.stages.evisa_stage import BaseEVisaStage
from common.translator import Translator
from common.util_types import TPayloadData, TStage


class EVisaPipeline(Generic[TPayloadData, TStage], ABC):
    def __init__(self, translator: Translator[TPayloadData]):
        self.stages = self._get_stages()
        self.translator = translator

    @abstractmethod
    def _get_stages(self) -> List[BaseEVisaStage[TPayloadData, TStage]]:
        pass

    def run(self, form_data: Dict) -> TPayloadData:
        data = self.translator.convert(form_data)
        session = Session()
        for stage in self.stages:
            stage.handle(session, data)

        return data


class MultiEVisaPipeline(EVisaPipeline[TPayloadData, TStage], ABC):
    def run(self, form_data: List[Dict]) -> List[TPayloadData]:
        data = [self.translator.convert(beneficiary) for beneficiary in form_data]
        session = Session()
        for stage in self.stages:
            stage.handle(session, data)

        return data


TPipeline = TypeVar("TPipeline", bound=EVisaPipeline)
