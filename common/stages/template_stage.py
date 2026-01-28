import json
from abc import abstractmethod
from typing import Generic, Dict, List
from processing.common.util_types import TPayloadData, TTemplate
from processing.common.variable import Variable


class EVisaTemplateStage(Generic[TPayloadData, TTemplate]):
    template: TTemplate

    def process_template(self, data: TPayloadData) -> Dict:
        variables = self.get_variables(data)
        with open(self.template.value, 'rb') as template:
            template_obj = json.load(template)
            for variable in variables:
                variable.handle(template_obj)

            return template_obj

    @abstractmethod
    def get_variables(self, data: TPayloadData) -> List[Variable]:
        pass
