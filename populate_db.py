import os
import sys
import django

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bairava_project.settings')
django.setup()

from core.models import (
    Stat, NewsItem, BusinessDivision, DivisionOffering,
    DivisionGalleryItem, MediaArticle
)
from construction.models import ConstructionProject, Service
from trust.models import TrustActivityItem, TrustProgram
from law_associates.models import LegalPracticeDetail, LegalService
from events.models import EventPortfolioItem, EventType

print("Populating database with comprehensive Bairava Groups data...")

# 1. POPULATE BUSINESS DIVISIONS
divisions_data = [
    {
        "name": "BAIRAVA FOUNDATION",
        "slug": "foundation",
        "tagline": "EMPOWERING COMMUNITIES, NURTURING POTENTIAL",
        "short_description": "Bairava Foundation focuses on initiatives that support communities through education, welfare, development and meaningful social programmes.",
        "full_description": "Bairava Foundation is dedicated to driving sustainable community empowerment through focused programmes in primary education, youth mentorship, healthcare access, and welfare development. Working in close collaboration with grassroots stakeholders, the Foundation aims to create lasting social impact and opportunities for all.",
        "division_type": "foundation_trust",
        "icon_name": "heart-handshake",
        "static_image_path": "core/images/divisions/foundation.jpg",
        "target_url": "/foundation/",
        "accent_color": "#7C3B29",
        "order": 1,
    },
    {
        "name": "BAIRAVA FINANCE",
        "slug": "finance",
        "tagline": "TRANSPARENT, PROFESSIONAL & RESPONSIBLE FINANCIAL SOLUTIONS",
        "short_description": "Bairava Finance focuses on professional and responsible financial solutions with an emphasis on transparency, reliability and long-term customer relationships.",
        "full_description": "Bairava Finance delivers tailored financial advisory and customized solutions for businesses and individuals. Guided by integrity and thorough market understanding, we prioritize transparent practices, prudent planning, and dependable customer relationships built on trust.",
        "division_type": "business",
        "icon_name": "trending-up",
        "static_image_path": "core/images/divisions/finance.jpg",
        "target_url": "/businesses/finance/",
        "accent_color": "#241F1C",
        "order": 2,
    },
    {
        "name": "BAIRAVA CONSTRUCTION & LAND PROMOTERS",
        "slug": "construction",
        "tagline": "MASTERING STRUCTURAL EXCELLENCE & ARCHITECTURAL INTEGRITY",
        "short_description": "Bairava Construction & Land Promoters focuses on residential, commercial and property development projects with attention to planning, quality and dependable execution.",
        "full_description": "With over two decades of engineering and civil construction excellence in Chennai, Bairava Construction & Land Promoters manages turnkey residential complexes, luxury individual villas, commercial buildings, and bespoke interior transformations from concept blueprint to flawless handover.",
        "division_type": "business",
        "icon_name": "building",
        "static_image_path": "core/images/divisions/construction.jpg",
        "target_url": "/businesses/construction/",
        "accent_color": "#7C3B29",
        "order": 3,
    },
    {
        "name": "BAIRAVA CLOUD KITCHEN",
        "slug": "cloud-kitchen",
        "tagline": "HYGIENIC, AUTHENTIC & FLAVORFUL CULINARY EXPERIENCES",
        "short_description": "Bairava Cloud Kitchen brings convenient food experiences to customers through professionally managed kitchen operations and carefully prepared menus.",
        "full_description": "Operating state-of-the-art commercial culinary hubs, Bairava Cloud Kitchen prepares wholesome regional specialties and contemporary meal packages. With rigorous hygiene standards, farm-fresh ingredients, and consistent delivery execution, we serve wholesome delight across every order.",
        "division_type": "business",
        "icon_name": "utensils",
        "static_image_path": "core/images/divisions/cloud_kitchen.jpg",
        "target_url": "/businesses/cloud-kitchen/",
        "accent_color": "#A9822E",
        "order": 4,
    },
    {
        "name": "BAIRAVA SPORTS CLUB",
        "slug": "sports-club",
        "tagline": "NURTURING ATHLETIC TALENT & FITNESS COMMUNITIES",
        "short_description": "Bairava Sports Club promotes sports, fitness, training and community participation by creating opportunities for people to play, train and compete.",
        "full_description": "Bairava Sports Club features dedicated indoor and outdoor training infrastructure, professional coaching programmes, and community fitness initiatives designed to develop athletic skills, foster teamwork, and promote active lifestyles across all age groups.",
        "division_type": "business",
        "icon_name": "activity",
        "static_image_path": "core/images/divisions/sports_club.jpg",
        "target_url": "/businesses/sports-club/",
        "accent_color": "#5C2B1D",
        "order": 5,
    },
    {
        "name": "BAIRAVA EVENT MANAGEMENT",
        "slug": "event-management",
        "tagline": "TURNKEY EVENT EXPERIENCES & FLAWLESS CELEBRATIONS",
        "short_description": "Bairava Event Management provides end-to-end event planning and execution for corporate, cultural, social, sporting and private occasions.",
        "full_description": "From intimate ceremonies and grand royal weddings to high-profile corporate summits, Bairava Event Management coordinates every aspect of event design, venue logistics, audiovisual technology, catering coordination, and on-site hospitality so clients can enjoy seamless celebrations.",
        "division_type": "business",
        "icon_name": "calendar",
        "static_image_path": "core/images/divisions/events.jpg",
        "target_url": "/businesses/event-management/",
        "accent_color": "#A9822E",
        "order": 6,
    },
    {
        "name": "BAIRAVA ஆடுகளம்",
        "slug": "aadukalam",
        "tagline": "POLITICS, PEOPLE & THE STORIES THAT SHAPE TOMORROW.",
        "short_description": "BAIRAVA ஆடுகளம் is a political news platform focused on Tamil Nadu, India and global political developments, presenting important political stories, public issues and policy discussions in a clear and responsible format.",
        "full_description": "BAIRAVA ஆடுகளம் brings together political news, public policy debates, election insights and weekly digital newspaper editions delivering concise, balanced and responsible political journalism.",
        "division_type": "business",
        "icon_name": "radio",
        "static_image_path": "core/images/divisions/aadukalam.jpg",
        "target_url": "/businesses/aadukalam/",
        "accent_color": "#7B3426",
        "order": 7,
    },
    {
        "name": "BAIRAVA MEDIA",
        "slug": "media",
        "tagline": "MEANINGFUL STORIES, DIGITAL PRODUCTION & COMMUNICATION",
        "short_description": "Bairava Media focuses on storytelling, digital content, communication and media initiatives that connect businesses, communities and audiences.",
        "full_description": "Bairava Media produces engaging audiovisual content, corporate documentaries, podcast productions, and digital campaigns. We craft compelling visual narratives that inform, inspire, and foster meaningful connections between brands, communities, and audiences.",
        "division_type": "business",
        "icon_name": "film",
        "static_image_path": "core/images/divisions/media.jpg",
        "target_url": "/businesses/media/",
        "accent_color": "#241F1C",
        "order": 8,
    },
    {
        "name": "BHAIRAVA ASSOCIATION",
        "slug": "bhairava-association",
        "tagline": "COMMUNITY • CONNECTION • COLLABORATION",
        "short_description": "Building stronger communities through networking, collaboration, engagement and collective growth.",
        "full_description": "Bhairava Association is focused on bringing people, professionals, businesses and communities together through meaningful connections, collaboration and organized initiatives. The association aims to create a strong platform for networking, community engagement, knowledge sharing and collective development.",
        "division_type": "business",
        "icon_name": "users",
        "static_image_path": "core/images/divisions/association.jpg",
        "target_url": "/businesses/bhairava-association/",
        "accent_color": "#7C3B29",
        "order": 9,
    },
    {
        "name": "BAIRAVA TRUST",
        "slug": "trust",
        "tagline": "COMPASSIONATE SOCIAL CARE & DAILY COMMUNITY SERVICE",
        "short_description": "Bairava Trust focuses on social welfare and community-oriented initiatives designed to support people and create positive community impact.",
        "full_description": "Established as a registered non-profit charitable initiative, Bairava Trust operates daily Annadhanam (free meal distribution), full-time elder care shelters, educational scholarships for low-income students, and emergency disaster relief drives across Chennai and surrounding areas.",
        "division_type": "foundation_trust",
        "icon_name": "shield",
        "static_image_path": "core/images/divisions/trust.jpg",
        "target_url": "/trust/",
        "accent_color": "#7C3B29",
        "order": 10,
    },
]

