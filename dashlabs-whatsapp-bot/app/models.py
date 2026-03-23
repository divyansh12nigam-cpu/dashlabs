from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String, nullable=False, index=True)
    name = Column(String)
    business_name = Column(String)
    email = Column(String)
    service_needed = Column(String)
    budget_range = Column(String)
    timeline = Column(String)
    details = Column(Text)
    status = Column(String, default="new", index=True)
    source = Column(String, default="whatsapp")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String, nullable=False, unique=True, index=True)
    current_flow = Column(String, nullable=True)
    current_step = Column(String, nullable=True)
    flow_data = Column(Text, default="{}")
    last_active_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String, nullable=False)
    direction = Column(String, nullable=False)  # inbound | outbound
    message_type = Column(String)  # text | button_reply | list_reply
    content = Column(Text)
    whatsapp_msg_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
