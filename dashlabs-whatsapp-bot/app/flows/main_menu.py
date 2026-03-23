"""Main menu — the entry point for all conversations."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.whatsapp.sender import send_buttons, send_list
from app.whatsapp.templates import (
    WELCOME_MESSAGE,
    WELCOME_BUTTONS,
    MORE_OPTIONS_SECTIONS,
)
from app.services.conversation_service import clear_conversation


async def send_main_menu(phone: str, db: AsyncSession):
    """Send the welcome message with main menu buttons."""
    await clear_conversation(db, phone)
    await send_buttons(phone, WELCOME_MESSAGE, WELCOME_BUTTONS)


async def send_more_options(phone: str):
    """Send the expanded options list."""
    await send_list(
        phone,
        "Here are more ways we can help:",
        "Browse Options",
        MORE_OPTIONS_SECTIONS,
    )
