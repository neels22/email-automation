# Gmail Email Monitor with WhatsApp Alerts

A Python application that monitors your Gmail for unread emails and sends WhatsApp notifications via Twilio. The script categorizes emails based on subject content and marks them as read after processing.

## Features

- ✅ **Gmail API Integration**: OAuth 2.0 authentication (no IMAP needed)
- ✅ **Email Categorization**: Automatically categorizes emails based on subject keywords
- ✅ **WhatsApp Notifications**: Sends formatted alerts via Twilio WhatsApp API
- ✅ **Secure Configuration**: Uses `.env` file for credentials
- ✅ **Auto Mark as Read**: Prevents duplicate notifications
- ✅ **Modular Design**: Clean, maintainable code structure

## Project Structure

```
email_alert/
├── main.py              # Main application script
├── .env                 # Environment variables (you create this)
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── credentials.json    # Google API credentials (you download this)
└── token.json          # OAuth token (auto-generated)
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd email-automation
pip install -r requirements.txt
```

### 2. Enable Gmail API in Google Cloud Console

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a New Project** (or select existing):
   - Click "Select a project" → "New Project"
   - Name: "Gmail Monitor" (or your choice)
   - Click "Create"

3. **Enable Gmail API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Gmail API" → "Enable"

4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - Choose "External" → "Create"
     - Fill required fields (App name, User support email, Developer email)
     - Save and continue through all steps
   - Back to "Create OAuth client ID":
     - Application type: "Desktop application"
     - Name: "Gmail Monitor"
     - Click "Create"

5. **Download Credentials**:
   - Click the download button (⬇️) next to your newly created OAuth client
   - Save the file as `credentials.json` in your project directory

### 3. Set Up Twilio WhatsApp

1. **Create Twilio Account**: https://www.twilio.com/try-twilio
2. **Get Account Credentials**:
   - Go to Twilio Console Dashboard
   - Note your Account SID and Auth Token
3. **Set Up WhatsApp Sandbox** (for testing):
   - Go to "Messaging" → "Try it out" → "Send a WhatsApp message"
   - Follow instructions to connect your WhatsApp to the sandbox
   - Note the sandbox number (e.g., `+14155238886`)

### 4. Configure Environment Variables

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials**:
   ```env
   # Twilio Configuration
   TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here
   
   # WhatsApp Numbers (must include whatsapp: prefix)
   TWILIO_FROM=whatsapp:+14155238886  # Your Twilio sandbox number
   TWILIO_TO=whatsapp:+1234567890     # Your WhatsApp number (with country code)
   ```

### 5. Run the Application

```bash
python main.py
```

**First Run:**
- A browser window will open for Gmail authentication
- Sign in with your Google account
- Grant permissions to read and modify Gmail
- The `token.json` file will be created automatically

## How It Works

### Email Categorization

The script categorizes emails based on subject content:

- 💰 **Invoice**: Subject contains "invoice"
- 💼 **Job**: Subject contains "job" 
- 📧 **General**: All other emails

### WhatsApp Message Format

```
🚨 *New Email Alert*

📂 *Category:* 💰 Invoice
👤 *From:* billing@company.com
📝 *Subject:* Invoice #12345 - Payment Due

---
_Sent by Gmail Monitor_
```

### Code Structure

- `gmail_auth()`: Handles OAuth 2.0 authentication
- `list_unread_messages()`: Fetches unread email IDs
- `get_message_details()`: Extracts From/Subject headers
- `categorize_email()`: Categorizes based on subject
- `send_whatsapp_notification()`: Sends Twilio WhatsApp message
- `mark_as_read()`: Marks email as read
- `process_message()`: Orchestrates the entire flow

## Usage Examples

### Basic Usage
```bash
python main.py
```

### Sample Output
```
🚀 Starting Gmail Email Monitor...
✅ Gmail API authentication successful
📧 Found 3 unread messages

📨 Processing message: 18c1f2b3d4e5f6g7
   From: billing@company.com
   Subject: Invoice #12345 - Payment Due
   Category: 💰 Invoice
✅ WhatsApp sent: SM1234567890abcdef
✅ Marked message 18c1f2b3d4e5f6g7 as read

📊 Summary:
   ✅ Successfully processed: 3
   ❌ Failed to process: 0
   📧 Total messages: 3

🎉 Gmail monitoring completed!
```

## Troubleshooting

### Common Issues

1. **"credentials.json file not found"**
   - Download OAuth credentials from Google Cloud Console
   - Place the file in the project root directory

2. **"Twilio credentials not configured"**
   - Check your `.env` file exists and has correct values
   - Ensure WhatsApp numbers include `whatsapp:` prefix

3. **"Gmail API authentication failed"**
   - Delete `token.json` and re-run to re-authenticate
   - Check Gmail API is enabled in Google Cloud Console

4. **WhatsApp not receiving messages**
   - Verify you've joined the Twilio WhatsApp sandbox
   - Check your phone number format includes country code
   - Ensure `whatsapp:` prefix is included in `.env`

### Security Notes

- Never commit `credentials.json`, `token.json`, or `.env` files to version control
- Add these files to your `.gitignore`
- Use strong, unique passwords for your Google and Twilio accounts
- Regularly rotate your Twilio Auth Token

## Customization

### Adding New Categories

Edit the `categorize_email()` function in `main.py`:

```python
def categorize_email(subject: str) -> str:
    subject_lower = subject.lower()
    
    if 'invoice' in subject_lower:
        return '💰 Invoice'
    elif 'job' in subject_lower:
        return '💼 Job'
    elif 'urgent' in subject_lower:
        return '🚨 Urgent'
    elif 'newsletter' in subject_lower:
        return '📰 Newsletter'
    else:
        return '📧 General'
```

### Filtering Specific Senders

Modify the Gmail query in `list_unread_messages()`:

```python
# Only emails from specific domain
results = service.users().messages().list(
    userId='me', 
    q='is:unread from:important-company.com'
).execute()
```

### Scheduling with Cron

Add to your crontab to run every 15 minutes:
```bash
crontab -e
# Add this line:
*/15 * * * * cd /path/to/email-automation && python main.py
```

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the Twilio and Google API documentation
3. Create an issue in this repository with detailed error messages