from datetime import datetime
from typing import List, Dict, TypeVar, Generic

T = TypeVar("T")


class Variable(Generic[T]):
    def __init__(self, path: List[str], value: T):
        self.path = path
        self.value = value

    def _process_value(self):
        return self.value

    def _handle(self, data_to_update: Dict, path: List[str]):
        field_name = path[0]
        if len(path) > 1:
            return self._handle(data_to_update[field_name], path[1:])

        data_to_update[field_name] = self._process_value()

    def handle(self, data_to_update: Dict):
        self._handle(data_to_update, self.path)


class MimicVariable(Generic[T], Variable[T]):
    def __init__(self, path: List[str], variable: Variable[T]):
        super().__init__(path, variable._process_value())
        self.variable = variable

    def handle(self, data_to_update: Dict):
        super().handle(data_to_update)
        self.variable.handle(data_to_update)


class DateVariable(Variable[datetime]):
    def __init__(self, *args, format_str: str = "%d/%m/%Y"):
        super().__init__(*args)
        self.format_str = format_str

    def _process_value(self):
        return self.value.strftime(self.format_str)


class ISODateVariable(Variable[datetime]):
    def _process_value(self):
        return f"{self.value.isoformat()}.000Z"
