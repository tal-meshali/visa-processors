import os
from abc import abstractmethod, ABCMeta
from enum import EnumMeta, Enum
from typing import TypeVar


class ABCEnumMeta(EnumMeta, ABCMeta):
    pass


class StageEnum(Enum, metaclass=ABCEnumMeta):
    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    def value(self) -> str:
        return self.base_url + super().value


class TemplateEnum(Enum, metaclass=ABCEnumMeta):
    @property
    @abstractmethod
    def base_path(self):
        pass

    @property
    def value(self) -> str:
        return os.path.join(os.getcwd(), 'templates', str(super().value) + ".json")


TPayloadData = TypeVar("TPayloadData")
TStage = TypeVar("TStage", bound=StageEnum)
TTemplate = TypeVar("TTemplate", bound=TemplateEnum)
