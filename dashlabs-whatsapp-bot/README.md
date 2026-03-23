# Dash Labs WhatsApp Bot

WhatsApp chatbot for Dash Labs — automates lead capture, quote requests, call booking, and FAQs via the WhatsApp Cloud API.

## Features

- **New Project Enquiry** — 7-step lead capture (service, name, business, budget, timeline, details)
- **Get a Quote** — Collect requirements, promise custom quote
- **Book a Call** — Collect preferred day + time slot
- **Services** — Explain each of the 9 services
- **Portfolio** — Share work samples
- **FAQ** — Turnaround, process, payments, support, revisions
- **Status Check** — Existing clients can check project status
- **Admin Notifications** — WhatsApp + email alerts for every new lead

## Tech Stack

- Python 3.9+ / FastAPI
- WhatsApp Cloud API (Meta)
- SQLite (via aiosqlite + SQLAlchemy)
- Button-driven flows (no AI/NLP required)

## Setup

### 1. Clone and install

```bash
cd dashlabs-whatsapp-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your actual values
```

### 3. Set up Meta WhatsApp Cloud API

1. Go to [developers.facebook.com](https://developers.facebook.com) and create an app
2. Add the **WhatsApp** product
3. In WhatsApp > Getting Started, note your **Phone Number ID** and **Access Token**
4. Generate a permanent **System User Token** from Business Settings
5. Add these to your `.env`:
   - `WHATSAPP_TOKEN` — your system user token
   - `WHATSAPP_PHONE_NUMBER_ID` — your phone number ID
   - `VERIFY_TOKEN` — any string you choose

### 4. Run locally

```bash
python3 scripts/init_db.py
uvicorn app.main:app --reload
```

### 5. Set up webhook (for local testing)

```bash
# In a separate terminal
ngrok http 8000
```

Then in the Meta Developer Console:
1. Go to WhatsApp > Configuration > Webhook
2. Set Callback URL to `https://your-ngrok-url.ngrok.io/webhook`
3. Set Verify Token to match your `VERIFY_TOKEN`
4. Subscribe to **messages** field

### 6. Test it

Send "hi" to your WhatsApp Business number — you should get the main menu.

## Deployment

### Railway / Render

Just push the repo. The `Procfile` is included.

### VPS (DigitalOcean, etc.)

```bash
# Run with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Use systemd + nginx + certbot for production HTTPS
```

Meta requires an HTTPS webhook URL (e.g., `https://bot.dashlabs.co.in/webhook`).

## Project Structure

```
app/
├── main.py              # FastAPI app entry point
├── config.py            # Environment settings
├── database.py          # SQLite async engine
├── models.py            # Lead, Conversation, Message models
├── whatsapp/
│   ├── webhook.py       # Webhook verify + incoming messages
│   ├── sender.py        # send_text(), send_buttons(), send_list()
│   └── templates.py     # All message content and button IDs
├── flows/
│   ├── router.py        # Central message dispatcher
│   ├── main_menu.py     # Welcome menu
│   ├── new_enquiry.py   # 7-step lead capture
│   ├── get_quote.py     # Quote request flow
│   ├── book_call.py     # Call booking flow
│   ├── services.py      # Service explainer
│   ├── portfolio.py     # Work samples
│   ├── faq.py           # FAQs
│   └── status_check.py  # Project status lookup
├── services/
│   ├── lead_service.py          # Lead CRUD
│   ├── conversation_service.py  # State management
│   └── notification_service.py  # Admin alerts
└── utils/
    └── helpers.py       # Phone formatting, etc.
```
