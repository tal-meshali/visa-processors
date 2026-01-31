import os

import firebase_admin
import functions_framework
from firebase_admin import auth, credentials
from flask import Request, abort
from google.cloud import firestore

from controllers.controllers import MoroccoController, TanzaniaController

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    # Try to get credentials from environment or use default
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        # Use default credentials (for Cloud Run / GCP environments)
        firebase_admin.initialize_app()


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
def process_request(request: Request):
    auth_header = None
    if request:
        auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Authentication required - missing or invalid authorization header")

    token = auth_header.split("Bearer ")[1]

    try:
        auth.verify_id_token(token)
    except Exception as e:
        abort(500, f"Failed to authenticate: {e}")

    controller = country_to_controller[request.json['country']](firestore_client=_FIRESTORE, bucket_name=_BUCKET_NAME)
    return controller.process_request(request.json['request_id']).as_dict()
