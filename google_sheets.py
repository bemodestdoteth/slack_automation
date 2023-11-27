from loguru import logger
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import get_variables, setup_logger, LOGFILE

import os
import time

setup_logger(logfile=LOGFILE)

def build_creds():
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", ['https://www.googleapis.com/auth/spreadsheets'])
        if not creds or not creds.valid: # If there are no (valid) credentials available, let the user log in.
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", ['https://www.googleapis.com/auth/spreadsheets']
                )
                creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token: # Save the credentials for the next run
            token.write(creds.to_json())

        logger.info("Credentials built")
        return creds
    except Exception as e:
        logger.error(e)
        raise Exception(e)
def check_data(data):
    if 'messages' not in data or 'replies' not in data:
        return False
    return True
def verify_data(creds, data_range, data_to_verify, retries=10):
    try:
        time.sleep(3)
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(
                spreadsheetId=get_variables('google_spreadsheet_id'),
                range=data_range
            )
            .execute()
        )
        values = result.get("values", [])

        # Compare the retrieved data with the original data
        result = values[-len(data_to_verify):] == data_to_verify
        logger.info(f"Data verified: {result}")

        if not result and retries > 0:
            logger.warning(f"Retrying verification. Retries left: {retries}")
            return verify_data(creds, data_range, data_to_verify, retries-1)
        elif not result and retries == 0:
            logger.error("Verification failed")
            return False

        return result
    except HttpError as e:
        logger.error(e)
        return False
def write_data(data):
    try:
        if not check_data(data):
            raise Exception("Data is not in the correct format")

        creds = build_creds()
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API to write data
        sheet = service.spreadsheets()

        message_sheet_range = f"{get_variables('google_spreadsheet_message_sheet_name')}!B2:G"
        sheet.values().append(
            spreadsheetId=get_variables('google_spreadsheet_id'),
            range=message_sheet_range, 
            valueInputOption="USER_ENTERED",
            body={"values": data['messages']}
        ).execute()

        if not verify_data(creds, message_sheet_range, data['messages']):
            raise Exception("Data was not written to sheet")
        logger.success("Meesage Data written to sheet")

        reply_sheet_range = f"{get_variables('google_spreadsheet_reply_sheet_name')}!B3:H"
        sheet.values().append(
            spreadsheetId=get_variables('google_spreadsheet_id'),
            range=reply_sheet_range, 
            valueInputOption="USER_ENTERED",
            body={"values": data['replies']}
        ).execute()

        if not verify_data(creds, reply_sheet_range, data['replies']):
            raise Exception("Data was not written to sheet")
        logger.success("Meesage Data written to sheet")

        logger.success("Reply Data written to sheet")
        logger.success("Data written to sheet successfully")
    except HttpError as e:
        logger.error(e)

if __name__ == "__main__":
  build_creds()