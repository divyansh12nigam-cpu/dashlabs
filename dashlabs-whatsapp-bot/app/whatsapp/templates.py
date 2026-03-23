"""All message content and button definitions for the bot."""

# ---------- Button / List IDs ----------
# Main menu
MENU_START_PROJECT = "menu_start_project"
MENU_GET_QUOTE = "menu_get_quote"
MENU_MORE_OPTIONS = "menu_more_options"

# More options list
OPT_PORTFOLIO = "opt_portfolio"
OPT_BOOK_CALL = "opt_book_call"
OPT_SERVICES = "opt_services"
OPT_FAQ = "opt_faq"
OPT_STATUS_CHECK = "opt_status_check"

# Services list
SVC_WEBSITES = "svc_websites"
SVC_WHATSAPP_BOTS = "svc_whatsapp_bots"
SVC_AI_CHATBOTS = "svc_ai_chatbots"
SVC_LLM_WRAPPERS = "svc_llm_wrappers"
SVC_MICRO_SITES = "svc_micro_sites"
SVC_BRANDING = "svc_branding"
SVC_AUTOMATION = "svc_automation"
SVC_INTERNAL_TOOLS = "svc_internal_tools"
SVC_APP_MVPS = "svc_app_mvps"

# Budget buttons
BUDGET_UNDER_15K = "budget_under_15k"
BUDGET_15K_30K = "budget_15k_30k"
BUDGET_30K_PLUS = "budget_30k_plus"

# Timeline buttons
TIMELINE_ASAP = "timeline_asap"
TIMELINE_THIS_MONTH = "timeline_this_month"
TIMELINE_NO_RUSH = "timeline_no_rush"

# Call booking
CALL_TODAY = "call_today"
CALL_TOMORROW = "call_tomorrow"
CALL_THIS_WEEK = "call_this_week"
CALL_MORNING = "call_morning"
CALL_AFTERNOON = "call_afternoon"
CALL_EVENING = "call_evening"

# Navigation
NAV_BACK_MENU = "nav_back_menu"
NAV_START_PROJECT = "nav_start_project"

# ---------- Services info ----------
SERVICES = {
    SVC_WEBSITES: {
        "name": "Websites",
        "description": "Multi-page responsive websites with modern design, SEO optimization, and mobile-first approach.",
    },
    SVC_WHATSAPP_BOTS: {
        "name": "WhatsApp Bots",
        "description": "WhatsApp API automation — lead capture, customer support, appointment booking, and more.",
    },
    SVC_AI_CHATBOTS: {
        "name": "AI Chatbots",
        "description": "Conversational AI bots powered by LLMs for intelligent customer interactions.",
    },
    SVC_LLM_WRAPPERS: {
        "name": "LLM Wrappers & AI Tools",
        "description": "Knowledge bases, content engines, decision tools, and custom GPTs tailored to your business.",
    },
    SVC_MICRO_SITES: {
        "name": "Micro-Sites",
        "description": "Single-page or minimal sites — perfect for events, launches, or landing pages.",
    },
    SVC_BRANDING: {
        "name": "Branding",
        "description": "Logo design, brand identity, color systems, and visual guidelines.",
    },
    SVC_AUTOMATION: {
        "name": "Automation",
        "description": "Process automation — connect tools, eliminate manual work, streamline workflows.",
    },
    SVC_INTERNAL_TOOLS: {
        "name": "Internal Tools",
        "description": "Custom dashboards, admin panels, and business tools built for your team.",
    },
    SVC_APP_MVPS: {
        "name": "App MVPs",
        "description": "Minimum viable products — web or mobile apps shipped fast to validate your idea.",
    },
}

SERVICE_ID_TO_NAME = {k: v["name"] for k, v in SERVICES.items()}

# ---------- FAQ content ----------
FAQS = {
    "faq_turnaround": {
        "title": "How long does it take?",
        "answer": "It depends on the project scope. Simple sites take 3-5 days, full products take 2-4 weeks. We'll give you an exact timeline after scoping your project.",
    },
    "faq_process": {
        "title": "What's your process?",
        "answer": (
            "Our process is simple:\n\n"
            "1. *Discover* — Free 30-min call to understand your needs\n"
            "2. *Scope* — Clear proposal within 24 hours\n"
            "3. *Build* — Daily progress with tight feedback loops\n"
            "4. *Launch* — Deployed + post-launch support"
        ),
    },
    "faq_payment": {
        "title": "Payment terms?",
        "answer": "50% upfront to start, 50% on delivery. We accept UPI and bank transfer.",
    },
    "faq_support": {
        "title": "Post-launch support?",
        "answer": "Every project includes post-launch support. Duration depends on the project scope — we'll confirm this in your proposal.",
    },
    "faq_revisions": {
        "title": "Do you do revisions?",
        "answer": "Yes — 2 revision rounds are included in all projects. Additional revisions can be arranged if needed.",
    },
}

# ---------- Message templates ----------
WELCOME_MESSAGE = (
    "Welcome to *Dash Labs*! \U0001F680\n\n"
    "We're a Design + AI studio — we build websites, bots, AI tools & branding, shipped in days.\n\n"
    "How can we help you today?"
)

