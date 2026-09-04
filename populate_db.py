import os
import django

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
        "name": "Bairava Foundation",
        "slug": "foundation",
        "tagline": "Empowering Communities, Nurturing Potential",
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
        "name": "Bairava Finance",
        "slug": "finance",
        "tagline": "Transparent, Professional & Responsible Financial Solutions",
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
        "name": "Bairava Construction & Promoters",
        "slug": "construction",
        "tagline": "Mastering Structural Excellence & Architectural Integrity",
        "short_description": "Bairava Construction & Promoters focuses on residential, commercial and property development projects with attention to planning, quality and dependable execution.",
        "full_description": "With over two decades of engineering and civil construction excellence in Chennai, Bairava Construction & Promoters manages turnkey residential complexes, luxury individual villas, commercial buildings, and bespoke interior transformations from concept blueprint to flawless handover.",
        "division_type": "business",
        "icon_name": "building",
        "static_image_path": "core/images/divisions/construction.jpg",
        "target_url": "/businesses/construction/",
        "accent_color": "#7C3B29",
        "order": 3,
    },
    {
        "name": "Bairava Cloud Kitchen",
        "slug": "cloud-kitchen",
        "tagline": "Hygienic, Authentic & Flavorful Culinary Experiences",
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
        "name": "Bairava Sports Club",
        "slug": "sports-club",
        "tagline": "Nurturing Athletic Talent & Fitness Communities",
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
        "name": "Bairava Event Management",
        "slug": "event-management",
        "tagline": "Turnkey Event Experiences & Flawless Celebrations",
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
        "name": "Bairava Aadukalam",
        "slug": "aadukalam",
        "tagline": "Celebrating Traditional Sports & Cultural Games",
        "short_description": "Bairava Aadukalam is a platform for sports, recreation, traditional activities and community participation, bringing people together through engaging experiences.",
        "full_description": "Rooted in Tamil Nadu's rich heritage of indigenous games, Bairava Aadukalam hosts regional Kabaddi leagues, Silambam training, rural athletic festivals, and recreational events that preserve traditional sports culture and unite communities in healthy competition.",
        "division_type": "business",
        "icon_name": "trophy",
        "static_image_path": "core/images/divisions/aadukalam.jpg",
        "target_url": "/businesses/aadukalam/",
        "accent_color": "#7C3B29",
        "order": 7,
    },
    {
        "name": "Bairava Trust",
        "slug": "trust",
        "tagline": "Compassionate Social Care & Daily Community Service",
        "short_description": "Bairava Trust focuses on social welfare and community-oriented initiatives designed to support people and create positive community impact.",
        "full_description": "Established as a registered non-profit charitable initiative, Bairava Trust operates daily Annadhanam (free meal distribution), full-time elder care shelters, educational scholarships for low-income students, and emergency disaster relief drives across Chennai and surrounding areas.",
        "division_type": "foundation_trust",
        "icon_name": "shield",
        "static_image_path": "core/images/divisions/trust.jpg",
        "target_url": "/trust/",
        "accent_color": "#7C3B29",
        "order": 8,
    },
    {
        "name": "Bairava Media",
        "slug": "media",
        "tagline": "Meaningful Stories, Digital Production & Communication",
        "short_description": "Bairava Media focuses on storytelling, digital content, communication and media initiatives that connect businesses, communities and audiences.",
        "full_description": "Bairava Media produces engaging audiovisual content, corporate documentaries, podcast productions, and digital campaigns. We craft compelling visual narratives that inform, inspire, and foster meaningful connections between brands, communities, and audiences.",
        "division_type": "business",
        "icon_name": "film",
        "static_image_path": "core/images/divisions/media.jpg",
        "target_url": "/businesses/media/",
        "accent_color": "#241F1C",
        "order": 9,
    },
]

division_objects = {}
for d_data in divisions_data:
    obj, created = BusinessDivision.objects.update_or_create(
        slug=d_data["slug"],
        defaults=d_data
    )
    division_objects[d_data["slug"]] = obj
    print(f"{'Created' if created else 'Updated'} division: {obj.name}")

