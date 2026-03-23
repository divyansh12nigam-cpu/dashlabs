"""Tests for conversation flow logic."""
from app.whatsapp.templates import (
    MENU_START_PROJECT,
    MENU_GET_QUOTE,
    MENU_MORE_OPTIONS,
    SERVICE_ID_TO_NAME,
    SERVICES,
    FAQS,
)


def test_service_ids_consistent():
    """All service IDs in the template map should have names."""
    for svc_id, info in SERVICES.items():
        assert svc_id in SERVICE_ID_TO_NAME
        assert SERVICE_ID_TO_NAME[svc_id] == info["name"]


def test_faq_content_present():
    """All FAQs should have title and answer."""
    for faq_id, faq in FAQS.items():
        assert "title" in faq
        assert "answer" in faq
        assert len(faq["title"]) > 0
        assert len(faq["answer"]) > 0


def test_button_ids_unique():
    """Main menu button IDs should be unique."""
    ids = [MENU_START_PROJECT, MENU_GET_QUOTE, MENU_MORE_OPTIONS]
    assert len(ids) == len(set(ids))
