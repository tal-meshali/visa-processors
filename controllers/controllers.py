from __future__ import annotations

from google.cloud import firestore

from common.pipeline import EVisaPipeline
from controllers.abstract.base_controller import BaseController, MultiController
from morocco.morocco_pipeline import MoroccoEVisaPipeline
from morocco.util_types import MoroccoVisaStages, MoroccoPayloadData
from tazania.tanzania_pipeline import TanzaniaEVisaPipeline
from tazania.tanzania_translator import TanzaniaTranslator
from tazania.util_types import TanzaniaVisaStages, TanzaniaPayloadData
from zic.util_types import ZICInsuranceStages
from zic.zic_pipeline import ZICInsurancePipeline


class MoroccoController(BaseController[EVisaPipeline[MoroccoPayloadData, MoroccoVisaStages]]):
    def __init__(self, firestore_client: firestore.Client, bucket_name: str) -> None:
        super().__init__(
            firestore_client=firestore_client,
            bucket_name=bucket_name,
            pipeline=MoroccoEVisaPipeline(),
        )


class TanzaniaController(BaseController[EVisaPipeline[TanzaniaPayloadData, TanzaniaVisaStages]]):
    def __init__(self, firestore_client: firestore.Client, bucket_name: str) -> None:
        super().__init__(
            firestore_client=firestore_client,
            bucket_name=bucket_name,
            pipeline=TanzaniaEVisaPipeline(TanzaniaTranslator()),
        )


class ZICController(MultiController[TanzaniaPayloadData, ZICInsuranceStages]):
    def __init__(self, firestore_client: firestore.Client, bucket_name: str) -> None:
        super().__init__(
            firestore_client=firestore_client,
            bucket_name=bucket_name,
            pipeline=ZICInsurancePipeline(TanzaniaTranslator()),
        )
