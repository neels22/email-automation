#!/usr/bin/env python3
"""
Gmail Email Monitor with WhatsApp Alerts via Twilio

This script monitors Gmail for unread emails and sends WhatsApp notifications
via Twilio with email categorization based on subject content.
"""

import os
import pickle
from typing import List, Dict, Optional
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from twilio.rest import Client
import base64
import email
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']

# Twilio configuration
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')  # Twilio WhatsApp number (format: whatsapp:+1234567890)
TWILIO_TO = os.getenv('TWILIO_TO')      # Your WhatsApp number (format: whatsapp:+1234567890)

def gmail_auth() -> Optional[object]:
    """
    Authenticate with Gmail API using OAuth 2.0.
    
    Returns:
        Gmail service object or None if authentication fails
    """
    creds = None
    
    # Check if token.json exists with saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists('credentials.json'):
                print("Error: credentials.json file not found!")
                print("Please download it from Google Cloud Console and place it in this directory.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
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
    """
    Get list of unread message IDs from Gmail.
    
    Args:
        service: Gmail API service object
        
    Returns:
        List of message IDs
    """
    try:
        results = service.users().messages().list(
            userId='me', 
            q='is:unread'
        ).execute()
        
        messages = results.get('messages', [])
        message_ids = [msg['id'] for msg in messages]
        
        print(f"📧 Found {len(message_ids)} unread messages")
        return message_ids
        
    except HttpError as error:
        print(f"❌ Error fetching unread messages: {error}")
        return []

def get_message_details(service, message_id: str) -> Dict[str, str]:
    """
    Get email details including From, Subject headers.
    
    Args:
        service: Gmail API service object
        message_id: Gmail message ID
        
    Returns:
        Dictionary with email details
    """
    try:
        message = service.users().messages().get(
            userId='me', 
            id=message_id,
            format='metadata',
            metadataHeaders=['From', 'Subject']
        ).execute()
        
        headers = message['payload'].get('headers', [])
        email_data = {'from': '', 'subject': '', 'id': message_id}
        
        for header in headers:
            name = header['name'].lower()
            if name == 'from':
                email_data['from'] = header['value']
            elif name == 'subject':
                email_data['subject'] = header['value']
        
        return email_data
        
    except HttpError as error:
        print(f"❌ Error fetching message details for {message_id}: {error}")
        return {'from': '', 'subject': '', 'id': message_id}

def categorize_email(subject: str) -> str:
    """
    Categorize email based on subject content.
    
    Args:
        subject: Email subject line
        
    Returns:
        Category string
    """
    subject_lower = subject.lower()
    
    if 'invoice' in subject_lower:
        return '💰 Invoice'
    elif 'job' in subject_lower:
        return '💼 Job'
    else:
        return '📧 General'

def send_whatsapp_notification(email_data: Dict[str, str]) -> bool:
    """
    Send WhatsApp notification via Twilio.
    
    Args:
        email_data: Dictionary containing email details
        
    Returns:
        True if sent successfully, False otherwise
    """
    if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO]):
        print("❌ Twilio credentials not configured properly")
        return False
    
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        
        category = categorize_email(email_data['subject'])
        
        message_body = f"""🚨 *New Email Alert*

📂 *Category:* {category}
👤 *From:* {email_data['from']}
📝 *Subject:* {email_data['subject']}

---
_Sent by Gmail Monitor_"""
        
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        
        print(f"✅ WhatsApp sent: {message.sid}")
        return True
        
    except Exception as error:
        print(f"❌ Error sending WhatsApp: {error}")
        return False

def mark_as_read(service, message_id: str) -> bool:
    """
    Mark email as read in Gmail.
    
    Args:
        service: Gmail API service object
        message_id: Gmail message ID
        
    Returns:
        True if marked successfully, False otherwise
    """
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()
        
        print(f"✅ Marked message {message_id} as read")
        return True
        
    except HttpError as error:
        print(f"❌ Error marking message as read: {error}")
        return False

def process_message(service, message_id: str) -> bool:
    """
    Process a single email message: get details, send notification, mark as read.
    
    Args:
        service: Gmail API service object
        message_id: Gmail message ID
        
    Returns:
        True if processed successfully, False otherwise
    """
    print(f"\n📨 Processing message: {message_id}")
    
    # Get email details
    email_data = get_message_details(service, message_id)
    
    if not email_data['from'] and not email_data['subject']:
        print("⚠️ Could not fetch email details, skipping...")
        return False
    
    print(f"   From: {email_data['from']}")
    print(f"   Subject: {email_data['subject']}")
    print(f"   Category: {categorize_email(email_data['subject'])}")
    
    # Send WhatsApp notification
    if send_whatsapp_notification(email_data):
        # Only mark as read if notification was sent successfully
        return mark_as_read(service, message_id)
    else:
        print("⚠️ Skipping mark as read due to notification failure")
        return False

def main():
    """
    Main function to monitor Gmail and send WhatsApp alerts.
    """
    print("🚀 Starting Gmail Email Monitor...")
    
    # Validate Twilio configuration
    if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO]):
        print("❌ Error: Twilio configuration incomplete!")
        print("Please check your .env file for TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO")
        return
    
    # Authenticate with Gmail
    service = gmail_auth()
    if not service:
        print("❌ Gmail authentication failed. Exiting.")
        return
    
    # Get unread messages
    message_ids = list_unread_messages(service)
    
    if not message_ids:
        print("✅ No unread messages found. Nothing to process.")
        return
    
    # Process each message
    processed_count = 0
    failed_count = 0
    
    for message_id in message_ids:
        if process_message(service, message_id):
            processed_count += 1
        else:
            failed_count += 1
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   ✅ Successfully processed: {processed_count}")
    print(f"   ❌ Failed to process: {failed_count}")
    print(f"   📧 Total messages: {len(message_ids)}")
    
    print("\n🎉 Gmail monitoring completed!")

if __name__ == "__main__":
    main() 