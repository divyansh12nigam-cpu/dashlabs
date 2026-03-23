"""Services flow — explain what each service includes."""
from app.whatsapp.sender import send_text, send_list, send_buttons
from app.whatsapp.templates import SERVICES, BACK_TO_MENU_BUTTONS


async def send_services_list(phone: str):
    """Send the full list of services."""
    rows = [
        {"id": svc_id, "title": info["name"][:24], "description": info["description"][:72]}
        for svc_id, info in SERVICES.items()
    ]
    await send_list(
        phone,
        "Here's everything we build at Dash Labs:",
        "View Services",
        [{"title": "Our Services", "rows": rows}],
    )


async def handle_service_selection(phone: str, reply_id: str):
    """Handle a specific service selection from the list."""
    service = SERVICES.get(reply_id)
    if service:
        await send_text(phone, f"*{service['name']}*\n\n{service['description']}")
        await send_buttons(
            phone,
            "Interested in this service?",
            BACK_TO_MENU_BUTTONS,
        )
    else:
        await send_services_list(phone)
