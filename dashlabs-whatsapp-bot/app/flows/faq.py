"""FAQ flow — answer common questions."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text, send_list, send_buttons
from app.whatsapp.templates import FAQS, BACK_TO_MENU_BUTTONS


async def send_faq_list(phone: str):
    """Send FAQ topics as a list message."""
    rows = [
        {"id": faq_id, "title": faq["title"][:24], "description": faq["answer"][:72]}
        for faq_id, faq in FAQS.items()
    ]
    await send_list(
        phone,
        "Here are answers to common questions:",
        "Browse FAQs",
        [{"title": "FAQs", "rows": rows}],
    )


async def handle_faq_selection(phone: str, reply_id: str, db: AsyncSession):
    """Handle a specific FAQ selection."""
    faq = FAQS.get(reply_id)
    if faq:
        await send_text(phone, f"*{faq['title']}*\n\n{faq['answer']}")
        await send_buttons(phone, "Need anything else?", BACK_TO_MENU_BUTTONS)
    else:
        await send_faq_list(phone)
