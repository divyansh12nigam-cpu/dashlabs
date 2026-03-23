"""Portfolio flow — share work samples."""
from app.whatsapp.sender import send_text, send_buttons
from app.whatsapp.templates import PORTFOLIO_MESSAGE, BACK_TO_MENU_BUTTONS


async def send_portfolio(phone: str):
    """Send portfolio info."""
    await send_text(phone, PORTFOLIO_MESSAGE)
    await send_buttons(phone, "Want to start your project?", BACK_TO_MENU_BUTTONS)
