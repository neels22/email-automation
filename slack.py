#!/usr/bin/env python3
"""
Gmail Email Monitor with Slack Notifications

Monitors Gmail for unread emails and sends categorized notifications
to a Slack channel using an incoming webhook.
"""

import os
import time
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']

# Slack webhook URL
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def gmail_auth() -> Optional[object]:
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        if not creds:
            if not os.path.exists('credentials.json'):
                print("❌ Missing credentials.json!")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)
        print("✅ Gmail API authentication successful")
        return service
    except HttpError as error:
        print(f"❌ Gmail API authentication failed: {error}")
        return None

def list_unread_messages(service) -> List[str]:
    now = int(time.time())
    since = now - 24 * 60 * 60
    query = f'is:unread after:{since}'
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        print(f"📬 Found {len(messages)} unread messages in the last 24 hours")
        return [msg['id'] for msg in messages]
    except HttpError as error:
        print(f"❌ Error fetching unread messages: {error}")
        return []

def get_message_details(service, message_id: str) -> Dict[str, str]:
    try:
        message = service.users().messages().get(
            userId='me', 
            id=message_id, 
            format='full'
        ).execute()

        headers = message['payload'].get('headers', [])
        email_data = {'from': '', 'subject': '', 'body': '', 'id': message_id}

        for header in headers:
            name = header['name'].lower()
            if name == 'from':
                email_data['from'] = header['value']
            elif name == 'subject':
                email_data['subject'] = header['value']

        # Parse body
        def get_body(payload):
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        return part['body'].get('data', '')
                    elif part['mimeType'].startswith("multipart"):
                        nested = get_body(part)
                        if nested:
                            return nested
            elif payload['mimeType'] == 'text/plain':
                return payload['body'].get('data', '')
            return ''

        body_encoded = get_body(message['payload'])
        if body_encoded:
            import base64
            from html import unescape
            decoded_bytes = base64.urlsafe_b64decode(body_encoded.encode('UTF-8'))
            decoded_str = decoded_bytes.decode('UTF-8', errors='ignore')
            email_data['body'] = unescape(decoded_str.strip())

        return email_data

    except HttpError as error:
        print(f"❌ Error fetching message details: {error}")
        return {'from': '', 'subject': '', 'body': '', 'id': message_id}

def categorize_email(subject: str) -> str:
    subject = subject.lower()
    if any(w in subject for w in ['invoice', 'payment', 'balance', 'credit', 'icici', 'mab']):
        return '💰 Banking / Payments'
    if any(w in subject for w in ['job offer', 'offer details', 'details for']):
        return '🧾 Offers / Details'
    if any(w in subject for w in ['application', 'applied', 'submission', 'recruit', 'thank you for applying']):
        return '💼 Job Applications'
    if any(w in subject for w in ['assessment', 'coding', 'test', 'code signal']):
        return '🧪 Assessments / Tests'
    if any(w in subject for w in ['interview', 'session', 'invite', 'meeting', 'event']):
        return '🗓️ Interviews / Events'
    if any(w in subject for w in ['security', 'password', 'verify', 'account', 'login']):
        return '🔒 Security / Account'
    if any(w in subject for w in ['digest', 'newsletter', 'updates', 'substack', 'new thread']):
        return '📬 Subscriptions / News'
    if any(w in subject for w in ['unfortunately', 'not moving forward', 'decline', 'rejected']):
        return '🧮 Rejections'
    return '🪪 Misc / General'

def send_slack_notification(email_data: Dict[str, str]) -> bool:
    category = categorize_email(email_data['subject'])
    snippet = email_data['body'][:300] + "..." if email_data['body'] else "(No body)"

    message = (
        f"*📬 New Email Alert*\n"
        f"*From:* {email_data['from']}\n"
        f"*Subject:* {email_data['subject']}\n"
        f"*Category:* {category}\n"
        f"*Body Preview:*\n```{snippet}```"
    )

    payload = {"text": message}

    try:
        res = requests.post(SLACK_WEBHOOK_URL, json=payload)
        print(f"📲 Slack message sent ({res.status_code}): {email_data['subject']}")
        return res.ok
    except Exception as e:
        print(f"❌ Error sending Slack notification: {e}")
        return False

def mark_as_read(service, message_id: str) -> bool:
    try:
        service.users().messages().modify(
            userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}
        ).execute()
        print(f"✅ Marked as read: {message_id}")
        return True
    except HttpError as error:
        print(f"❌ Error marking message read: {error}")
        return False

def process_message(service, message_id: str) -> bool:
    print(f"\n🔍 Processing message {message_id}")
    email_data = get_message_details(service, message_id)
    if not email_data['subject']:
        print("⚠️ No subject found. Skipping.")
        return False
    if send_slack_notification(email_data):
        return mark_as_read(service, message_id)
    return False

def main():
    print("🚀 Starting Gmail monitor with Slack...")
    service = gmail_auth()
    if not service:
        return
    message_ids = list_unread_messages(service)
    if not message_ids:
        print("✅ No new emails.")
        return
    success = 0
    for msg_id in message_ids:
        if process_message(service, msg_id):
            success += 1
    print(f"\n📊 Done. {success}/{len(message_ids)} processed.")

if __name__ == "__main__":
    main()
