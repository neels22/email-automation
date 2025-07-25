# Gmail Email Monitor with Slack Notifications

A Python application that monitors your Gmail inbox for unread emails and sends categorized notifications to a Slack channel using an incoming webhook. The script organizes emails by subject, posts a summary to Slack, and marks them as read to avoid duplicate alerts.

## Features

- ✅ **Gmail API Integration**: Secure OAuth 2.0 authentication (no IMAP required)
- ✅ **Email Categorization**: Automatically sorts emails into categories based on subject keywords
- ✅ **Slack Notifications**: Sends formatted alerts to a Slack channel via webhook
- ✅ **Environment Variables**: Uses `.env` for secure configuration
- ✅ **Auto Mark as Read**: Prevents duplicate notifications by marking emails as read after processing
- ✅ **Simple Setup**: Minimal configuration required

## How It Works

1. **Authenticate with Gmail**: Uses OAuth 2.0 to access your Gmail inbox securely.
2. **Fetch Unread Emails**: Looks for unread emails received in the last 24 hours.
3. **Categorize Emails**: Analyzes the subject line to assign a category (e.g., Banking, Job Applications, Security, etc.).
4. **Send Slack Notification**: Posts a summary (category, sender, subject, snippet) to your chosen Slack channel.
5. **Mark as Read**: Marks the email as read in Gmail to avoid duplicate notifications.

## Example Slack Notification

```
*💰 Banking / Payments*
*From:* ICICI Bank
*Subject:* Your account balance update
Your account balance is INR 10,000 as of today...
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd email-automation
pip install -r requirements.txt
```

### 2. Enable Gmail API in Google Cloud Console

Follow the same steps as in the WhatsApp section below to enable the Gmail API and download your `credentials.json` file.

### 3. Create a Slack Incoming Webhook

1. Go to your Slack workspace and open [Slack API: Incoming Webhooks](https://api.slack.com/messaging/webhooks).
2. Click "Create a Slack App" (or use an existing app).
3. Add the "Incoming Webhooks" feature and activate it.
4. Click "Add New Webhook to Workspace" and select the channel you want notifications sent to.
5. Copy the generated Webhook URL.

### 4. Configure Environment Variables

1. Create a `.env` file in your project root (or update it if it exists):

```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url
```

2. Ensure your `.env` file is **not** committed to version control.

### 5. Run the Slack Bot

```bash
python slack.py
```

- On first run, a browser window will open for Gmail authentication.
- Grant access to your Gmail account.
- The script will check for unread emails, send notifications to Slack, and mark them as read.

## Email Categorization

The bot uses keywords in the subject line to assign categories, such as:

- 💰 Banking / Payments: invoice, payment, balance, credit, icici, mab
- 🧾 Offers / Details: offer, details
- 💼 Job Applications: application, applied, submission, recruit, careers, applying
- 🧪 Assessments / Tests: assessment, coding, test, codesignal, hackerrank
- 🗓️ Interviews / Events: interview, invite, session, meeting, event, call
- 🔒 Security / Account: security, password, verify, account, login, unauthorized
- 📬 Subscriptions / News: digest, newsletter, updates, substack, thread
- 🧮 Rejections: unfortunately, decline, rejected, not moving forward, another candidate
- 🪪 Misc / General: Anything else

## Code Overview

- `gmail_auth()`: Handles Gmail OAuth 2.0 authentication
- `list_unread_messages()`: Fetches unread email IDs from the last 24 hours
- `get_message_details()`: Extracts sender, subject, and a snippet of the body
- `categorize_email()`: Assigns a category based on subject keywords
- `send_slack_notification()`: Sends a formatted message to Slack
- `mark_as_read()`: Marks the email as read in Gmail
- `process_message()`: Orchestrates the above steps for each email
- `main()`: Entry point for the script

## Troubleshooting

- **Missing credentials.json**: Download from Google Cloud Console and place in project root.
- **Missing SLACK_WEBHOOK_URL**: Create a Slack webhook and add it to your `.env` file.
- **Gmail API authentication failed**: Delete `token.json` and re-run the script to re-authenticate.
- **No notifications in Slack**: Double-check your webhook URL and Slack channel permissions.

---

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

---

## Real-World Troubleshooting Examples

### 1. Error 403: access_denied during OAuth

**Symptom:**
```
Error 403: access_denied
Request details: ...
```

**Cause:**
- The Google account you are using is not added as a test user in the OAuth consent screen, or the OAuth consent screen is not fully configured.
- You may be using the wrong OAuth client type (should be Desktop application).

**How to Fix:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **APIs & Services > OAuth consent screen**.
3. Fill out all required fields (App name, support email, etc.).
4. Under **Test users**, add the email address you use to log in during the OAuth flow.
5. Save and retry authentication.
6. Ensure your OAuth client is of type **Desktop application**.
7. If you see an "unverified app" warning, click "Advanced" and proceed (safe for personal use).

### 2. Gmail API has not been used in project ... or it is disabled

**Symptom:**
```
❌ Error fetching unread messages: <HttpError 403 when requesting https://gmail.googleapis.com/gmail/v1/users/me/messages?q=is%3Aunread&alt=json returned "Gmail API has not been used in project ... before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=... then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.". Details: ...>
```

**Cause:**
- The Gmail API is not enabled for your Google Cloud project, or you just enabled it and the change hasn't propagated yet.

**How to Fix:**
1. Visit the link provided in the error message, or go to [Gmail API enable page](https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=YOUR_PROJECT_ID) (replace `YOUR_PROJECT_ID` with your project number).
2. Click the **Enable** button.
3. Wait a minute or two for the change to propagate.
4. Re-run your script.

**Tip:** If you enabled the API just now and still see the error, wait a few minutes and try again.

---

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