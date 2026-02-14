from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Generic

from flask import abort
from google.cloud import firestore

from common.pipeline import MultiEVisaPipeline, TPipeline
from common.util_types import TStage, TPayloadData


@dataclass(frozen=True)
class ControllerResult:
    request_id: str
    processed_count: int
    status: str
    results: List[Dict[str, Any]]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "processed_count": self.processed_count,
            "status": self.status,
            "results": self.results,
        }


class BaseController(Generic[TPipeline]):
    def __init__(
            self,
            firestore_client: firestore.Client,
            bucket_name: str,
            pipeline: TPipeline,
    ) -> None:
        self._firestore = firestore_client
        self._bucket_name = bucket_name
        self.pipeline = pipeline

    def get_beneficiaries(self, request_id: str):
        request_doc = self._firestore.collection("requests").document(request_id).get()
        if not request_doc.exists:
            raise abort(404, f"Request with ID: {request_id} hasn't been found!")

        return self._firestore.collection("beneficiaries").where("request_id", "==", request_id).stream()

    def process_request(self, request_id: str) -> ControllerResult:
        beneficiaries = self.get_beneficiaries(request_id)

        results: List[Dict[str, Any]] = []
        status = "success"

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
                status = 'error'

        return ControllerResult(
            request_id=request_id,
            processed_count=len(results),
            status=status,
            results=results,
        )


class MultiController(Generic[TPayloadData, TStage], BaseController[MultiEVisaPipeline[List[TPayloadData], TStage]]):

    def process_request(self, request_id: str) -> ControllerResult:
        beneficiaries = self.get_beneficiaries(request_id)

        results: List[Dict[str, Any]] = []

        request_form_data = []

        for idx, beneficiary_doc in enumerate(beneficiaries):
            beneficiary_data = beneficiary_doc.to_dict() or {}
            form_data = beneficiary_data.get("form_data", {}) or {}
            request_form_data.append(form_data)

        status = "success"
        try:
            self.pipeline.run(request_form_data)
        except Exception as e:
            status = "error"
            results.append(
                {"request_id": request_id, "status": "error", "error": str(e)}
            )

        return ControllerResult(
            request_id=request_id,
            processed_count=len(results),
            status=status,
            results=results
        )
