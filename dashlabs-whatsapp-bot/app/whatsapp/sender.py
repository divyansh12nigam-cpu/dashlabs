"""WhatsApp Cloud API message sender."""
import logging
from typing import List, Dict, Optional

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

API_URL = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
    "Content-Type": "application/json",
}


async def _send(payload: dict) -> dict:
    """Send a message via the WhatsApp Cloud API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(API_URL, json=payload, headers=HEADERS)
        if resp.status_code != 200:
            logger.error("WhatsApp API error %s: %s", resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()


async def send_text(phone: str, body: str) -> dict:
    """Send a plain text message."""
    return await _send({
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": body},
    })


async def send_buttons(
    phone: str,
    body: str,
    buttons: List[Dict[str, str]],
    header: Optional[str] = None,
    footer: Optional[str] = None,
) -> dict:
    """Send an interactive message with reply buttons (max 3).

    buttons: [{"id": "btn_id", "title": "Button Text"}, ...]
    """
    action_buttons = [
        {"type": "reply", "reply": {"id": b["id"], "title": b["title"][:20]}}
        for b in buttons[:3]
    ]
    interactive = {
        "type": "button",
        "body": {"text": body},
        "action": {"buttons": action_buttons},
    }
    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"text": footer}

    return await _send({
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": interactive,
    })


async def send_list(
    phone: str,
    body: str,
    button_text: str,
    sections: List[Dict],
    header: Optional[str] = None,
    footer: Optional[str] = None,
) -> dict:
    """Send an interactive list message.

    sections: [{"title": "Section", "rows": [{"id": "row_id", "title": "Row", "description": "..."}]}]
    """
    interactive = {
        "type": "list",
        "body": {"text": body},
        "action": {
            "button": button_text[:20],
            "sections": sections,
        },
    }
    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"text": footer}

    return await _send({
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": interactive,
    })
