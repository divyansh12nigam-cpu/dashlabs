"""Central message router — dispatches to the correct flow based on conversation state."""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_text
from app.whatsapp.templates import (
    MENU_START_PROJECT,
    MENU_GET_QUOTE,
    MENU_MORE_OPTIONS,
    OPT_PORTFOLIO,
    OPT_BOOK_CALL,
    OPT_SERVICES,
    OPT_FAQ,
    OPT_STATUS_CHECK,
    NAV_BACK_MENU,
    NAV_START_PROJECT,
    UNSUPPORTED_MESSAGE,
    FAQS,
    SERVICES as SERVICES_MAP,
)
from app.services.conversation_service import get_conversation
from app.flows import (
    main_menu,
    new_enquiry,
    get_quote,
    faq,
    services,
    portfolio,
    book_call,
    status_check,
)

logger = logging.getLogger(__name__)

# Keywords that trigger the main menu
MENU_KEYWORDS = {"hi", "hello", "hey", "menu", "start", "help", "hola"}


async def route_message(
    phone: str,
    text: str,
    reply_id: str,
    msg_type: str,
    db: AsyncSession,
):
    """Route an incoming message to the correct flow handler."""

    # Check for navigation buttons first (these override everything)
    if reply_id == NAV_BACK_MENU:
        await main_menu.send_main_menu(phone, db)
        return
    if reply_id == NAV_START_PROJECT:
        await new_enquiry.start(phone, db)
        return

    # Check if user is in an active flow
    conv = await get_conversation(db, phone)

    if conv and conv.current_flow:
        # User is mid-flow — route to the correct flow handler
        flow = conv.current_flow
        step = conv.current_step

        if flow == "new_enquiry":
            await new_enquiry.handle_step(phone, text, reply_id, step, conv, db)
            return
        elif flow == "get_quote":
            await get_quote.handle_step(phone, text, reply_id, step, conv, db)
            return
        elif flow == "book_call":
            await book_call.handle_step(phone, text, reply_id, step, conv, db)
            return
        elif flow == "status_check":
            await status_check.handle_step(phone, text, reply_id, step, conv, db)
            return

    # No active flow — route based on button reply or keyword

    # Main menu buttons
    if reply_id == MENU_START_PROJECT:
        await new_enquiry.start(phone, db)
        return
    if reply_id == MENU_GET_QUOTE:
        await get_quote.start(phone, db)
        return
    if reply_id == MENU_MORE_OPTIONS:
        await main_menu.send_more_options(phone)
        return

    # More options list selections
    if reply_id == OPT_PORTFOLIO:
        await portfolio.send_portfolio(phone)
        return
    if reply_id == OPT_BOOK_CALL:
        await book_call.start(phone, db)
        return
    if reply_id == OPT_SERVICES:
        await services.send_services_list(phone)
        return
    if reply_id == OPT_FAQ:
        await faq.send_faq_list(phone)
        return
    if reply_id == OPT_STATUS_CHECK:
        await status_check.start(phone, db)
        return

    # FAQ selections
    if reply_id in FAQS:
        await faq.handle_faq_selection(phone, reply_id, db)
        return

    # Service detail selections
    if reply_id in SERVICES_MAP:
        await services.handle_service_selection(phone, reply_id)
        return

    # Text-based triggers
    if text:
        lower = text.strip().lower()
        if lower in MENU_KEYWORDS:
            await main_menu.send_main_menu(phone, db)
            return

    # Default: send main menu for any unrecognized input
    await main_menu.send_main_menu(phone, db)
