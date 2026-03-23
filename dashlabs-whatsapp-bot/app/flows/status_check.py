"""Status check flow — look up existing project by phone or name."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text, send_buttons
from app.whatsapp.templates import (
    STATUS_ASK_PHONE,
    STATUS_FOUND,
    STATUS_NOT_FOUND,
    BACK_TO_MENU_BUTTONS,
)
from app.services.conversation_service import set_conversation, clear_conversation
from app.services.lead_service import find_lead_by_phone, find_lead_by_name
from app.utils.helpers import normalize_phone

FLOW_NAME = "status_check"


async def start(phone: str, db: AsyncSession):
    """Begin status check — first try to look up by the sender's own phone."""
    lead = await find_lead_by_phone(db, phone)
    if lead:
        msg = STATUS_FOUND.format(service=lead.service_needed or "N/A", status=lead.status or "new")
        await send_text(phone, msg)
        await send_buttons(phone, "Need anything else?", BACK_TO_MENU_BUTTONS)
    else:
        # No lead found for their own number — ask for lookup info
        await set_conversation(db, phone, FLOW_NAME, "ask_lookup")
        await send_text(phone, STATUS_ASK_PHONE)


async def handle_step(phone: str, text: str, reply_id: str, step: str, conv, db: AsyncSession):
    """Handle the lookup step."""
    if step == "ask_lookup":
        query = text.strip()
        # Try as phone number first
        normalized = normalize_phone(query)
        lead = None
        if len(normalized) >= 10:
            lead = await find_lead_by_phone(db, normalized)
        if not lead:
            lead = await find_lead_by_name(db, query)

        if lead:
            msg = STATUS_FOUND.format(service=lead.service_needed or "N/A", status=lead.status or "new")
            await send_text(phone, msg)
            await send_buttons(phone, "Need anything else?", BACK_TO_MENU_BUTTONS)
        else:
            await send_text(phone, STATUS_NOT_FOUND)
            await send_buttons(phone, "What would you like to do?", BACK_TO_MENU_BUTTONS)

        await clear_conversation(db, phone)
