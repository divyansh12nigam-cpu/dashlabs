"""Book a call flow — collect day + time slot preference."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text, send_buttons
from app.whatsapp.templates import (
    BOOK_CALL_ASK_DAY,
    BOOK_CALL_ASK_SLOT,
    CALL_CONFIRMED,
    CALL_DAY_BUTTONS,
    CALL_SLOT_BUTTONS,
    BACK_TO_MENU_BUTTONS,
    CALL_TODAY,
    CALL_TOMORROW,
    CALL_THIS_WEEK,
    CALL_MORNING,
    CALL_AFTERNOON,
    CALL_EVENING,
)
from app.services.conversation_service import set_conversation, get_flow_data, clear_conversation
from app.services.notification_service import notify_call_request

FLOW_NAME = "book_call"

DAY_MAP = {
    CALL_TODAY: "Today",
    CALL_TOMORROW: "Tomorrow",
    CALL_THIS_WEEK: "This Week",
}

SLOT_MAP = {
    CALL_MORNING: "Morning (10-12)",
    CALL_AFTERNOON: "Afternoon (2-5)",
    CALL_EVENING: "Evening (6-8)",
}


async def start(phone: str, db: AsyncSession):
    """Begin the book call flow."""
    await set_conversation(db, phone, FLOW_NAME, "ask_day")
    await send_buttons(phone, BOOK_CALL_ASK_DAY, CALL_DAY_BUTTONS)


async def handle_step(phone: str, text: str, reply_id: str, step: str, conv, db: AsyncSession):
    """Handle steps in the book call flow."""
    data = await get_flow_data(conv)

    if step == "ask_day":
        data["day"] = DAY_MAP.get(reply_id, text.strip())
        await set_conversation(db, phone, FLOW_NAME, "ask_slot", data)
        await send_buttons(phone, BOOK_CALL_ASK_SLOT, CALL_SLOT_BUTTONS)

    elif step == "ask_slot":
        data["slot"] = SLOT_MAP.get(reply_id, text.strip())
        msg = CALL_CONFIRMED.format(day=data["day"], slot=data["slot"])
        await send_text(phone, msg)
        await send_buttons(phone, "Anything else?", BACK_TO_MENU_BUTTONS)

        data["phone"] = phone
        await notify_call_request(data)
        await clear_conversation(db, phone)