division_objects = {}
valid_division_slugs = {d["slug"] for d in divisions_data}
for d_data in divisions_data:
    obj, created = BusinessDivision.objects.update_or_create(
        slug=d_data["slug"],
        defaults=d_data
    )
    division_objects[d_data["slug"]] = obj
    print(f"{'Created' if created else 'Updated'} division: {obj.name}")

# Clean up any non-canonical division records
for d in BusinessDivision.objects.exclude(slug__in=valid_division_slugs):
    print(f"Removing obsolete division: {d.name} ({d.slug})")
    d.delete()

# 2. POPULATE DIVISION OFFERINGS
offerings_data = {
    "finance": [
        {"title": "FINANCIAL ADVISORY & PLANNING", "badge": "CORE", "description": "Objective guidance for corporate cash flow management, growth planning, and prudent capital allocation.", "order": 1},
        {"title": "WORKING CAPITAL & BUSINESS ASSISTANCE", "badge": "COMMERCIAL", "description": "Structured consultation on managing operational overheads, vendor receivables, and business expansion cycles.", "order": 2},
        {"title": "ASSET & EQUIPMENT FINANCING ADVISORY", "badge": "ENTERPRISE", "description": "Assisting enterprises in evaluating machinery, commercial vehicle, and infrastructural funding options.", "order": 3},
        {"title": "CUSTOMER-FIRST TRANSPARENT TERMS", "badge": "INTEGRITY", "description": "Clear agreements without hidden clauses, straightforward timelines, and dedicated relationship managers.", "order": 4},
    ],
    "cloud-kitchen": [
        {"title": "SIGNATURE SOUTH INDIAN THALI", "badge": "BEST SELLER", "description": "Authentic recipes featuring hand-ground spices, sambar, rasam, seasonal vegetable poriyal, and crisp appalam.", "order": 1},
        {"title": "DUM BIRYANI SPECIALTIES", "badge": "SIGNATURE", "description": "Slow-cooked aromatic Seeraga Samba and Basmati rice preparations layered with tender spices and natural flavors.", "order": 2},
        {"title": "DAILY WHOLESOME MEAL BOXES", "badge": "SUBSCRIPTION", "description": "Balanced, hygienic daily lunch and dinner boxes crafted for corporate staff, students, and busy families.", "order": 3},
        {"title": "BULK CATERING & PARTY ORDERS", "badge": "EVENTS", "description": "Freshly cooked banquet meals and high-tea packages delivered hot with reliable event timelines.", "order": 4},
    ],
    "sports-club": [
        {"title": "INDOOR BADMINTON COURTS", "badge": "BWF STANDARD", "description": "Synthetic multi-court facility with professional glare-free LED floodlighting and tournament netting.", "order": 1},
        {"title": "STRENGTH & CONDITIONING ZONE", "badge": "FITNESS", "description": "Modern resistance training machines, free weights, agility tracks, and personalized fitness training regimens.", "order": 2},
        {"title": "JUNIOR COACHING ACADEMY", "badge": "TRAINING", "description": "Structured coaching modules led by certified coaches focusing on fundamentals, discipline, and match tactics.", "order": 3},
        {"title": "COMMUNITY LEAGUES & TOURNAMENTS", "badge": "EVENTS", "description": "Regular weekend friendly leagues and open tournaments encouraging healthy competitive spirit.", "order": 4},
    ],
    "aadukalam": [
        {"title": "TAMIL NADU & NATIONAL POLITICS", "badge": "POLITICS", "description": "Balanced coverage of state assembly debates, parliamentary proceedings, and election developments.", "order": 1},
        {"title": "POLICY & GOVERNANCE ANALYSIS", "badge": "GOVERNANCE", "description": "In-depth scrutiny of public administration, legislative decisions, and welfare reforms.", "order": 2},
        {"title": "WEEKLY DIGITAL NEWSPAPER", "badge": "EDITION", "description": "Curated weekly edition synthesizing the week's major political events, editorial perspectives, and civic issues.", "order": 3},
        {"title": "NON-PARTISAN CITIZEN PERSPECTIVES", "badge": "DEMOCRACY", "description": "Amplifying public interest concerns, institutional transparency, and democratic awareness.", "order": 4},
    ],
    "media": [
        {"title": "VIDEO & DOCUMENTARY PRODUCTION", "badge": "4K CINEMA", "description": "High-definition corporate films, brand profile stories, and community documentary features.", "order": 1},
        {"title": "DIGITAL CONTENT & PODCAST STUDIO", "badge": "STUDIO SETUP", "description": "Acoustically treated multi-mic studio spaces equipped for podcast recordings and panel discussions.", "order": 2},
        {"title": "EVENT & LIVE STREAM COVERAGE", "badge": "LIVE BROADCAST", "description": "Multi-camera live streaming and high-speed social media feeds for corporate summits and cultural festivals.", "order": 3},
        {"title": "BRAND STORYTELLING & PR STRATEGY", "badge": "STRATEGY", "description": "Narrative-driven press releases, promotional video campaigns, and social digital storytelling.", "order": 4},
    ],
    "bhairava-association": [
        {"title": "COMMUNITY NETWORKING", "badge": "NETWORKING", "description": "Building meaningful connections among members, professionals and local communities.", "order": 1},
        {"title": "PROFESSIONAL COLLABORATION", "badge": "COLLABORATION", "description": "Encouraging partnerships, knowledge sharing and opportunities for professional growth.", "order": 2},
        {"title": "COMMUNITY INITIATIVES", "badge": "INITIATIVES", "description": "Supporting programs and activities that contribute to community development.", "order": 3},
        {"title": "MEMBER ENGAGEMENT", "badge": "ENGAGEMENT", "description": "Creating events, meetings and activities that encourage participation and stronger relationships.", "order": 4},
        {"title": "KNOWLEDGE & NETWORKING", "badge": "KNOWLEDGE", "description": "Providing opportunities to exchange ideas, experience and practical knowledge.", "order": 5},
        {"title": "COLLECTIVE GROWTH", "badge": "GROWTH", "description": "Working together to create sustainable opportunities and positive community impact.", "order": 6},
    ],
    "foundation": [
        {"title": "EDUCATIONAL SCHOLARSHIPS & SUPPLIES", "badge": "EDUCATION", "description": "Direct financial aid for school fees, notebooks, uniform kits, and digital learning devices for deserving students.", "order": 1},
        {"title": "COMMUNITY WELFARE & MEDICAL SUPPORT", "badge": "WELFARE", "description": "Regular health screenings, eye checkup camps, and distribution of essential health provisions in underserved areas.", "order": 2},
        {"title": "VOCATIONAL SKILL WORKSHOPS", "badge": "EMPOWERMENT", "description": "Practical training programs in computer literacy, handicrafts, and tailoring to foster financial independence.", "order": 3},
        {"title": "YOUTH LEADERSHIP & MENTORSHIP", "badge": "MENTORSHIP", "description": "Career counseling sessions and personality development camps guiding teenagers toward higher education.", "order": 4},
    ]
}

