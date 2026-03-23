"""CRUD operations for leads."""
import logging
from typing import Optional, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Lead

logger = logging.getLogger(__name__)


async def create_lead(db: AsyncSession, data: Dict[str, Any]) -> Lead:
    """Create a new lead from captured flow data."""
    lead = Lead(
        phone=data.get("phone", ""),
        name=data.get("name"),
        business_name=data.get("business"),
        service_needed=data.get("service"),
        budget_range=data.get("budget"),
        timeline=data.get("timeline"),
        details=data.get("details"),
        source=data.get("source", "whatsapp"),
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    logger.info("Lead created: id=%s phone=%s service=%s", lead.id, lead.phone, lead.service_needed)
    return lead


async def find_lead_by_phone(db: AsyncSession, phone: str) -> Optional[Lead]:
    """Find the most recent lead by phone number."""
    result = await db.execute(
        select(Lead)
        .where(Lead.phone == phone)
        .order_by(Lead.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def find_lead_by_name(db: AsyncSession, name: str) -> Optional[Lead]:
    """Find the most recent lead by name (case-insensitive partial match)."""
    result = await db.execute(
        select(Lead)
        .where(Lead.name.ilike(f"%{name}%"))
        .order_by(Lead.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
