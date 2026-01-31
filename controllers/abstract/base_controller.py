from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Generic

from google.cloud import firestore

from common.pipeline import EVisaPipeline
from common.util_types import TStage, TPayloadData


class RequestNotFoundError(Exception):
    def __init__(self, request_id: str):
        super().__init__(f"Request {request_id} not found")
        self.request_id = request_id


@dataclass(frozen=True)
class ControllerResult:
    request_id: str
    processed_count: int
    results: List[Dict[str, Any]]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "processed_count": self.processed_count,
            "results": self.results,
        }


class BaseController(Generic[TPayloadData, TStage]):
    def __init__(
            self,
            *,
            firestore_client: firestore.Client,
            bucket_name: str,
            pipeline: EVisaPipeline[TPayloadData, TStage],
    ) -> None:
        self._firestore = firestore_client
        self._bucket_name = bucket_name
        self.pipeline = pipeline

    def process_request(self, request_id: str) -> ControllerResult:
        request_doc = self._firestore.collection("requests").document(request_id).get()
        if not request_doc.exists:
            raise RequestNotFoundError(request_id)

        beneficiaries = (
            self._firestore.collection("beneficiaries")
            .where("request_id", "==", request_id)
            .stream()
        )

        results: List[Dict[str, Any]] = []

        for idx, beneficiary_doc in enumerate(beneficiaries):
            beneficiary_data = beneficiary_doc.to_dict() or {}
            form_data = beneficiary_data.get("form_data", {}) or {}

            try:
                self.pipeline.run(form_data)
                results.append({"beneficiary_id": beneficiary_doc.id, "status": "success"})
            except Exception as e:
                results.append(
                    {"beneficiary_id": beneficiary_doc.id, "status": "error", "error": str(e)}
                )

        return ControllerResult(
            request_id=request_id,
            processed_count=len(results),
            results=results,
        )
