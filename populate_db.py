import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bairava_project.settings')
django.setup()

from construction.models import ConstructionProject, Service
from trust.models import TrustActivityItem, TrustProgram
from law_associates.models import LegalPracticeDetail, LegalService
from events.models import EventPortfolioItem, EventType
from core.models import Stat, NewsItem

print("Populating database with premium, highly professional content promoting Bairava Groups...")

# 1. ADD ADDITIONAL CONSTRUCTION PROJECTS
construction_projects = [
    {
        "title": "Bairava Heights",
        "location": "Anna Nagar, Chennai",
        "category": "residential",
        "status": "ongoing",
        "description": "A luxury 5-story residential complex featuring state-of-the-art earthquake-resistant RCC structure, modular designer kitchens, false ceilings in all rooms, and premium automated elevators.",
        "completion_year": "2027",
        "built_up_area": "18,500 sq.ft",
        "order": 10
    },
    {
        "title": "Bairava Tech Hub",
        "location": "Perungudi, OMR, Chennai",
        "category": "commercial",
        "status": "completed",
        "description": "Premium multi-tenant corporate office building featuring a glass facade, green building certifications, ISO compliant sewage treatment plant, and 100% power backup capacity.",
        "completion_year": "2025",
        "built_up_area": "45,000 sq.ft",
        "order": 11
    },
    {
        "title": "The Golden Villas",
        "location": "East Coast Road (ECR), Chennai",
        "category": "villas",
        "status": "completed",
        "description": "An enclave of 12 sea-facing signature villas designed with premium Italian marble flooring, individual swimming pools, integrated security systems, and private landscaped terraces.",
        "completion_year": "2024",
        "built_up_area": "6,200 sq.ft",
        "order": 12
    },
    {
        "title": "Corporate HQ Renovation",
        "location": "Nungambakkam, Chennai",
        "category": "interiors",
        "status": "completed",
        "description": "Complete interior design, custom furniture fabrication, modular partitions, pop false ceilings, and acoustic soundproofing execution for a major multi-national logistics firm.",
        "completion_year": "2024",
        "built_up_area": "12,000 sq.ft",
        "order": 13
    }
]

for cp in construction_projects:
    obj, created = ConstructionProject.objects.get_or_create(
        title=cp["title"],
        defaults=cp
    )
    if created:
        print(f"Created construction project: {cp['title']}")

# 2. POPULATE TRUST ACTIVITIES
trust_activities = [
    {
        "title": "Daily Annadhanam Program",
        "category": "annadhanam",
        "impact_stat": "500+ Hot Meals Served Daily",
        "description": "Our sacred daily food service provides fresh, hot, and nutritious meals to the elderly, the homeless, and low-income laborers near the trust premises without fail, 365 days a year.",
        "order": 1
    },
    {
        "title": "Bairava Senior Care Sanctuary",
        "category": "elder_care",
        "impact_stat": "40+ Permanent Senior Residents",
        "description": "A fully-equipped, safe, and comfortable shelter home offering free lodging, nursing care, nutritional meals, clothing, and complete medical supervision to abandoned senior citizens.",
        "order": 2
    },
    {
        "title": "Higher Education Scholarships",
        "category": "scholarship",
        "impact_stat": "150+ Scholarships Awarded Yearly",
        "description": "Financial sponsorships covering school tuition fees, books, and college admissions for talented youngsters from economically weaker backgrounds to enable equal career opportunities.",
        "order": 3
    },
    {
        "title": "Cyclone Relief & Medical Camps",
        "category": "relief",
        "impact_stat": "10,000+ Families Supported",
        "description": "Immediate disaster relief distribution including dry rations, clean drinking water, medicines, and temporary shelter during natural calamities, supplemented by regular free health checkup camps.",
        "order": 4
    }
]

for ta in trust_activities:
    obj, created = TrustActivityItem.objects.get_or_create(
        title=ta["title"],
        defaults=ta
    )
    if created:
        print(f"Created trust activity: {ta['title']}")

