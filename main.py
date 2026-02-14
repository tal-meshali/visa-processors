import os
import json

import firebase_admin
import functions_framework
from firebase_admin import auth, credentials
from flask import Request, abort, jsonify
from google.cloud import firestore

from controllers.controllers import MoroccoController, TanzaniaController, ZICController

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
    "tanzania": TanzaniaController,
    "zanzibar": ZICController
}


@functions_framework.http
def main(request: Request):
    """
    Main entry point for Cloud Run service.
    Routes requests based on path.
    """

    # Route to payme_callback if path matches
    if '/payme-callback' in request.path:
        return process_request(request)
    else:
        return process_request(request)
        # return process_request(request)


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


def payme_callback(request: Request):
    """
    PayMe callback endpoint that receives payment status updates.
    This endpoint is called by PayMe after payment completion.
    Updates the request status based on payment result.
    """
    if request.method != "POST":
        abort(405, "Method not allowed")

    try:
        # Parse request data - PayMe may send JSON or form data
        if request.is_json:
            data = request.get_json()
            print("DATA1", data)
        else:
            # Try to parse as form data
            data = request.form.to_dict()
            print("DATA2", data)
            # If form data, try to parse JSON strings
            for key, value in data.items():
                if isinstance(value, str):
                    try:
                        data[key] = json.loads(value)
                    except (json.JSONDecodeError, ValueError):
                        pass

        # Extract transaction_id (which we sent as reference/request_id)
        transaction_id = data.get("transaction_id") or data.get("sale_id") or data.get("reference")
        
        # Extract payment status
        # PayMe typically sends status codes: 0 = success, 1 = failed
        # Or status strings like "success", "failed", "completed", "cancelled"
        status_code = data.get("status_code")
        status_text = data.get("status") or data.get("payment_status")
        
        # Determine if payment succeeded
        payment_succeeded = False
        if status_code == 0:
            payment_succeeded = True
        elif status_code == 1:
            payment_succeeded = False
        elif status_text:
            status_lower = str(status_text).lower()
            payment_succeeded = status_lower in ["success", "completed", "paid", "approved"]
        
        if not transaction_id:
            abort(400, "Missing transaction_id/reference in callback data")

        # Update request status in Firestore
        requests_ref = _FIRESTORE.collection("requests")
        request_doc = requests_ref.document(transaction_id).get()
        
        if not request_doc.exists:
            abort(404, f"Request not found: {transaction_id}")

        # Update status based on payment result
        new_status = "payment_received" if payment_succeeded else "payment_failed"
        
        requests_ref.document(transaction_id).update({
            "status": new_status,
            "updated_at": firestore.SERVER_TIMESTAMP
        })

        # Return success response to PayMe
        return jsonify({
            "status": "success",
            "message": f"Request status updated to {new_status}",
            "request_id": transaction_id
        }), 200

    except Exception as e:
        # Log error but return 200 to PayMe to prevent retries
        print(f"Error processing PayMe callback: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 200


if __name__ == '__main__':
    controller = MoroccoController(firestore_client=_FIRESTORE, bucket_name=_BUCKET_NAME)
    controller.process_request("CvHNV0dX6uyjxdHRVyvu").as_dict()