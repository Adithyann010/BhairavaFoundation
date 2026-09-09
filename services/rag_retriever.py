"""
Website Content & RAG Retriever for Bairava Groups.
Retrieves accurate, real-time database context from Django models to feed into the AI Chatbot.
"""

from typing import Dict, List, Optional
import re


def get_group_general_knowledge() -> str:
    """Return core foundational facts about Bairava Groups."""
    return (
        "BAIRAVA GROUPS GENERAL INFORMATION:\n"
        "- Name: BAIRAVA GROUPS\n"
        "- Philosophy: 'Building Businesses. Creating Opportunities. Serving Communities.'\n"
        "- Heritage: Over 20+ years of excellence across diverse industry verticals.\n"
        "- Contact Phone: +91 99417 57555\n"
        "- Contact URL: /contact/\n"
        "- Total Divisions: 10 integrated divisions comprising 8 commercial businesses and 2 social & charitable initiatives.\n"
        "\n"
        "EIGHT COMMERCIAL BUSINESS DIVISIONS:\n"
        "1. BAIRAVA FINANCE: Transparent, professional & responsible financial solutions & advisory (/businesses/finance/).\n"
        "2. BAIRAVA CONSTRUCTION & LAND PROMOTERS: Turnkey residential, commercial, luxury villas, architectural builds and property development in Chennai (/businesses/construction/).\n"
        "3. BAIRAVA CLOUD KITCHEN: Hygienic, authentic culinary experiences, traditional South Indian thalis, dum biryani, and daily wholesome meal boxes (/businesses/cloud-kitchen/).\n"
        "4. BAIRAVA SPORTS CLUB: World-class sports facilities, BWF-standard indoor badminton courts, fitness & strength conditioning, and junior coaching academies (/businesses/sports-club/).\n"
        "5. BAIRAVA EVENT MANAGEMENT: End-to-end event planning, luxury weddings, corporate summits, social galas, and bespoke decor coordination (/businesses/event-management/).\n"
        "6. BAIRAVA ஆடுகளம்: News channel committed to delivering accurate, unbiased, and people-centric journalism across Tamil Nadu, India and worldwide (/businesses/aadukalam/).\n"
        "7. BAIRAVA MEDIA: Meaningful visual storytelling, documentary production, digital content, podcast studio, and brand communications (/businesses/media/).\n"
        "8. BHAIRAVA ASSOCIATION: Community networking, professional collaboration, member engagement, knowledge sharing and collective development (/businesses/bhairava-association/).\n"
        "\n"
        "TWO SOCIAL & COMMUNITY INITIATIVES:\n"
        "9. BAIRAVA FOUNDATION: Sustainable community empowerment through educational scholarships, healthcare access, welfare development, and youth mentorship (/foundation/).\n"
        "10. BAIRAVA TRUST: Compassionate social care, daily Annadhanam (free meals for 500+ daily), full-time elder care shelter, low-income student support, and community relief drives (/trust/).\n"
        "\n"
        "LEGAL ASSOCIATES:\n"
        "- LEGAL ASSOCIATES: Professional legal guidance for businesses, organizations and individuals in corporate law, contracts, property titles, compliance and advisory (/legal/).\n"
        "\n"
        "FUTURE PLAN (UPCOMING VENTURES - COMING SOON):\n"
        "- BAIRAVA WATER SOLUTIONS: Planned venture for packaged drinking water and water-can distribution for homes, offices and businesses. Tagline: 'Pure Water. Healthier Lives.' (/future-plan/#water-solutions).\n"
        "- BAIRAVA JEWELLERY: Planned venture for elegant and high-quality jewellery collections, combining traditional inspiration with modern craftsmanship for meaningful moments and special occasions. Tagline: 'Timeless Beauty. Lasting Value.' (/future-plan/#jewellery).\n"
    )