for slug, items in offerings_data.items():
    if slug in division_objects:
        div = division_objects[slug]
        for item in items:
            DivisionOffering.objects.update_or_create(
                division=div,
                title=item["title"],
                defaults={
                    "badge": item["badge"],
                    "description": item["description"],
                    "order": item["order"]
                }
            )

# 3. POPULATE STATS
stats_data = [
    {"value": "20+", "label": "YEARS OF EXCELLENCE", "order": 1},
    {"value": "10", "label": "INTEGRATED DIVISIONS", "order": 2},
    {"value": "100+", "label": "DEDICATED TEAM MEMBERS", "order": 3},
    {"value": "500+", "label": "DAILY BENEFICIARIES", "order": 4},
]

valid_stat_labels = {s["label"] for s in stats_data}
# Remove old or duplicate stats
Stat.objects.exclude(label__in=valid_stat_labels).delete()

for s in stats_data:
    Stat.objects.update_or_create(
        label=s["label"],
        defaults=s
    )
print("Stats populated and deduplicated!")

# 4. POPULATE NEWS / RECENT HIGHLIGHTS
news_data = [
    {
        "category": "sports",
        "title": "BAIRAVA AADUKALAM STATE-LEVEL KABADDI CHAMPIONSHIP 2026",
        "description": "Over 24 top teams across Tamil Nadu competed with extraordinary spirit; trophies, sports scholarships, and merit certificates were awarded.",
        "link": ""
    },
    {
        "category": "trust",
        "title": "BAIRAVA TRUST EXPANDS DAILY ANNADHANAM INITIATIVE",
        "description": "Daily hot meal distribution capacity increased to serve over 500 senior citizens, underserved individuals, and hospital caregivers every single day.",
        "link": ""
    },
    {
        "category": "construction",
        "title": "COMPLETION MILESTONE: PREMIUM RESIDENTIAL COMPLEX HANDOVER",
        "description": "Successfully completed Bairava Heights in Anna Nagar ahead of schedule with earthquake-resistant RCC structure and bespoke architectural detailing.",
        "link": ""
    },
    {
        "category": "media",
        "title": "BAIRAVA MEDIA LAUNCHES COMMUNITY SPOTLIGHT DOCUMENTARY SERIES",
        "description": "A new digital storytelling initiative capturing inspiring real stories of grassroots entrepreneurs, athletes, and social change champions.",
        "link": ""
    }
]