# 2. POPULATE DIVISION OFFERINGS
offerings_data = {
    "finance": [
        {"title": "Financial Advisory & Planning", "badge": "Core", "description": "Objective guidance for corporate cash flow management, growth planning, and prudent capital allocation.", "order": 1},
        {"title": "Working Capital & Business Assistance", "badge": "Commercial", "description": "Structured consultation on managing operational overheads, vendor receivables, and business expansion cycles.", "order": 2},
        {"title": "Asset & Equipment Financing Advisory", "badge": "Enterprise", "description": "Assisting enterprises in evaluating machinery, commercial vehicle, and infrastructural funding options.", "order": 3},
        {"title": "Customer-First Transparent Terms", "badge": "Integrity", "description": "Clear agreements without hidden clauses, straightforward timelines, and dedicated relationship managers.", "order": 4},
    ],
    "cloud-kitchen": [
        {"title": "Signature South Indian Thali", "badge": "Best Seller", "description": "Authentic recipes featuring hand-ground spices, sambar, rasam, seasonal vegetable poriyal, and crisp appalam.", "order": 1},
        {"title": "Dum Biryani Specialties", "badge": "Signature", "description": "Slow-cooked aromatic Seeraga Samba and Basmati rice preparations layered with tender spices and natural flavors.", "order": 2},
        {"title": "Daily Wholesome Meal Boxes", "badge": "Subscription", "description": "Balanced, hygienic daily lunch and dinner boxes crafted for corporate staff, students, and busy families.", "order": 3},
        {"title": "Bulk Catering & Party Orders", "badge": "Events", "description": "Freshly cooked banquet meals and high-tea packages delivered hot with reliable event timelines.", "order": 4},
    ],
    "sports-club": [
        {"title": "Indoor Badminton Courts", "badge": "BWF Standard", "description": "Synthetic multi-court facility with professional glare-free LED floodlighting and tournament netting.", "order": 1},
        {"title": "Strength & Conditioning Zone", "badge": "Fitness", "description": "Modern resistance training machines, free weights, agility tracks, and personalized fitness training regimens.", "order": 2},
        {"title": "Junior Coaching Academy", "badge": "Training", "description": "Structured coaching modules led by certified coaches focusing on fundamentals, discipline, and match tactics.", "order": 3},
        {"title": "Community Leagues & Tournaments", "badge": "Events", "description": "Regular weekend friendly leagues and open tournaments encouraging healthy competitive spirit.", "order": 4},
    ],
    "aadukalam": [
        {"title": "Kabaddi Tournaments & Coaching", "badge": "Heritage Sport", "description": "Professional clay court training, safety gear guidance, and regular district-level tournament hosting.", "order": 1},
        {"title": "Silambam & Traditional Martial Arts", "badge": "Cultural Arts", "description": "Authentic staff-spinning and ancient self-defense art forms taught by seasoned traditional practitioners.", "order": 2},
        {"title": "Rural & Recreational Sports Galas", "badge": "Community", "description": "Multi-discipline athletic festivals featuring Kho-Kho, volleyball, tug of war, and indigenous field games.", "order": 3},
        {"title": "Youth Fitness Camps", "badge": "Development", "description": "Open ground conditioning drills and fitness workshops building stamina and discipline among local youth.", "order": 4},
    ],
    "media": [
        {"title": "Video & Documentary Production", "badge": "4K Cinema", "description": "High-definition corporate films, brand profile stories, and community documentary features.", "order": 1},
        {"title": "Digital Content & Podcast Studio", "badge": "Studio Setup", "description": "Acoustically treated multi-mic studio spaces equipped for podcast recordings and panel discussions.", "order": 2},
        {"title": "Event & Live Stream Coverage", "badge": "Live Broadcast", "description": "Multi-camera live streaming and high-speed social media feeds for corporate summits and cultural festivals.", "order": 3},
        {"title": "Brand Storytelling & PR Strategy", "badge": "Strategy", "description": "Narrative-driven press releases, promotional video campaigns, and social digital storytelling.", "order": 4},
    ],
    "foundation": [
        {"title": "Educational Scholarships & Supplies", "badge": "Education", "description": "Direct financial aid for school fees, notebooks, uniform kits, and digital learning devices for deserving students.", "order": 1},
        {"title": "Community Welfare & Medical Support", "badge": "Welfare", "description": "Regular health screenings, eye checkup camps, and distribution of essential health provisions in underserved areas.", "order": 2},
        {"title": "Vocational Skill Workshops", "badge": "Empowerment", "description": "Practical training programs in computer literacy, handicrafts, and tailoring to foster financial independence.", "order": 3},
        {"title": "Youth Leadership & Mentorship", "badge": "Mentorship", "description": "Career counseling sessions and personality development camps guiding teenagers toward higher education.", "order": 4},
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
    {"value": "20+", "label": "Years of Excellence", "order": 1},
    {"value": "9", "label": "Integrated Divisions", "order": 2},
    {"value": "100+", "label": "Dedicated Team Members", "order": 3},
    {"value": "500+", "label": "Daily Beneficiaries", "order": 4},
]

for s in stats_data:
    Stat.objects.update_or_create(
        label=s["label"],
        defaults=s
    )
print("Stats populated!")

# 4. POPULATE NEWS / RECENT HIGHLIGHTS
news_data = [
    {
        "category": "sports",
        "title": "Bairava Aadukalam State-Level Kabaddi Championship 2026",
        "description": "Over 24 top teams across Tamil Nadu competed with extraordinary spirit; trophies, sports scholarships, and merit certificates were awarded.",
        "link": ""
    },
    {
        "category": "trust",
        "title": "Bairava Trust Expands Daily Annadhanam Initiative",
        "description": "Daily hot meal distribution capacity increased to serve over 500 senior citizens, underserved individuals, and hospital caregivers every single day.",
        "link": ""
    },
    {
        "category": "construction",
        "title": "Completion Milestone: Premium Residential Complex Handover",
        "description": "Successfully completed Bairava Heights in Anna Nagar ahead of schedule with earthquake-resistant RCC structure and bespoke architectural detailing.",
        "link": ""
    },
    {
        "category": "media",
        "title": "Bairava Media Launches Community Spotlight Documentary Series",
        "description": "A new digital storytelling initiative capturing inspiring real stories of grassroots entrepreneurs, athletes, and social change champions.",
        "link": ""
    }
]

for n in news_data:
    NewsItem.objects.update_or_create(
        title=n["title"],
        defaults=n
    )
print("News items populated!")

# 5. POPULATE MEDIA ARTICLES
media_articles = [
    {
        "title": "Empowering Local Sports: Inside the Bairava Aadukalam Movement",
        "slug": "empowering-local-sports-bairava-aadukalam",
        "category": "Sports & Community",
        "summary": "How Bairava Aadukalam is reviving indigenous sports and training the next generation of regional athletes in Tamil Nadu.",
        "content": "Traditional sports carry the cultural soul of our communities. Bairava Aadukalam was created to provide young talent with quality sports infrastructure, professional coaching, and tournament exposure.",
        "static_image_path": "core/images/divisions/aadukalam.jpg",
        "featured": True,
        "order": 1,
    },
    {
        "title": "Sustainable Construction Practices Shaping Modern Chennai",
        "slug": "sustainable-construction-practices-chennai",
        "category": "Architecture & Build",
        "summary": "An insightful look into how Bairava Construction & Promoters combines classic durability with energy-efficient construction design.",
        "content": "From soil testing and structural stability to solar integration and rainwater harvesting, every Bairava build is designed for longevity and environmental harmony.",
        "static_image_path": "core/images/divisions/construction.jpg",
        "featured": True,
        "order": 2,
    },
    {
        "title": "The Power of Compassion: Two Decades of Bairava Trust Initiatives",
        "slug": "power-of-compassion-two-decades-bairava-trust",
        "category": "Social Impact",
        "summary": "Exploring the journey of Bairava Trust in providing uninterrupted shelter, nutrition, and dignity to senior citizens in need.",
        "content": "Every day at the Bairava Senior Sanctuary begins with warm meals, medical checks, and genuine companionship. Community support remains the cornerstone of our mission.",
        "static_image_path": "core/images/divisions/trust.jpg",
        "featured": True,
        "order": 3,
    },
]

for ma in media_articles:
    MediaArticle.objects.update_or_create(
        slug=ma["slug"],
        defaults=ma
    )
print("Media articles populated!")

print("All Bairava Groups database models successfully populated and synced!")