def retrieve_website_context(user_query: str, current_page: str = "", division_context: str = "") -> Dict[str, any]:
    """
    Retrieve comprehensive context from Django database models based on user query and active page context.
    Returns:
        {
            'context_text': str,
            'matched_divisions': List[str],
            'primary_division': Optional[str],
            'action_links': List[Dict[str, str]]
        }
    """
    from core.models import (
        BusinessDivision, DivisionOffering, MediaArticle, Stat, NewsItem
    )
    from construction.models import ConstructionProject, Service as ConstructionService
    from trust.models import TrustActivityItem, TrustProgram
    from events.models import EventPortfolioItem, EventType

    query_lower = (user_query or "").lower().strip()
    page_lower = (current_page or "").lower().strip()
    division_hint = (division_context or "").lower().strip()

    context_sections = []
    matched_divisions = []
    action_links = []
    primary_division = None

    # Always include group overview summary
    context_sections.append(get_group_general_knowledge())

    # Detect primary division from page URL or hint
    slug_map = {
        'construction': 'construction',
        'foundation': 'foundation',
        'trust': 'trust',
        'finance': 'finance',
        'cloud-kitchen': 'cloud-kitchen',
        'sports-club': 'sports-club',
        'sports': 'sports-club',
        'aadukalam': 'aadukalam',
        'media': 'media',
        'association': 'bhairava-association',
        'bhairava-association': 'bhairava-association',
        'legal': 'legal',
        'event': 'event-management',
        'events': 'event-management',
        'event-management': 'event-management',
    }

    for key, slug in slug_map.items():
        if key in page_lower or key in division_hint:
            primary_division = slug
            break

    # Keyword matching in query for specific divisions
    keywords = {
        'construction': ['construct', 'build', 'project', 'villa', 'residential', 'commercial', 'flat', 'interior', 'civil', 'contractor', 'architect', 'chennai build'],
        'foundation': ['foundation', 'empower', 'education', 'school', 'scholarship', 'mentorship', 'welfare', 'empowering'],
        'trust': ['trust', 'annadhanam', 'meal', 'elder', 'old age', 'sanctuary', 'shelter', 'donate', 'donation', 'sponsor', 'charity', 'hunger', 'relief'],
        'finance': ['finance', 'financial', 'advisory', 'loan', 'capital', 'working capital', 'equipment', 'funding', 'asset finance'],
        'cloud-kitchen': ['cloud kitchen', 'kitchen', 'food', 'meal', 'thali', 'biryani', 'catering', 'menu', 'culinary', 'lunch', 'dinner', 'order food', 'boxes'],
        'sports-club': ['sports club', 'badminton', 'court', 'fitness', 'gym', 'training', 'coach', 'coaching', 'athletic', 'bwf', 'indoor court'],
        'aadukalam': ['aadukalam', 'news', 'news channel', 'breaking news', 'tamil nadu news', 'broadcast', 'journalism', 'newsroom', 'livestream'],
        'event-management': ['event', 'events', 'wedding', 'reception', 'conference', 'summit', 'gala', 'decor', 'party', 'coordination', 'planner'],
        'media': ['media', 'video', 'documentary', 'podcast', 'storytelling', 'press', 'production', 'broadcast', 'article', 'news story'],
        'association': ['association', 'bhairava association', 'networking', 'collaboration', 'community networking', 'member engagement', 'collective growth'],
        'legal': ['legal', 'lawyer', 'advocate', 'corporate law', 'contracts', 'property law', 'compliance', 'legal advisory', 'dispute'],
        'contact': ['contact', 'phone', 'email', 'address', 'enquiry', 'reach', 'office', 'touch', 'call', 'talk', 'location', 'where', 'number']
    }

    matched_keywords = set()
    for category, terms in keywords.items():
        if any(re.search(rf'\b{re.escape(t)}\b', query_lower) for t in terms):
            matched_keywords.add(category)
            if category in slug_map:
                matched_divisions.append(slug_map[category])

    if primary_division and primary_division not in matched_divisions:
        matched_divisions.insert(0, primary_division)

    # 1. Fetch Business Divisions and Offerings
    try:
        divisions = list(BusinessDivision.objects.filter(is_active=True).prefetch_related('offerings'))
        divisions_info = ["ALL 9 BUSINESS DIVISIONS & INITIATIVES:"]
        for div in divisions:
            is_matched = (div.slug in matched_divisions) or (primary_division == div.slug) or not matched_divisions
            div_text = f"• Division: {div.name} (Slug: {div.slug}, Type: {div.get_division_type_display()})\n"
            div_text += f"  Tagline: {div.tagline}\n"
            div_text += f"  Short Description: {div.short_description}\n"
            if is_matched and div.full_description:
                div_text += f"  In-Depth Details: {div.full_description}\n"
            
            offerings = list(div.offerings.all())
            if offerings:
                div_text += "  Offerings & Services:\n"
                for off in offerings:
                    badge_str = f" [{off.badge}]" if off.badge else ""
                    div_text += f"    - {off.title}{badge_str}: {off.description}\n"
            
            target_url = div.target_url or f"/businesses/{div.slug}/"
            div_text += f"  Website Page: {target_url}\n"
            divisions_info.append(div_text)
        
        context_sections.append("\n".join(divisions_info))
    except Exception as e:
        context_sections.append(f"Business divisions data retrieval note: {e}")

    # 2. Fetch Construction Projects & Services if relevant or general query
    if 'construction' in matched_divisions or primary_division == 'construction' or not matched_divisions or 'project' in query_lower:
        try:
            projects = list(ConstructionProject.objects.all()[:10])
            services = list(ConstructionService.objects.all())
            const_info = ["CONSTRUCTION PROJECTS & ENGINEERING SERVICES (Bairava Construction & Land Promoters):"]
            if services:
                const_info.append("Services Offered:")
                for s in services:
                    const_info.append(f"  - {s.title}: {s.description}")
            if projects:
                const_info.append("Projects Portfolio:")
                for p in projects:
                    area_str = f", Built-up area: {p.built_up_area}" if p.built_up_area else ""
                    year_str = f", Year: {p.completion_year}" if p.completion_year else ""
                    const_info.append(f"  - {p.title} (Category: {p.get_category_display()}, Location: {p.location}, Status: {p.get_status_display()}{year_str}{area_str}): {p.description}")
            const_info.append("Enquiry Page: /businesses/construction/")
            context_sections.append("\n".join(const_info))
            action_links.append({'title': 'Explore Construction Projects', 'url': '/businesses/construction/'})
        except Exception as e:
            context_sections.append(f"Construction data retrieval note: {e}")

    # 3. Fetch Trust Activities & Programs
    if 'trust' in matched_divisions or primary_division == 'trust' or not matched_divisions or 'annadhanam' in query_lower:
        try:
            activities = list(TrustActivityItem.objects.all()[:10])
            programs = list(TrustProgram.objects.all())
            trust_info = ["BAIRAVA CHARITABLE TRUST ACTIVITIES & COMMUNITY CARE:"]
            if programs:
                trust_info.append("Key Programs:")
                for prog in programs:
                    trust_info.append(f"  - {prog.title}: {prog.description}")
            if activities:
                trust_info.append("Featured Activity Highlights & Impact:")
                for act in activities:
                    impact_str = f" [Impact: {act.impact_stat}]" if act.impact_stat else ""
                    trust_info.append(f"  - {act.title} (Category: {act.get_category_display()}{impact_str}): {act.description}")
            trust_info.append("Trust Page: /trust/")
            context_sections.append("\n".join(trust_info))
            action_links.append({'title': 'Explore Bairava Trust', 'url': '/trust/'})
        except Exception as e:
            context_sections.append(f"Trust data retrieval note: {e}")

    # 4. Fetch Event Management Portfolio & Event Types
    if 'event-management' in matched_divisions or primary_division == 'event-management' or not matched_divisions or 'event' in query_lower:
        try:
            portfolio = list(EventPortfolioItem.objects.all()[:10])
            event_types = list(EventType.objects.all())
            events_info = ["BAIRAVA EVENT MANAGEMENT SERVICES & PORTFOLIO:"]
            if event_types:
                events_info.append("Event Types Managed:")
                for et in event_types:
                    events_info.append(f"  - {et.title}: {et.description}")
            if portfolio:
                events_info.append("Featured Event Portfolio:")
                for ep in portfolio:
                    cap_str = f", Capacity: {ep.guest_capacity}" if ep.guest_capacity else ""
                    events_info.append(f"  - {ep.title} (Category: {ep.get_category_display()}, Location: {ep.location}{cap_str}, Year: {ep.completion_year}): {ep.description}")
            events_info.append("Event Enquiry Page: /businesses/event-management/")
            context_sections.append("\n".join(events_info))
            action_links.append({'title': 'Event Planning Services', 'url': '/businesses/event-management/'})
        except Exception as e:
            context_sections.append(f"Events data retrieval note: {e}")

    # 5. Fetch Media Articles & Highlights
    if 'media' in matched_divisions or primary_division == 'media' or 'article' in query_lower or 'news' in query_lower:
        try:
            articles = list(MediaArticle.objects.all()[:5])
            if articles:
                media_info = ["BAIRAVA MEDIA PUBLISHED ARTICLES & STORIES:"]
                for art in articles:
                    media_info.append(f"  - {art.title} (Category: {art.category}): {art.summary}")
                media_info.append("Media Page: /businesses/media/")
                context_sections.append("\n".join(media_info))
        except Exception as e:
            pass

    # 6. Fetch Group Stats & Recent News
    try:
        stats = list(Stat.objects.all())
        news = list(NewsItem.objects.all()[:4])
        stats_info = ["KEY GROUP STATS & HIGHLIGHTS:"]
        if stats:
            stats_info.append("Verified Statistics: " + ", ".join([f"{s.value} {s.label}" for s in stats]))
        if news:
            stats_info.append("Recent Updates:")
            for n in news:
                stats_info.append(f"  - {n.title} [{n.get_category_display()}]: {n.description}")
        context_sections.append("\n".join(stats_info))
    except Exception as e:
        pass

    # Action links
    if 'contact' in matched_keywords or 'enquiry' in query_lower or not action_links:
        action_links.append({'title': 'Contact Us', 'url': '/contact/'})

    return {
        'context_text': "\n\n".join(context_sections),
        'matched_divisions': matched_divisions,
        'primary_division': primary_division,
        'action_links': action_links
    }


