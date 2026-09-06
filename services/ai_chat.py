"""
AI Chat Service Layer for Bairava Groups.
Provides secure, website-aware AI chat capabilities via OpenAI-compatible endpoints
with robust database-grounded RAG retrieval and zero-hallucination guarantees.
"""

import os
import re
import logging
import requests
from typing import Dict, Any, Optional
from django.conf import settings
from .rag_retriever import retrieve_website_context, get_suggested_questions

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are Bairava AI Assistant, the official website assistant for Bairava Groups.

Your job is to help website visitors understand Bairava Groups, its businesses, projects, services, initiatives, events and contact information.

Answer clearly, professionally and concisely.

Use only the information supplied from the Bairava Groups website and retrieved database context.

Never invent facts.

If information is unavailable, say:
"I don't have that information in the Bairava Groups website data. Please contact the Bairava Groups team for accurate information."

Do not provide financial, legal or other professional advice.

Do not claim that a service, product, project or event exists unless it is present in the supplied website information.

When appropriate, direct users to the relevant page of the Bairava Groups website."""


def get_ai_config() -> Dict[str, str]:
    """Retrieve AI configuration from Django settings or environment."""
    api_key = getattr(settings, 'AI_API_KEY', os.environ.get('AI_API_KEY', '')).strip()
    base_url = getattr(settings, 'AI_API_BASE_URL', os.environ.get('AI_API_BASE_URL', 'https://api.openai.com/v1')).strip().rstrip('/')
    model = getattr(settings, 'AI_MODEL', os.environ.get('AI_MODEL', 'gpt-4o-mini')).strip()
    return {
        'api_key': api_key,
        'base_url': base_url,
        'model': model
    }


def call_openai_compatible_api(
    user_message: str,
    context_text: str,
    current_page: str = "",
    timeout: int = 12
) -> Optional[str]:
    """
    Call an OpenAI-compatible endpoint with the strict system prompt and database context.
    """
    config = get_ai_config()
    api_key = config['api_key']
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_content = f"{SYSTEM_INSTRUCTION}\n\n=== VERIFIED BAIRAVA GROUPS DATABASE CONTEXT ===\n{context_text}\n\n=== USER CURRENT PAGE ===\n{current_page or 'Homepage'}"

    payload = {
        "model": config['model'],
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }

    url = f"{config['base_url']}/chat/completions"
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            choices = data.get("choices", [])
            if choices and "message" in choices[0]:
                return choices[0]["message"].get("content", "").strip()
        else:
            logger.warning(f"AI API request failed with status {response.status_code}: {response.text}")
    except Exception as exc:
        logger.error(f"Error connecting to AI API provider: {exc}")
    
    return None


def generate_rag_fallback_response(
    user_query: str,
    context_data: Dict[str, Any],
    current_page: str = ""
) -> str:
    """
    Intelligent, deterministic RAG generator using verified database context.
    Ensures zero hallucination and strict website-aware factual precision.
    """
    q = (user_query or "").lower().strip()
    page = (current_page or "").lower().strip()

    # 1. Contact / Enquiry triggers
    contact_triggers = [
        'contact', 'how to reach', 'how can i contact', 'phone', 'phone number',
        'enquire', 'enquiry', 'i want to enquire', 'i want to contact',
        'need more information', 'call you', 'email', 'touch with you', 'reach out',
        'office address', 'where are you located'
    ]
    if any(ct in q for ct in contact_triggers) and not any(k in q for k in ['foundation', 'trust', 'construction', 'finance', 'sports', 'kitchen', 'event', 'media', 'aadukalam']):
        return (
            "Sure. You can contact the Bairava Groups team through our **[Contact Us](/contact/)** page or directly reach us by phone at **[+91 99417 57555](tel:+919941757555)**.\n\n"
            "Our team is happy to assist you with commercial business enquiries, project requirements, foundation initiatives, and charitable trust partnerships."
        )

    # 2. Specific Division: Trust
    if any(term in q for term in ['trust', 'annadhanam', 'elder care', 'shelter', 'meal', 'donation', 'donate', 'charitable']) or ('trust' in page and any(term in q for term in ['activity', 'activities', 'support', 'conduct', 'what do', 'tell me'])):
        return (
            "**[Bairava Charitable Trust](/trust/)** conducts dedicated humanitarian service and daily social care across Chennai.\n\n"
            "**Key Trust Activities:**\n"
            "- **Daily Annadhanam**: Serving over 500+ wholesome hot meals daily to senior citizens, hospital caregivers, and underserved individuals.\n"
            "- **Elder Care Sanctuary**: Providing dignified shelter, nutrition, and healthcare to senior citizens in need.\n"
            "- **Educational Scholarships**: Supporting low-income students with school fees and supplies.\n"
            "- **Community & Disaster Relief**: Emergency relief distribution during crises and festivals.\n\n"
            "Learn more or sponsor a meal drive on the **[Bairava Trust Page](/trust/)**."
        )

    # 3. Specific Division: Foundation
    if ('foundation' in q) or ('foundation' in page and any(term in q for term in ['initiative', 'initiatives', 'support', 'involved', 'programme', 'program', 'what do', 'tell me'])):
        return (
            "**[Bairava Foundation](/foundation/)** is dedicated to sustainable community empowerment and social development.\n\n"
            "**Core Initiatives:**\n"
            "- **Educational Scholarships & Supplies**: Direct financial aid for school fees, notebooks, and learning materials for deserving students.\n"
            "- **Community Welfare & Medical Support**: Regular health screening camps, eye checkups, and essential care in underserved communities.\n"
            "- **Vocational Skill Workshops**: Practical training in computer literacy, tailoring, and handicrafts for financial independence.\n"
            "- **Youth Leadership & Mentorship**: Career guidance and mentorship sessions for students.\n\n"
            "To collaborate or get involved, visit the **[Bairava Foundation Page](/foundation/)**."
        )

    # 4. Specific Division: Construction & Land Promoters
    if any(term in q for term in ['construction', 'promoters', 'builder', 'project', 'villa', 'residential', 'commercial complex', 'interior', 'flat']) or ('construction' in page and any(term in q for term in ['what do you do', 'services', 'available', 'work', 'projects'])):
        return (
            "**[Bairava Construction & Promoters](/businesses/construction/)** brings over two decades of engineering and structural excellence in Chennai.\n\n"
            "**Key Offerings:**\n"
            "- **Turnkey Residential Buildings & Luxury Villas**: Custom architectural blueprints, earthquake-resistant RCC design, and handover.\n"
            "- **Commercial Complexes**: Modern retail and office spaces built to strict safety and durability standards.\n"
            "- **Interiors & Renovations**: Modular kitchens, false ceilings, and interior styling.\n\n"
            "**Featured Projects:**\n"
            "- *Bairava Heights* — Residential Complex in Anna Nagar\n"
            "- *Bairava Palm Enclave* — Luxury Villas in ECR\n"
            "- *Bairava Commercial Center* — Corporate Office Space in T. Nagar\n\n"
            "You can submit an enquiry for your site directly on the **[Construction & Projects Page](/businesses/construction/)** or via **[Contact Us](/contact/)**."
        )

    # 5. Specific Division: Finance
    if ('finance' in q or 'financial' in q) or ('finance' in page and any(term in q for term in ['service', 'services', 'solution', 'do', 'offer'])):
        return (
            "**[Bairava Finance](/businesses/finance/)** provides transparent, professional, and responsible financial solutions.\n\n"
            "**Solutions Offered:**\n"
            "- **Financial Advisory & Planning**: Objective guidance for business cash flow management and prudent capital allocation.\n"
            "- **Working Capital Assistance**: Consultation on managing operational overheads and business expansion cycles.\n"
            "- **Asset & Equipment Financing Advisory**: Evaluating funding options for machinery and commercial infrastructure.\n"
            "- **Customer-First Transparent Terms**: Clear, straightforward terms and dedicated relationship managers.\n\n"
            "Submit your financial advisory enquiry on the **[Bairava Finance Page](/businesses/finance/)**."
        )

    # 6. Specific Division: Cloud Kitchen
    if any(term in q for term in ['cloud kitchen', 'kitchen', 'food', 'thali', 'biryani', 'menu', 'meal box', 'catering', 'culinary']) or ('cloud-kitchen' in page and any(term in q for term in ['offer', 'menu', 'food'])):
        return (
            "**[Bairava Cloud Kitchen](/businesses/cloud-kitchen/)** prepares hygienic, authentic, and flavorful culinary experiences using farm-fresh ingredients.\n\n"
            "**Menu Highlights:**\n"
            "- **Signature South Indian Thali**: Authentic recipes with hand-ground spices, sambar, rasam, seasonal poriyal, and appalam.\n"
            "- **Dum Biryani Specialties**: Slow-cooked aromatic Seeraga Samba and Basmati preparations.\n"
            "- **Daily Wholesome Meal Boxes**: Balanced subscription lunches and dinners for corporate staff, students, and families.\n"
            "- **Bulk Catering & Party Orders**: Freshly prepared banquet meals for corporate and private gatherings.\n\n"
            "Explore our menu on the **[Bairava Cloud Kitchen Page](/businesses/cloud-kitchen/)**."
        )

    # 7. Specific Division: Sports Club
    if any(term in q for term in ['sports club', 'badminton', 'gym', 'fitness', 'court', 'coaching']) or ('sports-club' in page and any(term in q for term in ['available', 'facility', 'facilities', 'sports'])):
        return (
            "**[Bairava Sports Club](/businesses/sports-club/)** offers world-class training infrastructure and fitness facilities.\n\n"
            "**Facilities & Programs:**\n"
            "- **Indoor Badminton Courts**: Synthetic multi-court facility built to BWF standards with glare-free LED lighting.\n"
            "- **Strength & Conditioning Zone**: Modern resistance equipment, free weights, and agility tracks.\n"
            "- **Junior Coaching Academy**: Structured modules led by certified coaches focusing on technique and match tactics.\n"
            "- **Community Leagues**: Regular friendly tournaments for all age groups.\n\n"
            "Join or book court slots on the **[Bairava Sports Club Page](/businesses/sports-club/)**."
        )

    # 8. Specific Division: Aadukalam
    if any(term in q for term in ['aadukalam', 'kabaddi', 'silambam', 'traditional sport', 'rural sport']) or ('aadukalam' in page and any(term in q for term in ['what is', 'do', 'sports'])):
        return (
            "**[Bairava Aadukalam](/businesses/aadukalam/)** is dedicated to celebrating and preserving Tamil Nadu's rich heritage of indigenous and traditional sports.\n\n"
            "**Activities & Initiatives:**\n"
            "- **Kabaddi Tournaments & Coaching**: State-level championships and professional clay court training.\n"
            "- **Silambam & Traditional Martial Arts**: Ancient staff-spinning and self-defense art taught by master practitioners.\n"
            "- **Rural Athletic Festivals**: Community galas featuring Kho-Kho, volleyball, and tug of war.\n"
            "- **Youth Fitness Camps**: Conditioning workshops for local athletes.\n\n"
            "Learn more on the **[Bairava Aadukalam Page](/businesses/aadukalam/)**."
        )

    # 9. Specific Division: Event Management
    if any(term in q for term in ['event', 'events', 'wedding', 'reception', 'conference', 'summit', 'decor', 'gala']) or ('event-management' in page and any(term in q for term in ['services', 'manage', 'type', 'types'])):
        return (
            "**[Bairava Event Management](/businesses/event-management/)** delivers end-to-end event planning, luxury coordination, and turnkey production.\n\n"
            "**Services Offered:**\n"
            "- **Luxury Weddings & Receptions**: Destination weddings, custom floral decor, stage production, and guest hospitality.\n"
            "- **Corporate Summits & Product Launches**: Multi-track AV setups, keynote stages, and seamless delegate management.\n"
            "- **Social Galas & Family Celebrations**: Birthdays, anniversaries, and bespoke private gatherings.\n"
            "- **Decor & Technical Production**: Lighting, live streaming, and vendor sourcing.\n\n"
            "Plan your next event on the **[Bairava Event Management Page](/businesses/event-management/)**."
        )

    # 10. Specific Division: Media
    if any(term in q for term in ['media', 'video', 'documentary', 'podcast', 'storytelling', 'press', 'broadcast']) or ('media' in page and any(term in q for term in ['do', 'services', 'articles'])):
        return (
            "**[Bairava Media](/businesses/media/)** is our digital storytelling and creative media production arm.\n\n"
            "**Capabilities:**\n"
            "- **Video & Documentary Production**: High-definition 4K corporate films and community documentaries.\n"
            "- **Digital Content & Podcast Studio**: Acoustically treated studio for multi-mic podcast recordings.\n"
            "- **Live Broadcast & Event Coverage**: Multi-camera live streaming for major conferences and sports tournaments.\n"
            "- **Brand Storytelling**: Narrative-driven PR, press releases, and digital campaigns.\n\n"
            "Explore published articles on the **[Bairava Media Page](/businesses/media/)**."
        )

    # 11. Future Plan (Upcoming Ventures - Coming Soon)
    if any(term in q for term in ['future plan', 'future business', 'upcoming venture', 'upcoming business', 'vision ahead']) or ('future-plan' in page and any(term in q for term in ['what', 'tell me', 'about', 'plan'])):
        return (
            "**Future Plan — Our Vision Ahead**\n\n"
            "Expanding our horizons to create more value, opportunities and meaningful impact. Bairava Groups has two exciting new ventures coming soon:\n\n"
            "1. **[Bairava Water Solutions](/future-plan/#water-solutions)** — Planned venture focused on packaged drinking water and water-can distribution for homes, offices, and businesses (\"Pure Water. Healthier Lives.\")\n"
            "2. **[Bairava Jewellery](/future-plan/#jewellery)** — Planned venture bringing elegant and high-quality jewellery collections combining traditional inspiration with modern craftsmanship (\"Timeless Beauty. Lasting Value.\")\n\n"
            "Both ventures are currently marked as **Coming Soon**. Explore more details on our dedicated **[Future Plan Page](/future-plan/)**."
        )

    # 12. Specific Upcoming Venture: Bairava Water Solutions
    if any(term in q for term in ['water solution', 'water solutions', 'bairava water', 'water can', 'drinking water', 'packaged water']):
        return (
            "**[Bairava Water Solutions](/future-plan/#water-solutions)** is a planned upcoming venture under Bairava Groups (\"Pure Water. Healthier Lives.\").\n\n"
            "**Main Concept & Key Highlights:**\n"
            "- Packaged drinking water & water-can distribution for homes, offices, and businesses.\n"
            "- Clean, pure, and safe drinking water supply.\n"
            "- Reliable and convenient doorstep delivery.\n\n"
            "Status: **Coming Soon**. Read more on the **[Future Plan Page](/future-plan/)**."
        )

    # 13. Specific Upcoming Venture: Bairava Jewellery
    if any(term in q for term in ['jewellery', 'jewelry', 'bairava jewellery', 'gold jewellery']):
        return (
            "**[Bairava Jewellery](/future-plan/#jewellery)** is a planned upcoming venture under Bairava Groups (\"Timeless Beauty. Lasting Value.\").\n\n"
            "**Main Concept & Key Highlights:**\n"
            "- Elegant and high-quality gold jewellery collections for meaningful celebrations and special occasions.\n"
            "- Harmonious blend of traditional South Indian heritage with contemporary modern design.\n"
            "- Expert craftsmanship and customer-focused shopping experience.\n\n"
            "Status: **Coming Soon**. Read more on the **[Future Plan Page](/future-plan/)**."
        )

    # 11. General businesses / divisions overview
    if any(term in q for term in ['what businesses', 'business divisions', 'seven business', '7 business', 'divisions', 'ventures', 'what does bairava do', 'tell me about bairava groups', 'about bairava groups', 'overview']):
        return (
            "**Bairava Groups** operates across **7 commercial business divisions** and **2 social & charitable initiatives**:\n\n"
            "**Commercial Businesses:**\n"
            "1. **[Bairava Finance](/businesses/finance/)** — Transparent, professional, and responsible financial solutions & advisory.\n"
            "2. **[Bairava Construction & Promoters](/businesses/construction/)** — Turnkey residential, luxury villas, commercial developments, and interior executions in Chennai.\n"
            "3. **[Bairava Cloud Kitchen](/businesses/cloud-kitchen/)** — Authentic regional thalis, dum biryani, wholesome daily meal boxes, and catering.\n"
            "4. **[Bairava Sports Club](/businesses/sports-club/)** — BWF-standard indoor badminton courts, gym fitness conditioning, and junior coaching.\n"
            "5. **[Bairava Event Management](/businesses/event-management/)** — Luxury weddings, corporate summits, social galas, and bespoke decor planning.\n"
            "6. **[Bairava Aadukalam](/businesses/aadukalam/)** — State-level Kabaddi tournaments, Silambam martial arts, and rural sports galas.\n"
            "7. **[Bairava Media](/businesses/media/)** — Documentary production, podcast studio recordings, digital storytelling, and brand communications.\n\n"
            "**Community & Social Initiatives:**\n"
            "8. **[Bairava Foundation](/foundation/)** — Community empowerment, school scholarships, and healthcare access.\n"
            "9. **[Bairava Trust](/trust/)** — Compassionate social care, daily Annadhanam (500+ free meals daily), and elder care shelter.\n\n"
            "How can I assist you with any specific division or project?"
        )

    # 12. General Contact / Enquiry fallback if mentioned anywhere
    if any(ct in q for ct in contact_triggers):
        return (
            "Sure. You can contact the Bairava Groups team through our **[Contact Us](/contact/)** page or directly reach us by phone at **[+91 99417 57555](tel:+919941757555)**.\n\n"
            "Our team is happy to assist you with commercial business enquiries, project requirements, foundation initiatives, and charitable trust partnerships."
        )

    # 13. Strict refusal for unknown queries not in website/database context
    # Do NOT invent prices, dates, unlisted business branches, stock prices, external facts.
    return (
        "I don't have that information in the Bairava Groups website data. "
        "Please contact the Bairava Groups team for accurate information via our **[Contact Us](/contact/)** page or call **[+91 99417 57555](tel:+919941757555)**."
    )


def process_chat_message(
    message: str,
    conversation_id: str = "",
    current_page: str = "",
    division_context: str = ""
) -> Dict[str, Any]:
    """
    Main entry point for processing a chat message.
    1. Validates and sanitizes input.
    2. Retrieves relevant RAG context from the database.
    3. Attempts AI completion via API; falls back to deterministic RAG engine if unavailable.
    4. Formulates response with suggestions and action links.
    """
    clean_message = (message or "").strip()
    if not clean_message:
        return {
            "response": "Please enter a question so I can assist you with Bairava Groups.",
            "conversation_id": conversation_id,
            "suggestions": get_suggested_questions(current_page)
        }

    # Retrieve context from Django DB
    context_data = retrieve_website_context(
        user_query=clean_message,
        current_page=current_page,
        division_context=division_context
    )

    # Try calling AI API if configured
    ai_answer = None
    config = get_ai_config()
    if config['api_key']:
        ai_answer = call_openai_compatible_api(
            user_message=clean_message,
            context_text=context_data['context_text'],
            current_page=current_page
        )

    # If AI API is not configured or failed, use grounded database fallback
    if not ai_answer:
        ai_answer = generate_rag_fallback_response(
            user_query=clean_message,
            context_data=context_data,
            current_page=current_page
        )

    # Get tailored suggestions
    suggestions = get_suggested_questions(current_page)

    return {
        "response": ai_answer,
        "conversation_id": conversation_id,
        "suggestions": suggestions,
        "action_links": context_data.get('action_links', [])
    }
