from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, Dict

from models.orm import Beneficiary
from processing.common.data_classes import PassportData
from processing.common.util_types import TPayloadData


class Translator(Generic[TPayloadData], ABC):
    EMAIL = 'moredite1@gmail.com'

    def __init__(self, beneficiary: Beneficiary):
        self.beneficiary = {**beneficiary.to_dict(), "id": beneficiary.id}

    @staticmethod
    def _convert_passport_data(passport_data: Dict) -> PassportData:
        kwargs = {k: datetime.strptime(v, '%d/%m/%Y') if k.startswith('date') else v for k, v in passport_data.items()
                  if not k.startswith("code_section")}
        return PassportData(**kwargs)

    @abstractmethod
    def convert(self) -> TPayloadData:
        pass