valid_news_titles = {n["title"] for n in news_data}
# Remove old or duplicate news items
NewsItem.objects.exclude(title__in=valid_news_titles).delete()

for n in news_data:
    NewsItem.objects.update_or_create(
        title=n["title"],
        defaults=n
    )
print("News items populated and deduplicated!")

# 5. POPULATE MEDIA ARTICLES
media_articles = [
    {
        "title": "EMPOWERING LOCAL SPORTS: INSIDE THE BAIRAVA AADUKALAM MOVEMENT",
        "slug": "empowering-local-sports-bairava-aadukalam",
        "category": "SPORTS & COMMUNITY",
        "summary": "How Bairava Aadukalam is reviving indigenous sports and training the next generation of regional athletes in Tamil Nadu.",
        "content": "Traditional sports carry the cultural soul of our communities. Bairava Aadukalam was created to provide young talent with quality sports infrastructure, professional coaching, and tournament exposure.",
        "static_image_path": "core/images/divisions/aadukalam.jpg",
        "featured": True,
        "order": 1,
    },
    {
        "title": "SUSTAINABLE CONSTRUCTION PRACTICES SHAPING MODERN CHENNAI",
        "slug": "sustainable-construction-practices-chennai",
        "category": "ARCHITECTURE & BUILD",
        "summary": "An insightful look into how Bairava Construction & Land Promoters combines classic durability with energy-efficient construction design.",
        "content": "From soil testing and structural stability to solar integration and rainwater harvesting, every Bairava build is designed for longevity and environmental harmony.",
        "static_image_path": "core/images/divisions/construction.jpg",
        "featured": True,
        "order": 2,
    },
    {
        "title": "THE POWER OF COMPASSION: TWO DECADES OF BAIRAVA TRUST INITIATIVES",
        "slug": "power-of-compassion-two-decades-bairava-trust",
        "category": "SOCIAL IMPACT",
        "summary": "Exploring the journey of Bairava Trust in providing uninterrupted shelter, nutrition, and dignity to senior citizens in need.",
        "content": "Every day at the Bairava Senior Sanctuary begins with warm meals, medical checks, and genuine companionship. Community support remains the cornerstone of our mission.",
        "static_image_path": "core/images/divisions/trust.jpg",
        "featured": True,
        "order": 3,
    },
]

