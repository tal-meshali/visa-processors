import datetime
import os
from abc import ABC
from mimetypes import guess_type
from typing import Dict

from bs4 import BeautifulSoup
from tazania.stages.abstract.base_tanzania_stage import BaseTanzaniaEVisaStage


class TanzaniaDataProcessStage(BaseTanzaniaEVisaStage, ABC):

    @staticmethod
    def extend_with_option_value(
            result: Dict, document: BeautifulSoup, field: str, value: str
    ) -> None:
        result[field] = {
            tag.getText(): tag.get("value")
            for tag in document.find(attrs={"name": field}).findAll("option")
        }[value]

    @staticmethod
    def extend_with_date_fields(
            result: Dict, value: datetime.datetime, prefix=""
    ) -> None:
        result[f"{prefix}Day"] = value.day
        result[f"{prefix}Month"] = value.month
        result[f"{prefix}Year"] = value.year

    @staticmethod
    def process_file(field_name: str, path: str, result: Dict):
        name = os.path.basename(path)
        with open(path, "rb") as f:
            result[field_name] = (os.path.basename(path), f.read(), guess_type(name)[0])
