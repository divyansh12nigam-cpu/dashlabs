"""Manage conversation state and message logging."""
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Conversation, Message

logger = logging.getLogger(__name__)


async def get_conversation(db: AsyncSession, phone: str) -> Optional[Conversation]:
    """Get the active conversation for a phone number, or None if expired/missing."""
    result = await db.execute(select(Conversation).where(Conversation.phone == phone))
    conv = result.scalar_one_or_none()
    if conv is None:
        return None

    # Check timeout
    timeout = timedelta(minutes=settings.CONVERSATION_TIMEOUT_MINUTES)
    if datetime.utcnow() - conv.last_active_at > timeout:
        # Stale conversation — clear it
        await clear_conversation(db, phone)
        return None

    return conv


async def set_conversation(
    db: AsyncSession,
    phone: str,
    flow: Optional[str],
    step: Optional[str],
    flow_data: Optional[Dict[str, Any]] = None,
) -> Conversation:
    """Create or update conversation state."""
    result = await db.execute(select(Conversation).where(Conversation.phone == phone))
    conv = result.scalar_one_or_none()

    if conv is None:
        conv = Conversation(
            phone=phone,
            current_flow=flow,
            current_step=step,
            flow_data=json.dumps(flow_data or {}),
            last_active_at=datetime.utcnow(),
        )
        db.add(conv)
    else:
        conv.current_flow = flow
        conv.current_step = step
        if flow_data is not None:
            conv.flow_data = json.dumps(flow_data)
        conv.last_active_at = datetime.utcnow()

    await db.commit()
    return conv


async def get_flow_data(conv: Optional[Conversation]) -> Dict[str, Any]:
    """Parse flow_data JSON from a conversation."""
    if conv is None:
        return {}
    try:
        return json.loads(conv.flow_data or "{}")
    except json.JSONDecodeError:
        return {}


async def clear_conversation(db: AsyncSession, phone: str):
    """Remove conversation state (flow completed or timed out)."""
    result = await db.execute(select(Conversation).where(Conversation.phone == phone))
    conv = result.scalar_one_or_none()
    if conv:
        await db.delete(conv)
        await db.commit()


async def log_message(
    db: AsyncSession,
    phone: str,
    direction: str,
    message_type: str,
    content: str,
    whatsapp_msg_id: str = "",
    update_content: bool = False,
) -> bool:
    """Log a message. Returns True if this msg_id was already logged (duplicate)."""
    if whatsapp_msg_id:
        result = await db.execute(
            select(Message).where(Message.whatsapp_msg_id == whatsapp_msg_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            if update_content and content:
                existing.content = content
                await db.commit()
            return True  # duplicate

    msg = Message(
        phone=phone,
        direction=direction,
        message_type=message_type,
        content=content,
        whatsapp_msg_id=whatsapp_msg_id,
    )
    db.add(msg)
    await db.commit()
    return False
