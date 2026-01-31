"""
Module for extracting visa request IDs from Gmail and managing them in Google Sheets.
"""
import base64
import os
import re
from datetime import datetime
from typing import Optional

import google
import gspread
import requests
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build

from morocco.stages.abstract.morocco_evisa_stage import MOROCCO_USER_AGENT

# Constants
URL_REGEX = re.compile(r'https://www\.acces-maroc\.ma/#/e-visa/formulaire\?token=([\w-]+)')
SHEET_URL = "https://docs.google.com/spreadsheets/d/1VF10FboDqj-GtoIjuVppkpaaH1RNQAYwewcZ60oeQ00/"
EMAIL_ADDRESS = "admin@visa-kal.co.il"
API_ENDPOINT = "https://api.acces-maroc.ma/api/api/demandeEvisa/sendMail"
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class VisaRequestIdExtractor:
    """
    Handles extraction of visa request IDs from Gmail and management in Google Sheets.
    """

    def __init__(
            self,
            service_account_path: Optional[str] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    ):
        """
        Initialize the extractor with Google API credentials.

        Args:
            service_account_path: Path to Google service account credentials JSON file (for Sheets)
        """
        self.service_account_path = service_account_path
        self._gmail_service = None
        self._sheet_client = None

    def _get_gmail_service(self):
        """Get or create Gmail API service instance using OAuth2 user credentials."""
        if self._gmail_service is None:
            creds = None

            # Try to load existing token
            if self.service_account_path:
                try:
                    creds = ServiceAccountCredentials.from_service_account_file(
                        self.service_account_path, scopes=GMAIL_SCOPES
                    ).with_subject(EMAIL_ADDRESS)
                except Exception:
                    pass

            self._gmail_service = build('gmail', 'v1', credentials=creds)
        return self._gmail_service

    def _get_sheet_client(self):
        """Get or create Google Sheets client instance using service account."""
        if self._sheet_client is None:
            if not self.service_account_path:
                try:
                    # In Cloud Run, service account should already be configured.
                    creds, project = google.auth.default(scopes=SHEETS_SCOPES)
                except Exception:
                    raise ValueError(
                        "Service account path required for Google Sheets access. "
                        "Please provide service_account_path."
                    )
            else:
                creds = ServiceAccountCredentials.from_service_account_file(
                    self.service_account_path, scopes=SHEETS_SCOPES
                )
            self._sheet_client = gspread.authorize(creds)
        return self._sheet_client

    def get_new_url(self) -> int:
        """
        Request a new visa URL by sending an email request.

        Returns:
            HTTP response status code
        """
        payload = {
            "confirmMail": EMAIL_ADDRESS,
            "mail": EMAIL_ADDRESS,
        }

        response = requests.post(
            API_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json", "User-Agent": MOROCCO_USER_AGENT},
            timeout=30.0
        )

        return response.status_code

    def extract_and_append_email_data(self) -> None:
        """
        Extract visa request URLs from Gmail emails and append them to Google Sheets.
        Only processes emails that haven't been added yet based on the latest date in the sheet.
        """
        gmail_service = self._get_gmail_service()
        sheet_client = self._get_sheet_client()

        # Open the spreadsheet
        spreadsheet = sheet_client.open_by_url(SHEET_URL)
        worksheet = spreadsheet.sheet1

        # Build search query
        search_query = "from:(noreply@maec.gov.ma) subject:(Complete your eVisa)"

        # Add date filter if there are existing rows
        if date_values := worksheet.col_values(2):
            actual_dates = [datetime.fromisoformat(date_value) for date_value in date_values]
            search_query += f" after:{int(max(actual_dates).timestamp())}"

        # Search for emails
        results = gmail_service.users().messages().list(
            userId='me', q=search_query
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return

        # Get full message details and sort by date
        message_details = []
        for msg in messages:
            message = gmail_service.users().messages().get(
                userId='me', id=msg['id'], format='full'
            ).execute()
            message_details.append(message)

        # Sort messages by date (internalDate)
        message_details.sort(key=lambda m: int(m.get('internalDate', 0)))

        # Extract URLs and append to sheet
        for message in message_details:
            payload = message['payload']
            while payload['body']['size'] == 0:
                payload = payload['parts'][0]
            body_data = payload['body']['data']
            body_text = base64.urlsafe_b64decode(body_data).decode('utf-8')
            # If HTML, extract text content (simple approach - regex works on HTML too)
            url_match = URL_REGEX.search(body_text)

            if url_match:
                token = url_match.group(1)
                response = requests.post("https://api.acces-maroc.ma/api/api/demandeEvisa/checkToken",
                                         headers={"Content-Type": "application/json", "User-Agent": MOROCCO_USER_AGENT},
                                         json={'token': token})
                message_date = datetime.fromtimestamp(
                    int(message.get('internalDate', 0)) / 1000
                ).isoformat()

                worksheet.append_row([response.json()['numeroDossier'], message_date, False])

    def get_and_remove_request_id(self) -> Optional[str]:
        """
        Get the first unprocessed request ID from the sheet, remove it from the sheet,
        and return it.

        Returns:
            The visa request URL (token) if found, None otherwise
        """
        sheet_client = self._get_sheet_client()
        spreadsheet = sheet_client.open_by_url(SHEET_URL)
        worksheet = spreadsheet.sheet1

        # Get first unused code row index
        row_index = next(i for i, value in enumerate(worksheet.col_values(3)) if value == 'FALSE') + 1
        code = worksheet.row_values(row_index)[0]

        # Mark as used
        worksheet.update_cell(row_index, 3, "TRUE")

        return code

    def update_known_request_code(self, old_request_code, request_code, firebase_request_id):
        sheet_client = self._get_sheet_client()
        spreadsheet = sheet_client.open_by_url(SHEET_URL)
        worksheet = spreadsheet.sheet1

        # Get matching to UNKNOWN code
        row_index = next(i for i, value in enumerate(worksheet.col_values(1)) if value == old_request_code) + 1
        code = worksheet.row_values(row_index)[0]

        # Update the new one to keep track
        worksheet.update_cell(row_index, 3, "TRUE")


if __name__ == '__main__':
    print(VisaRequestIdExtractor().get_and_remove_request_id())
