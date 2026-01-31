import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, Dict, Optional

from google.cloud import firestore
from common.data_classes import PassportData
from common.util_types import TPayloadData


class Translator(Generic[TPayloadData], ABC):
    EMAIl = 'admin@visa-kal.co.il'

    @staticmethod
    def _format_datetime(date_string, date_format='%Y-%m-%d'):
        return datetime.strptime(date_string, date_format)

    @staticmethod
    def _convert_passport_data(passport_data: Dict) -> PassportData:
        kwargs = {k: Translator._format_datetime(v) if k.startswith('date') else v for k, v in
                  passport_data.items()
                  if not k.startswith("code_section")}
        return PassportData(**kwargs)

    @abstractmethod
    def convert(self, form_data: Dict) -> TPayloadData:
        pass
