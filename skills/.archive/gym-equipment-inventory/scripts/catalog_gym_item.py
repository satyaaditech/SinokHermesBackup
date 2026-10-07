#!/usr/bin/env python3
"""
Helper script to upload gym photo to Google Drive and append structured record to Google Sheets.
Includes automatic randomized jitter to prevent rate-limiting and over-processing flags.
"""

import sys
import time
import random
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_PATH = '/home/satyaaditech/.hermes/google_token.json'
DRIVE_FOLDER_ID = '1Ec3XHJW6k8MYc3dyOvtxL7m1wRgbzyFa'
SPREADSHEET_ID = '1NAkd3IOOx_gNDeKPXOHI3gSQSHleW6q8pyDmBubdHVo'
SHEET_TAB = 'Daftar Alat Gym'

def get_services():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    drive = build('drive', 'v3', credentials=creds)
    sheets = build('sheets', 'v4', credentials=creds)
    return drive, sheets

def upload_photo(drive, local_path, destination_filename):
    file_metadata = {
        'name': destination_filename,
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(local_path, mimetype='image/jpeg', resumable=True)
    uploaded = drive.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink, webContentLink'
    ).execute()
    file_id = uploaded.get('id')
    # Grant read permission so Google Sheets =IMAGE() can fetch thumbnail
    try:
        drive.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()
    except Exception as e:
        print(f"Warning setting permission on {file_id}: {e}")
    return uploaded

def append_to_sheet(sheets, row_data):
    body = {
        'values': [row_data]
    }
    result = sheets.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{SHEET_TAB}'!A:I",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    return result

def safe_delay(min_sec=45, max_sec=110):
    jitter = random.randint(min_sec, max_sec)
    print(f"Applying safe random jitter: {jitter}s...")
    time.sleep(jitter)
