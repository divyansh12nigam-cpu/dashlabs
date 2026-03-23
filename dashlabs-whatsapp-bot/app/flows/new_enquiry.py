"""New project enquiry — 7-step lead capture state machine."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text, send_buttons, send_list
from app.whatsapp.templates import (
    ENQUIRY_ASK_SERVICE,
    ENQUIRY_SERVICE_SECTIONS,
    ENQUIRY_ASK_NAME,
    ENQUIRY_ASK_BUSINESS,
    ENQUIRY_ASK_BUDGET,
    ENQUIRY_ASK_TIMELINE,
    ENQUIRY_ASK_DETAILS,
    ENQUIRY_CONFIRMED,
    BUDGET_BUTTONS,
    TIMELINE_BUTTONS,
    BACK_TO_MENU_BUTTONS,
    SERVICE_ID_TO_NAME,
    BUDGET_UNDER_15K,
    BUDGET_15K_30K,
    BUDGET_30K_PLUS,
    TIMELINE_ASAP,
    TIMELINE_THIS_MONTH,
    TIMELINE_NO_RUSH,
)
from app.services.conversation_service import set_conversation, get_flow_data
from app.services.lead_service import create_lead
from app.services.notification_service import notify_new_lead

FLOW_NAME = "new_enquiry"

BUDGET_MAP = {
    BUDGET_UNDER_15K: "Under 15K",
    BUDGET_15K_30K: "15K - 30K",
    BUDGET_30K_PLUS: "30K+",
}

TIMELINE_MAP = {
    TIMELINE_ASAP: "ASAP",
    TIMELINE_THIS_MONTH: "This month",
    TIMELINE_NO_RUSH: "No rush",
}


async def start(phone: str, db: AsyncSession):
    """Begin the new enquiry flow — ask which service."""
    await set_conversation(db, phone, FLOW_NAME, "ask_service")
    await send_list(phone, ENQUIRY_ASK_SERVICE, "Pick a Service", ENQUIRY_SERVICE_SECTIONS)


async def handle_step(phone: str, text: str, reply_id: str, step: str, conv, db: AsyncSession):
    """Handle a step in the new enquiry flow."""
    data = await get_flow_data(conv)

    if step == "ask_service":
        service_name = SERVICE_ID_TO_NAME.get(reply_id, text)
        data["service"] = service_name
        await set_conversation(db, phone, FLOW_NAME, "ask_name", data)
        await send_text(phone, ENQUIRY_ASK_NAME)

    elif step == "ask_name":
        data["name"] = text.strip()
        await set_conversation(db, phone, FLOW_NAME, "ask_business", data)
        await send_text(phone, ENQUIRY_ASK_BUSINESS)

    elif step == "ask_business":
        val = text.strip()
        data["business"] = val if val.lower() != "skip" else "N/A"
        await set_conversation(db, phone, FLOW_NAME, "ask_budget", data)
        await send_buttons(phone, ENQUIRY_ASK_BUDGET, BUDGET_BUTTONS)

    elif step == "ask_budget":
        data["budget"] = BUDGET_MAP.get(reply_id, text.strip())
        await set_conversation(db, phone, FLOW_NAME, "ask_timeline", data)
        await send_buttons(phone, ENQUIRY_ASK_TIMELINE, TIMELINE_BUTTONS)

    elif step == "ask_timeline":
        data["timeline"] = TIMELINE_MAP.get(reply_id, text.strip())
        await set_conversation(db, phone, FLOW_NAME, "ask_details", data)
        await send_text(phone, ENQUIRY_ASK_DETAILS)

    elif step == "ask_details":
        val = text.strip()
        data["details"] = val if val.lower() != "skip" else ""
        await _confirm_and_save(phone, data, db)


async def _confirm_and_save(phone: str, data: dict, db: AsyncSession):
    """Send confirmation, save lead, notify admin, clear state."""
    details = data.get("details", "")
    details_line = f"\U0001F4DD *Details:* {details}\n" if details else ""

    msg = ENQUIRY_CONFIRMED.format(
        name=data.get("name", "N/A"),
        business=data.get("business", "N/A"),
        service=data.get("service", "N/A"),
        budget=data.get("budget", "N/A"),
        timeline=data.get("timeline", "N/A"),
        details_line=details_line,
    )
    await send_text(phone, msg)
    await send_buttons(phone, "What would you like to do next?", BACK_TO_MENU_BUTTONS)

    # Save lead
    data["phone"] = phone
    data["source"] = "whatsapp"
    await create_lead(db, data)

    # Notify admin
    await notify_new_lead(data)

    # Clear conversation
    from app.services.conversation_service import clear_conversation
    await clear_conversation(db, phone)
