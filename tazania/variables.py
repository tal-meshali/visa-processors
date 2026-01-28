from datetime import datetime
from typing import Dict, Callable, List

from bs4 import BeautifulSoup

from processing.common.variable import Variable


class TanzaniaOptionsVariable(Variable[str]):
    def __init__(self, path: List[str], value: str, document: BeautifulSoup, **kwargs):
        super().__init__(path, value)
        self.document = document

    def _process_value(self):
        return {
            tag.getText(): tag.get("value")
            for tag in self.document.find(attrs={"name": self.path[-1]}).findAll("option")
        }[self.value]


class TanzaniaDatePartVariable(Variable[datetime]):
    def __init__(self, action: Callable[[datetime], str], *args):
        super().__init__(*args)
        self.action = action

    def _process_value(self):
        return self.action(self.value)


class TanzaniaDateVariable(Variable[datetime]):
    def _add_suffix(self, suffix: str):
        return [*self.path[:-1], self.path[-1] + suffix]

    def handle(self, data_to_update: Dict):
        variables = [
            TanzaniaDatePartVariable(lambda d: d.day, self._add_suffix("Day"), self.value),
            TanzaniaDatePartVariable(lambda d: d.month, self._add_suffix("Month"), self.value),
            TanzaniaDatePartVariable(lambda d: d.year, self._add_suffix("Year"), self.value)
        ]
        for variable in variables:
            variable.handle(data_to_update)