def get_suggested_questions(current_page: str = "") -> List[str]:
    """
    Return tailored suggested questions based on the active page/division.
    """
    page = (current_page or "").lower().strip()

    if 'construction' in page:
        return [
            "What projects are available?",
            "Tell me about your construction services.",
            "How can I make an enquiry?"
        ]
    elif 'foundation' in page:
        return [
            "What initiatives does the Foundation support?",
            "How can I get involved?",
            "Tell me about educational scholarships."
        ]
    elif 'trust' in page:
        return [
            "What activities does the Trust conduct?",
            "How can I contact the Trust?",
            "Tell me about the daily Annadhanam meal initiative."
        ]
    elif 'event' in page:
        return [
            "What types of events do you manage?",
            "How can I make an event enquiry?",
            "Tell me about your wedding planning services."
        ]
    elif 'finance' in page:
        return [
            "Tell me about Bairava Finance.",
            "What financial solutions are offered?",
            "How can I get financial advisory?"
        ]
    elif 'cloud-kitchen' in page or 'kitchen' in page:
        return [
            "What does Bairava Cloud Kitchen offer?",
            "Tell me about your meal boxes and thalis.",
            "Do you cater for bulk orders and events?"
        ]
    elif 'sports' in page:
        return [
            "What sports facilities are available?",
            "Tell me about the junior badminton coaching.",
            "What fitness training is offered?"
        ]
    elif 'aadukalam' in page:
        return [
            "What is Bairava Aadukalam?",
            "Tell me about Kabaddi tournaments and Silambam.",
            "What rural sports events are organized?"
        ]
    elif 'media' in page:
        return [
            "What does Bairava Media do?",
            "What video production and podcast services exist?",
            "Tell me about your published stories."
        ]
    elif 'association' in page:
        return [
            "What is Bhairava Association?",
            "Tell me about community networking and collaboration.",
            "How can I participate or connect with the association?"
        ]
    elif 'legal' in page:
        return [
            "What legal guidance is provided by Legal Associates?",
            "Tell me about corporate and business law support.",
            "How can I schedule a confidential legal consultation?"
        ]
    elif 'future-plan' in page or 'future' in page:
        return [
            "What is Bairava Water Solutions?",
            "Tell me about Bairava Jewellery.",
            "What are the upcoming ventures under Future Plan?"
        ]
    elif 'contact' in page:
        return [
            "How can I contact Bairava Groups?",
            "What is your phone number?",
            "Where can I submit a business enquiry?"
        ]
    else:
        # Default / Homepage
        return [
            "What businesses does Bairava Groups operate?",
            "Tell me about Bairava Groups.",
            "How can I contact you?"
        ]