valid_media_slugs = {ma["slug"] for ma in media_articles}
MediaArticle.objects.exclude(slug__in=valid_media_slugs).delete()

for ma in media_articles:
    MediaArticle.objects.update_or_create(
        slug=ma["slug"],
        defaults=ma
    )
print("Media articles populated and deduplicated!")

# 6. POPULATE CONSTRUCTION PROJECTS (EXACTLY 4 DISTINCT PROJECTS WITH UNIQUE SLUGS & UNIQUE IMAGES)
construction_projects_data = [
    {
        "slug": "bairava-heights",
        "title": "BAIRAVA HEIGHTS",
        "location": "Anna Nagar, Chennai",
        "category": "residential",
        "status": "ongoing",
        "description": "A luxury multi-story residential apartment enclave designed with earthquake-resistant RCC structure, elegant glass balconies, and landscaped entrance plaza in prime Anna Nagar.",
        "completion_year": "2027",
        "built_up_area": "24,000 sq.ft",
        "image": "projects/bairava_heights.jpg",
        "order": 1,
    },
    {
        "slug": "bairava-tech-hub",
        "title": "BAIRAVA TECH HUB",
        "location": "Perungudi, OMR, Chennai",
        "category": "commercial",
        "status": "completed",
        "description": "Modern corporate IT tech park featuring contemporary glass curtain wall facade, energy-efficient floor plates, water reflection plaza, and high-speed infrastructure on Chennai's IT corridor.",
        "completion_year": "2025",
        "built_up_area": "48,000 sq.ft",
        "image": "projects/bairava_tech_hub.jpg",
        "order": 2,
    },
    {
        "slug": "the-golden-villas",
        "title": "THE GOLDEN VILLAS",
        "location": "East Coast Road (ECR), Chennai",
        "category": "villas",
        "status": "completed",
        "description": "Exclusive beachfront luxury villa estate featuring Italian marble finishes, private crystal swimming pools, private tropical gardens, and biometric smart-home security systems.",
        "completion_year": "2024",
        "built_up_area": "8,500 sq.ft",
        "image": "projects/golden_villas.jpg",
        "order": 3,
    },
    {
        "slug": "corporate-hq-renovation",
        "title": "CORPORATE HQ RENOVATION",
        "location": "Nungambakkam, Chennai",
        "category": "interiors",
        "status": "completed",
        "description": "Comprehensive structural restoration, modern architectural louver facade upgrade, acoustic glass executive suites, and luxury corporate reception interiors.",
        "completion_year": "2024",
        "built_up_area": "16,200 sq.ft",
        "image": "projects/corporate_hq.jpg",
        "order": 4,
    },
]