# 3. POPULATE LEGAL PRACTICE DETAILS
legal_details = [
    {
        "title": "Legal Notice Drafting & Reply representation",
        "category": "notice",
        "turnaround_time": "24 - 48 Hour Draft Delivery",
        "description": "We specialize in drafting clean, legally sound legal notices and responses for property disputes, recovery issues, breach of contracts, and family matters.",
        "order": 1
    },
    {
        "title": "Property Title Verification & Registration",
        "category": "property",
        "turnaround_time": "Full Title Investigation Certificate",
        "description": "Comprehensive document vetting, parent document verification, guideline value checks, encumbrance certificate reviews, and representation at sub-registrar offices.",
        "order": 2
    },
    {
        "title": "Money Recovery Suit & Section 138 Representation",
        "category": "recovery",
        "turnaround_time": "High Success Rate Recovery Proceedings",
        "description": "Advocacy for recovery of commercial debts, pending partner payouts, security deposits, and legal handling of Cheque Bounce cases under Section 138 of NI Act.",
        "order": 3
    },
    {
        "title": "Criminal Trial Defense & Anticipatory Bail representation",
        "category": "criminal",
        "turnaround_time": "Immediate Emergency Bail Assistance",
        "description": "Representing clients at magistrate courts, sessions courts, and Madras High Court for bail, anticipatory bail, quashing of FIRs, and trial defense.",
        "order": 4
    },
    {
        "title": "Harassment Protection & Debt Settlement Advice",
        "category": "protection",
        "turnaround_time": "Immediate Cease-and-Desist Remedies",
        "description": "Legal protection against unlawful harassment by bank recovery agents and lenders, debt restructuring advisory, and defense of personal credit rights.",
        "order": 5
    }
]

for ld in legal_details:
    obj, created = LegalPracticeDetail.objects.get_or_create(
        title=ld["title"],
        defaults=ld
    )
    if created:
        print(f"Created legal practice detail: {ld['title']}")

# 4. POPULATE EVENT PORTFOLIO ITEMS
event_portfolio = [
    {
        "title": "The Grand Royal Palace Wedding",
        "location": "Mayor Ramanathan Hall (MRC), Chennai",
        "category": "wedding",
        "guest_capacity": "1,200 Guests",
        "completion_year": "2025",
        "description": "A lavish turnkey wedding production featuring customized traditional Chettinad decor, state-of-the-art stage lighting, coordinates for 50+ catering staff, and end-to-end guest logistics.",
        "order": 1
    },
    {
        "title": "Bairava Corporate Tech Summit",
        "location": "ITC Grand Chola, Chennai",
        "category": "corporate",
        "guest_capacity": "600 Delegates",
        "completion_year": "2025",
        "description": "Production and execution of a annual tech summit including curved LED screen set-ups, audio-visual engineering, host coordination, and delegate registration management.",
        "order": 2
    },
    {
        "title": "Sri Angala Eswari Festival Gala",
        "location": "KK Nagar Ground, Chennai",
        "category": "social",
        "guest_capacity": "3,000+ Attendees",
        "completion_year": "2026",
        "description": "Complete planning, crowd control barricading, mega stage set-up, sound systems, and catering management for a grand social festival gathering.",
        "order": 3
    },
    {
        "title": "Contemporary Floral & Mandap Concept",
        "location": "Leela Palace, Chennai",
        "category": "decor",
        "guest_capacity": "800 Guests",
        "completion_year": "2025",
        "description": "Exquisite wedding mandap decoration combining premium imported white orchids and traditional marigolds with glass partitions and floating lighting elements.",
        "order": 4
    }
]

for ep in event_portfolio:
    obj, created = EventPortfolioItem.objects.get_or_create(
        title=ep["title"],
        defaults=ep
    )
    if created:
        print(f"Created event portfolio item: {ep['title']}")

print("All premium database cards successfully populated!")
