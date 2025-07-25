# ⏰ Automating with Cron on macOS

This guide explains how to automatically run the `slack.py` script every 5 minutes using `cron` on macOS.

---

## 🧾 Purpose

- Automatically check Gmail for unread emails every 5 minutes
- Categorize and send Slack notifications
- Run even when you're not at the computer (as long as Mac is awake)

---

## 🛠 Setup Instructions

### ✅ Step 1: Move Project Folder Off Desktop

macOS protects Desktop, Documents, and Downloads from cron access.

Move your folder to a safe location:

```bash
mkdir -p ~/scripts
mv ~/Desktop/email-automation ~/scripts/
```

---

### ✅ Step 2: Create a Bash Wrapper Script

Create `run_notifier.sh` in the project directory:

```bash
#!/bin/bash
cd /Users/indraneelsarode/scripts/email-automation
source ./myenv/bin/activate
./myenv/bin/python slack.py
```

Then make it executable:

```bash
chmod +x /Users/indraneelsarode/scripts/email-automation/run_notifier.sh
```

---

### ✅ Step 3: Edit Your Crontab

Open crontab:

```bash
crontab -e
```

Add this line to run every 5 minutes:

```cron
*/5 * * * * /bin/bash /Users/indraneelsarode/scripts/email-automation/run_notifier.sh >> /Users/indraneelsarode/scripts/email-automation/slack.log 2>&1
```

This:

* Runs the notifier script
* Appends all output to `slack.log`

---

### ✅ Step 4: Give Full Disk Access (Important)

Go to:

> **System Settings → Privacy & Security → Full Disk Access**

Enable:

* Terminal
* `/bin/bash`
* Python from your virtual environment (e.g., `/Users/indraneelsarode/scripts/email-automation/myenv/bin/python`)

---

## 🧪 Troubleshooting

### ❌ `Operation not permitted`

**Fix**: Grant Full Disk Access and avoid Desktop/Documents

---

### ❌ `Missing credentials.json!`

**Fix**: Add `cd` to the script so it runs in the correct directory

---

### ❌ `ModuleNotFoundError: No module named 'google.auth'`

**Fix**: Make sure you're using the virtual environment's Python

---

## ✅ Status

Once cron is set up:

* Script runs silently every 5 minutes
* Logs go to `slack.log`
* Slack messages are sent for new unread emails

You can monitor it with:

```bash
tail -f ~/scripts/email-automation/slack.log
```

---

## 💤 Note About Sleep

* If your Mac is asleep, cron won't run
* Use `caffeinate` to keep it awake:

```bash
caffeinate -i -t 3600   # Stay awake for 1 hour
```

---

## 📌 Tip

To test immediately without waiting:

```bash
/bin/bash ~/scripts/email-automation/run_notifier.sh
```
