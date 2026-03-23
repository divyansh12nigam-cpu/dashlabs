"""Send admin notifications when new leads come in."""
import logging
from typing import Dict, Any

import aiosmtplib
from email.message import EmailMessage

from app.config import settings
from app.whatsapp.sender import send_text
from app.utils.helpers import format_phone_display

logger = logging.getLogger(__name__)


async def notify_new_lead(lead_data: Dict[str, Any]):
    """Notify admin about a new lead via WhatsApp and email."""
    await _notify_whatsapp(lead_data)
    await _notify_email(lead_data)


async def notify_call_request(call_data: Dict[str, Any]):
    """Notify admin about a call booking request."""
    phone_display = format_phone_display(call_data.get("phone", ""))
    msg = (
        "\U0001F4DE *New Call Request!*\n\n"
        f"\U0001F464 *From:* {phone_display}\n"
        f"\U0001F4C5 *When:* {call_data.get('day', 'N/A')}, {call_data.get('slot', 'N/A')}\n\n"
        "Please confirm the slot with them."
    )
    try:
        await send_text(settings.ADMIN_PHONE, msg)
    except Exception as e:
        logger.error("Failed to send call request notification: %s", e)


async def _notify_whatsapp(lead_data: Dict[str, Any]):
    """Send a WhatsApp message to the admin phone."""
    phone_display = format_phone_display(lead_data.get("phone", ""))
    details = lead_data.get("details", "")
    details_line = f"\U0001F4DD *Details:* {details}\n" if details and details.lower() != "skip" else ""

    msg = (
        "\U0001F514 *New Lead!*\n\n"
        f"\U0001F464 *Name:* {lead_data.get('name', 'N/A')}\n"
        f"\U0001F4F1 *Phone:* {phone_display}\n"
        f"\U0001F3E2 *Business:* {lead_data.get('business', 'N/A')}\n"
        f"\U0001F6E0 *Service:* {lead_data.get('service', 'N/A')}\n"
        f"\U0001F4B0 *Budget:* {lead_data.get('budget', 'N/A')}\n"
        f"\u23F0 *Timeline:* {lead_data.get('timeline', 'N/A')}\n"
        f"{details_line}\n"
        f"Source: WhatsApp Bot"
    )
    try:
        await send_text(settings.ADMIN_PHONE, msg)
        logger.info("Admin WhatsApp notification sent for lead: %s", lead_data.get("phone"))
    except Exception as e:
        logger.error("Failed to send admin WhatsApp notification: %s", e)


async def _notify_email(lead_data: Dict[str, Any]):
    """Send an email notification to the admin."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured, skipping email notification")
        return

    phone_display = format_phone_display(lead_data.get("phone", ""))
    details = lead_data.get("details", "")
    details_line = f"Details: {details}\n" if details and details.lower() != "skip" else ""

    body = (
        f"New lead from WhatsApp Bot:\n\n"
        f"Name: {lead_data.get('name', 'N/A')}\n"
        f"Phone: {phone_display}\n"
        f"Business: {lead_data.get('business', 'N/A')}\n"
        f"Service: {lead_data.get('service', 'N/A')}\n"
        f"Budget: {lead_data.get('budget', 'N/A')}\n"
        f"Timeline: {lead_data.get('timeline', 'N/A')}\n"
        f"{details_line}"
    )

    msg = EmailMessage()
    msg["Subject"] = f"New Lead: {lead_data.get('name', 'Unknown')} — {lead_data.get('service', 'N/A')}"
    msg["From"] = settings.SMTP_USER
    msg["To"] = settings.ADMIN_EMAIL
    msg.set_content(body)

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info("Admin email notification sent for lead: %s", lead_data.get("phone"))
    except Exception as e:
        logger.error("Failed to send admin email notification: %s", e)