valid_project_slugs = {cp["slug"] for cp in construction_projects_data}
valid_project_titles = {cp["title"] for cp in construction_projects_data}

# Safely remove any duplicate or obsolete construction project records
for p in ConstructionProject.objects.all():
    if p.slug not in valid_project_slugs and p.title not in valid_project_titles:
        print(f"Removing obsolete construction project: {p.title} (ID: {p.id})")
        p.delete()
    elif not p.slug:
        # If legacy record without slug, remove it so it's cleanly recreated with slug
        print(f"Removing legacy un-slugged project: {p.title} (ID: {p.id})")
        p.delete()

for cp in construction_projects_data:
    p_obj, created = ConstructionProject.objects.update_or_create(
        slug=cp["slug"],
        defaults=cp
    )
    print(f"{'Created' if created else 'Updated'} construction project: {p_obj.title} (Slug: {p_obj.slug})")

# Clean up any leftover records that exceed the 4 canonical projects
for p in ConstructionProject.objects.exclude(slug__in=valid_project_slugs):
    print(f"Removing excess construction project: {p.title} ({p.slug})")
    p.delete()

print(f"Construction projects verified count: {ConstructionProject.objects.count()}")

# 7. POPULATE LEGAL ASSOCIATES DATA
legal_practice_data = [
    {
        "title": "CORPORATE & BUSINESS LAW",
        "category": "notice",
        "turnaround_time": "ADVISORY & DRAFTING",
        "description": "Legal support for business operations, agreements, corporate documentation and commercial matters.",
        "order": 1,
    },
    {
        "title": "CONTRACTS & AGREEMENTS",
        "category": "notice",
        "turnaround_time": "REVIEW & STRUCTURING",
        "description": "Assistance with reviewing, preparing and organizing business contracts and agreements.",
        "order": 2,
    },
    {
        "title": "PROPERTY & REAL ESTATE LAW",
        "category": "property",
        "turnaround_time": "TITLE & DUE DILIGENCE",
        "description": "Legal support related to property transactions, documentation and real-estate matters.",
        "order": 3,
    },
    {
        "title": "COMPLIANCE & DOCUMENTATION",
        "category": "notice",
        "turnaround_time": "STATUTORY AUDIT",
        "description": "Support for maintaining appropriate legal documentation and business compliance processes.",
        "order": 4,
    },
    {
        "title": "LEGAL ADVISORY",
        "category": "notice",
        "turnaround_time": "STRATEGIC COUNSEL",
        "description": "Professional legal guidance to help businesses make informed decisions and manage legal requirements.",
        "order": 5,
    },
    {
        "title": "DISPUTE SUPPORT",
        "category": "recovery",
        "turnaround_time": "COORDINATION & ADVOCACY",
        "description": "Assistance in understanding legal matters and coordinating with appropriate legal professionals when disputes arise.",
        "order": 6,
    },
]

valid_legal_practice_titles = {lp["title"] for lp in legal_practice_data}
LegalPracticeDetail.objects.exclude(title__in=valid_legal_practice_titles).delete()

for lp in legal_practice_data:
    LegalPracticeDetail.objects.update_or_create(
        title=lp["title"],
        defaults=lp
    )
print("Legal practice details populated and deduplicated!")

legal_services_data = [
    {"description": "Corporate & Business Law Support", "tag": "CORPORATE", "order": 1},
    {"description": "Contracts, MOUs & Commercial Agreements", "tag": "CONTRACTS", "order": 2},
    {"description": "Property Title Verification & Due Diligence", "tag": "PROPERTY", "order": 3},
    {"description": "Business Compliance & Legal Documentation", "tag": "COMPLIANCE", "order": 4},
    {"description": "Strategic Business Legal Advisory", "tag": "ADVISORY", "order": 5},
    {"description": "Commercial Dispute Coordination & Resolution", "tag": "DISPUTE", "order": 6},
]

for ls in legal_services_data:
    LegalService.objects.update_or_create(
        description=ls["description"],
        defaults=ls
    )
print("Legal services populated!")

print("All Bairava Groups database models successfully populated and synced!")
