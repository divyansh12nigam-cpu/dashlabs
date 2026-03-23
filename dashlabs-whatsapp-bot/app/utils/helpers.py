import re


def normalize_phone(phone: str) -> str:
    """Strip non-digits and ensure no leading +."""
    return re.sub(r"[^\d]", "", phone)


def format_phone_display(phone: str) -> str:
    """Format phone for display: 919625922022 -> +91 96259 22022."""
    phone = normalize_phone(phone)
    if len(phone) == 12 and phone.startswith("91"):
        return f"+{phone[:2]} {phone[2:7]} {phone[7:]}"
    return f"+{phone}"
