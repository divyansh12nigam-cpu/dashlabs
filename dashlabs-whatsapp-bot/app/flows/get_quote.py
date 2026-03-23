"""Get a quote flow — collect service + details, promise custom quote."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text, send_list, send_buttons
from app.whatsapp.templates import (
    QUOTE_ASK_SERVICE,
    QUOTE_ASK_DETAILS,
    QUOTE_CONFIRMED,
    ENQUIRY_SERVICE_SECTIONS,
    SERVICE_ID_TO_NAME,
    BACK_TO_MENU_BUTTONS,
)
from app.services.conversation_service import set_conversation, get_flow_data, clear_conversation
from app.services.lead_service import create_lead
from app.services.notification_service import notify_new_lead

FLOW_NAME = "get_quote"


async def start(phone: str, db: AsyncSession):
    """Begin the get quote flow."""
    await set_conversation(db, phone, FLOW_NAME, "ask_service")
    await send_list(phone, QUOTE_ASK_SERVICE, "Pick a Service", ENQUIRY_SERVICE_SECTIONS)


async def handle_step(phone: str, text: str, reply_id: str, step: str, conv, db: AsyncSession):
    """Handle steps in the get quote flow."""
    data = await get_flow_data(conv)

    if step == "ask_service":
        service_name = SERVICE_ID_TO_NAME.get(reply_id, text)
        data["service"] = service_name
        await set_conversation(db, phone, FLOW_NAME, "ask_details", data)
        await send_text(phone, QUOTE_ASK_DETAILS)

    elif step == "ask_details":
        val = text.strip()
        data["details"] = val if val.lower() != "skip" else "Will discuss on call"

        msg = QUOTE_CONFIRMED.format(
            service=data.get("service", "N/A"),
            details=data.get("details", "N/A"),
        )
        await send_text(phone, msg)
        await send_buttons(phone, "Anything else?", BACK_TO_MENU_BUTTONS)

        # Save as lead
        data["phone"] = phone
        data["source"] = "whatsapp_quote"
        await create_lead(db, data)
        await notify_new_lead(data)
        await clear_conversation(db, phone)