WELCOME_BUTTONS = [
    {"id": MENU_START_PROJECT, "title": "Start a Project"},
    {"id": MENU_GET_QUOTE, "title": "Get a Quote"},
    {"id": MENU_MORE_OPTIONS, "title": "More Options"},
]

MORE_OPTIONS_SECTIONS = [
    {
        "title": "Explore",
        "rows": [
            {"id": OPT_PORTFOLIO, "title": "View our Work", "description": "See what we've built"},
            {"id": OPT_BOOK_CALL, "title": "Book a Call", "description": "Schedule a free 15-min call"},
            {"id": OPT_SERVICES, "title": "What We Build", "description": "Our full list of services"},
        ],
    },
    {
        "title": "Help",
        "rows": [
            {"id": OPT_FAQ, "title": "FAQs", "description": "Common questions answered"},
            {"id": OPT_STATUS_CHECK, "title": "Project Status", "description": "Check on an existing project"},
        ],
    },
]

ENQUIRY_ASK_SERVICE = "What type of project are you looking for?"

ENQUIRY_SERVICE_SECTIONS = [
    {
        "title": "Services",
        "rows": [
            {"id": svc_id, "title": info["name"][:24], "description": info["description"][:72]}
            for svc_id, info in SERVICES.items()
        ],
    }
]

ENQUIRY_ASK_NAME = "Great choice! What's your name?"
ENQUIRY_ASK_BUSINESS = "What's your business or brand called?\n\n_(Type 'skip' if you don't have one yet)_"
ENQUIRY_ASK_BUDGET = "What's your approximate budget range?"
ENQUIRY_ASK_TIMELINE = "When do you need this delivered?"
ENQUIRY_ASK_DETAILS = (
    "Any other details you'd like to share? Features, inspiration links, specific requirements?\n\n"
    "_(Type 'skip' if nothing else to add)_"
)

BUDGET_BUTTONS = [
    {"id": BUDGET_UNDER_15K, "title": "Under 15K"},
    {"id": BUDGET_15K_30K, "title": "15K - 30K"},
    {"id": BUDGET_30K_PLUS, "title": "30K+"},
]

TIMELINE_BUTTONS = [
    {"id": TIMELINE_ASAP, "title": "ASAP"},
    {"id": TIMELINE_THIS_MONTH, "title": "This month"},
    {"id": TIMELINE_NO_RUSH, "title": "No rush"},
]

ENQUIRY_CONFIRMED = (
    "\u2705 *Got it!* Here's a summary:\n\n"
    "\U0001F464 *Name:* {name}\n"
    "\U0001F3E2 *Business:* {business}\n"
    "\U0001F6E0 *Service:* {service}\n"
    "\U0001F4B0 *Budget:* {budget}\n"
    "\u23F0 *Timeline:* {timeline}\n"
    "{details_line}"
    "\n\nOur team will get back to you *within 4 hours*. Talk soon!"
)

PORTFOLIO_MESSAGE = (
    "*Our Recent Work* \U0001F3A8\n\n"
    "Check out what we've built:\n"
    "\U0001F310 dashlabs.co.in — Our own site\n\n"
    "We'll share more relevant samples based on your project. "
    "Want to discuss yours?"
)

BOOK_CALL_ASK_DAY = "When works best for a quick 15-min call?"
BOOK_CALL_ASK_SLOT = "What time works?"

CALL_DAY_BUTTONS = [
    {"id": CALL_TODAY, "title": "Today"},
    {"id": CALL_TOMORROW, "title": "Tomorrow"},
    {"id": CALL_THIS_WEEK, "title": "This Week"},
]

CALL_SLOT_BUTTONS = [
    {"id": CALL_MORNING, "title": "Morning (10-12)"},
    {"id": CALL_AFTERNOON, "title": "Afternoon (2-5)"},
    {"id": CALL_EVENING, "title": "Evening (6-8)"},
]

CALL_CONFIRMED = (
    "\u2705 *Call request received!*\n\n"
    "\U0001F4C5 *When:* {day}, {slot}\n\n"
    "We'll confirm your slot shortly on WhatsApp. Talk soon!"
)

STATUS_ASK_PHONE = "Please share the phone number or name your project is registered under."
STATUS_FOUND = "\U0001F4CB Your project (*{service}*) is currently: *{status}*\n\nOur team will share a detailed update shortly."
STATUS_NOT_FOUND = "I couldn't find a project with that info. Would you like to start a new enquiry?"

BACK_TO_MENU_BUTTONS = [
    {"id": NAV_START_PROJECT, "title": "Start a Project"},
    {"id": NAV_BACK_MENU, "title": "Back to Menu"},
]

UNSUPPORTED_MESSAGE = "I can handle text and button replies. Could you try again with text, or tap one of the menu options?"

QUOTE_ASK_SERVICE = "What service are you looking for a quote on?"
QUOTE_ASK_DETAILS = (
    "Tell us a bit about what you need — features, scope, inspiration links, anything that helps us quote accurately.\n\n"
    "_(Type 'skip' if you're not sure yet — we'll figure it out on a call)_"
)
QUOTE_CONFIRMED = (
    "\u2705 *Quote request received!*\n\n"
    "\U0001F6E0 *Service:* {service}\n"
    "\U0001F4DD *Details:* {details}\n\n"
    "Our team will share a *custom quote within 4 hours*. Hang tight!"
)
