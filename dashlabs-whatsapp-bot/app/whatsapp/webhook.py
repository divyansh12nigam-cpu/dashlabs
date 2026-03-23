"""WhatsApp webhook endpoints — verification and incoming messages."""
import logging

from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.flows.router import route_message
from app.services.conversation_service import log_message

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/webhook")
async def verify_webhook(request: Request):
    """Meta webhook verification challenge."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return PlainTextResponse(content=challenge, status_code=200)

    logger.warning("Webhook verification failed")
    return PlainTextResponse(content="Forbidden", status_code=403)


@router.post("/webhook")
async def handle_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Handle incoming WhatsApp messages."""
    body = await request.json()

    entries = body.get("entry", [])
    if not entries:
        return {"status": "ok"}

    changes = entries[0].get("changes", [])
    if not changes:
        return {"status": "ok"}

    value = changes[0].get("value", {})

    # Only process actual messages, not status updates
    messages = value.get("messages")
    if not messages:
        return {"status": "ok"}

    message = messages[0]
    phone = message.get("from", "")
    msg_id = message.get("id", "")
    msg_type = message.get("type", "")

    # Dedup: check if we already processed this message
    if msg_id and await log_message(db, phone, "inbound", msg_type, "", msg_id):
        logger.info("Duplicate message %s, skipping", msg_id)
        return {"status": "ok"}

    # Extract message content based on type
    text = ""
    reply_id = ""

    if msg_type == "text":
        text = message.get("text", {}).get("body", "")
    elif msg_type == "interactive":
        interactive = message.get("interactive", {})
        reply_type = interactive.get("type", "")
        if reply_type == "button_reply":
            reply_id = interactive.get("button_reply", {}).get("id", "")
            text = interactive.get("button_reply", {}).get("title", "")
        elif reply_type == "list_reply":
            reply_id = interactive.get("list_reply", {}).get("id", "")
            text = interactive.get("list_reply", {}).get("title", "")
    else:
        # Unsupported message type (image, audio, etc.) — send to main menu
        text = ""

    # Update the logged message with actual content
    await log_message(db, phone, "inbound", msg_type, reply_id or text, msg_id, update_content=True)

    # Route to the appropriate flow
    await route_message(phone, text, reply_id, msg_type, db)

    return {"status": "ok"}
