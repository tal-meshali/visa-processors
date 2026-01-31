import os

import functions_framework
from flask import Request
from google.cloud import firestore

from controllers.controllers import MoroccoController, TanzaniaController


def get_firestore_client() -> firestore.Client:
    """Initialize and return Firestore client"""
    project_id = os.getenv("GCP_PROJECT_ID")
    database_id = os.getenv("FIRESTORE_DATABASE")

    return firestore.Client(
        project=project_id,
        database=database_id
    )


_FIRESTORE = get_firestore_client()
_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

country_to_controller = {
    "morocco": MoroccoController,
    "tanzania": TanzaniaController
}


@functions_framework.http
async def process_request(request: Request):
    controller = country_to_controller[request.json['country']](firestore_client=_FIRESTORE, bucket_name=_BUCKET_NAME)
    return controller.process_request(request.json['request_id']).as_dict()
