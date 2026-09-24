import json
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from core.models import BusinessDivision, DivisionOffering, Stat, NewsItem
from construction.models import ConstructionProject, Service as ConstructionService
from trust.models import TrustActivityItem, TrustProgram
from events.models import EventPortfolioItem, EventType
from services.rag_retriever import retrieve_website_context, get_suggested_questions
from services.ai_chat import process_chat_message


class AIChatbotTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create business divisions
        self.div_construction = BusinessDivision.objects.create(
            name="Bairava Construction & Land Promoters",
            slug="construction",
            tagline="Mastering Structural Excellence",
            short_description="Turnkey construction in Chennai.",
            full_description="Over two decades of engineering excellence in Chennai.",
            division_type="business",
            order=1
        )
        self.div_foundation = BusinessDivision.objects.create(
            name="Bairava Foundation",
            slug="foundation",
            tagline="Empowering Communities",
            short_description="Community welfare and educational support.",
            full_description="Dedicated to sustainable community empowerment.",
            division_type="foundation_trust",
            order=2
        )
        self.div_trust = BusinessDivision.objects.create(
            name="Bairava Trust",
            slug="trust",
            tagline="Compassionate Social Care",
            short_description="Daily Annadhanam and elder care.",
            full_description="Daily Annadhanam serving 500+ daily meals.",
            division_type="foundation_trust",
            order=3
        )
        self.div_finance = BusinessDivision.objects.create(
            name="Bairava Finance",
            slug="finance",
            tagline="Transparent Financial Solutions",
            short_description="Responsible financial advisory.",
            full_description="Tailored financial planning and capital advisory.",
            division_type="business",
            order=4
        )

        # Create Construction project and service
        self.project = ConstructionProject.objects.create(
            title="Bairava Heights",
            slug="bairava-heights",
            location="Anna Nagar, Chennai",
            category="residential",
            status="completed",
            description="Premium residential complex.",
            built_up_area="24,000 sq.ft"
        )
        self.const_service = ConstructionService.objects.create(
            title="Civil & Structural Construction",
            description="Turnkey architectural build."
        )

        # Create Trust activities
        self.trust_act = TrustActivityItem.objects.create(
            title="Daily Free Meals",
            category="annadhanam",
            impact_stat="500+ meals daily",
            description="Nutritious meals served every single day."
        )

    def test_suggestions_endpoint(self):
        """Test GET /api/chat/suggestions/ returns contextual suggestions."""
        url = reverse('core:chat_suggestions_api')

        # Homepage suggestions
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("suggestions", data)
        self.assertTrue(len(data["suggestions"]) >= 3)
        self.assertIn("What businesses does Bairava Groups operate?", data["suggestions"])

        # Construction page suggestions
        response = self.client.get(url + '?current_page=/businesses/construction/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("What projects are available?", data["suggestions"])

        # Trust page suggestions
        response = self.client.get(url + '?current_page=/trust/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("What activities does the Trust conduct?", data["suggestions"])

    def test_chat_api_validation(self):
        """Test POST /api/chat/ request validation for bad payloads."""
        url = reverse('core:chat_api')

        # Invalid JSON
        response = self.client.post(url, "not a json string", content_type="application/json")
        self.assertEqual(response.status_code, 400)

        # Empty message
        response = self.client.post(url, json.dumps({"message": ""}), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        # Exceedingly long message
        long_message = "x" * 1001
        response = self.client.post(url, json.dumps({"message": long_message}), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_chat_api_business_divisions_query(self):
        """Test asking about business divisions."""
        url = reverse('core:chat_api')
        payload = {
            "message": "What businesses does Bairava Groups have?",
            "conversation_id": "test_conv_1"
        }
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("Bairava Finance", data["response"])
        self.assertIn("Bairava Construction", data["response"])
        self.assertIn("Bairava Foundation", data["response"])
        self.assertIn("Bairava Trust", data["response"])

    def test_chat_api_construction_query(self):
        """Test asking about construction & projects."""
        url = reverse('core:chat_api')
        payload = {
            "message": "What projects does Bairava Construction have?",
            "conversation_id": "test_conv_2",
            "current_page": "/businesses/construction/"
        }
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("Bairava Construction", data["response"])
        self.assertIn("Bairava Heights", data["response"])

    def test_chat_api_trust_and_annadhanam_query(self):
        """Test asking about Bairava Trust activities and Annadhanam."""
        url = reverse('core:chat_api')
        payload = {
            "message": "Tell me about Bairava Trust activities and Annadhanam",
            "conversation_id": "test_conv_3"
        }
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("Bairava Charitable Trust", data["response"])
        self.assertIn("Annadhanam", data["response"])

    def test_chat_api_contact_query(self):
        """Test asking about contact information."""
        url = reverse('core:chat_api')
        payload = {
            "message": "How can I contact Bairava Groups?",
            "conversation_id": "test_conv_4"
        }
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("Contact Us", data["response"])
        self.assertIn("+91 99417 57555", data["response"])

    def test_chat_api_no_hallucination_for_unknown_query(self):
        """Test that unknown queries not present in DB return strict refusal."""
        url = reverse('core:chat_api')
        payload = {
            "message": "What is the stock market ticker symbol for Bairava in New York?",
            "conversation_id": "test_conv_5"
        }
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("I don't have that information in the Bairava Groups website data", data["response"])

    def test_chat_api_cloud_kitchen_query(self):
        """Test asking about cloud kitchen food and menu."""
        url = reverse('core:chat_api')
        payload = {"message": "What does Bairava Cloud Kitchen offer?", "conversation_id": "test_conv_6"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Bairava Cloud Kitchen", data["response"])
        self.assertIn("Thali", data["response"])

    def test_chat_api_sports_club_query(self):
        """Test asking about sports club."""
        url = reverse('core:chat_api')
        payload = {"message": "What sports facilities are available at Bairava Sports Club?", "conversation_id": "test_conv_7"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Bairava Sports Club", data["response"])
        self.assertIn("Badminton", data["response"])

    def test_chat_api_aadukalam_query(self):
        """Test asking about Aadukalam."""
        url = reverse('core:chat_api')
        payload = {"message": "What is Bairava Aadukalam?", "conversation_id": "test_conv_8"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("BAIRAVA", data["response"].upper())
        self.assertTrue("ஆடுகளம்" in data["response"] or "Aadukalam" in data["response"] or "news" in data["response"].lower())

    def test_chat_api_event_management_query(self):
        """Test asking about event management."""
        url = reverse('core:chat_api')
        payload = {"message": "What types of events do you manage?", "conversation_id": "test_conv_9"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Bairava Event Management", data["response"])
        self.assertIn("Weddings", data["response"])

    def test_chat_api_media_query(self):
        """Test asking about Bairava Media."""
        url = reverse('core:chat_api')
        payload = {"message": "What does Bairava Media do?", "conversation_id": "test_conv_10"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Bairava Media", data["response"])
        self.assertIn("Documentary", data["response"])

    def test_chat_api_rate_limiting(self):
        """Test that excessive requests trigger rate limiting (HTTP 429)."""
        url = reverse('core:chat_api')
        # Simulate 35 requests within session
        session = self.client.session
        import time
        now = time.time()
        session['ai_chat_request_timestamps'] = [now - 10] * 32
        session.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = session.session_key

        payload = {"message": "Hello", "conversation_id": "test_conv_rate"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 429)

    def test_rag_retriever_context(self):
        """Test RAG retriever output directly."""
        context_data = retrieve_website_context(
            user_query="construction",
            current_page="/businesses/construction/"
        )
        self.assertIn("context_text", context_data)
        self.assertIn("Bairava Construction", context_data["context_text"])
        self.assertIn("Bairava Heights", context_data["context_text"])


class FuturePlanTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()

    def test_future_plan_page_status_and_content(self):
        """Test GET /future-plan/ returns 200 and contains all required vision & venture details."""
        from core.views import future_plan_view
        req = self.rf.get(reverse('core:future_plan'))
        response = future_plan_view(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Headings & Vision
        self.assertIn("OUR VISION AHEAD", content)
        self.assertIn("FUTURE PLAN", content)
        self.assertIn("Expanding our horizons to create more value", content)
        self.assertIn("TWO NEW BUSINESSES COMING SOON UNDER BAIRAVA GROUPS", content)

        # Business 1: Bairava Water Solutions
        self.assertIn("BAIRAVA WATER SOLUTIONS", content)
        self.assertIn("Pure Water. Healthier Lives.", content)
        self.assertIn("Packaged drinking water and water-can distribution", content)
        self.assertIn("Clean &amp; Safe Drinking Water", content)
        self.assertIn("A Healthier Tomorrow with Bairava.", content)

        # Business 2: Bairava Jewellery
        self.assertIn("BAIRAVA JEWELLERY", content)
        self.assertIn("Timeless Beauty. Lasting Value.", content)
        self.assertIn("Jewellery retail and elegant handcrafted collections", content)
        self.assertIn("Gold Jewellery &amp; Traditional Collections", content)
        self.assertIn("Tradition Today. For Generations Tomorrow.", content)

        # Coming Soon indicators
        self.assertIn("COMING SOON", content)

        # Footer copyright test
        self.assertIn("© 2026 La Fortune Makers. All rights reserved. Chennai, Tamil Nadu.", content)

    def test_future_plan_nav_in_all_pages(self):
        """Test that Future Plan appears in the header between Businesses and Foundation & Trust."""
        from core.views import home
        req = self.rf.get(reverse('core:home'))
        response = home(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn("FUTURE PLAN", content)
        self.assertIn("BAIRAVA WATER SOLUTIONS", content)
        self.assertIn("BAIRAVA JEWELLERY", content)

        # Check navigation ordering in HTML
        businesses_pos = content.find("BUSINESSES")
        future_plan_pos = content.find("FUTURE PLAN")
        foundation_pos = content.find("FOUNDATION &amp; TRUST")
        self.assertTrue(businesses_pos < future_plan_pos < foundation_pos)

    def test_future_plan_suggestions(self):
        """Test chatbot suggestions for future-plan page."""
        from core.views_chat import chat_suggestions_api
        req = self.rf.get(reverse('core:chat_suggestions_api') + '?current_page=/future-plan/')
        response = chat_suggestions_api(req)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIn("What is Bairava Water Solutions?", data["suggestions"])


class BairavaLawAssociatesTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_law, _ = BusinessDivision.objects.update_or_create(
            slug="law-associates",
            defaults={
                "name": "BAIRAVA LAW ASSOCIATES",
                "tagline": "Your Trusted Legal Partner.",
                "short_description": "Delivering practical, professional and client-focused legal solutions for individuals, businesses and organizations with integrity, expertise and commitment.",
                "full_description": "Bairava Law Associates provides practical legal guidance and professional support for individuals, businesses and organizations.",
                "division_type": "business",
                "order": 8,
            }
        )
        practice_areas = [
            ("CORPORATE & COMMERCIAL LAW", "Business structuring, contracts, agreements and compliance support.", "contracts", 1),
            ("CIVIL LAW", "Legal guidance, dispute resolution, documentation and representation support.", "dispute", 2),
            ("PROPERTY & REAL ESTATE LAW", "Property documentation, agreements, due diligence and property-related legal matters.", "property", 3),
            ("CRIMINAL LAW", "Legal guidance and representation relating to criminal proceedings and defence matters.", "defense", 4),
            ("FAMILY & PERSONAL LAW", "Professional guidance for family and personal legal matters.", "family", 5),
            ("LEGAL DOCUMENTATION", "Drafting, reviewing and organizing legal agreements, notices and documentation.", "documentation", 6),
            ("LABOUR & EMPLOYMENT LAW", "Guidance relating to employment matters, workplace issues, contracts and compliance.", "employment", 7),
            ("LEGAL CONSULTATION", "Professional consultation for individuals, businesses and organizations.", "consultation", 8),
        ]
        for title, desc, badge, order in practice_areas:
            DivisionOffering.objects.update_or_create(
                division=self.div_law,
                title=title,
                defaults={
                    "description": desc,
                    "badge": badge,
                    "order": order
                }
            )

    def test_law_associates_page_status_and_content(self):
        """Test GET /businesses/law-associates/ returns 200 and renders exact legal content and structure."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'law-associates'}))
        response = business_detail(req, slug='law-associates')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # SEO & Headings
        self.assertIn("Bairava Law Associates | Professional Legal Guidance", content)
        self.assertIn("HOME", content)
        self.assertIn("LEGAL", content)
        self.assertIn("BAIRAVA LAW ASSOCIATES", content)
        self.assertIn("JUSTICE", content)
        self.assertIn("INTEGRITY", content)
        self.assertIn("SOLUTIONS", content)
        self.assertIn("LEGAL GUIDANCE &amp; ADVISORY", content)
        self.assertIn('"Your Trusted Legal Partner."', content)
        self.assertIn("Delivering practical, professional and client-focused legal solutions", content)

        # Buttons
        self.assertIn("GET LEGAL CONSULTATION", content)
        self.assertIn("OUR PRACTICE AREAS", content)

        # Restored Exact Logo
        self.assertIn("core/images/logos/bairava-law-associates-logo.png", content)

        # Trust Strip
        self.assertIn("EXPERIENCED TEAM", content)
        self.assertIn("Skilled legal professionals", content)
        self.assertIn("TRUSTED ADVISORY", content)
        self.assertIn("Practical &amp; transparent legal guidance", content)
        self.assertIn("CLIENT FOCUSED", content)
        self.assertIn("Personalized legal solutions", content)
        self.assertIn("RESULT ORIENTED", content)
        self.assertIn("Professional and responsible legal support", content)

        # 8 Practice Areas
        self.assertIn("OUR PRACTICE AREAS", content)
        self.assertIn("Comprehensive Legal Solutions", content)
        self.assertIn("CORPORATE &amp; COMMERCIAL LAW", content)
        self.assertIn("CIVIL LAW", content)
        self.assertIn("PROPERTY &amp; REAL ESTATE LAW", content)
        self.assertIn("CRIMINAL LAW", content)
        self.assertIn("FAMILY &amp; PERSONAL LAW", content)
        self.assertIn("LEGAL DOCUMENTATION", content)
        self.assertIn("LABOUR &amp; EMPLOYMENT LAW", content)
        self.assertIn("LEGAL CONSULTATION", content)

        # About Section
        self.assertIn("ABOUT BAIRAVA LAW ASSOCIATES", content)
        self.assertIn("Committed to Justice, Driven by Integrity", content)
        self.assertIn("INTEGRITY", content)
        self.assertIn("EXPERTISE", content)
        self.assertIn("CLIENT FOCUS", content)
        self.assertIn("LONG-TERM SUPPORT", content)

        # Consultation CTA & Form
        self.assertIn("NEED LEGAL GUIDANCE?", content)
        self.assertIn("Speak with Bairava Law Associates for professional legal consultation and practical guidance.", content)
        self.assertIn("REQUEST CONSULTATION", content)
        self.assertIn("CONTACT US", content)

        # Verify removal of old Association identity
        self.assertNotIn("BAIRAVA ASSOCIATION", content)
        self.assertNotIn("Community • Connection • Collaboration", content)
        self.assertNotIn("Professional Growth", content)
        self.assertNotIn("Social Impact", content)

    def test_legal_url_routes_to_law_associates(self):
        """Test GET /legal/ successfully redirects to Bairava Law Associates."""
        response = self.client.get('/legal/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, reverse('core:business_detail', kwargs={'slug': 'law-associates'}))

    def test_legacy_routes_redirect_to_law_associates(self):
        """Test legacy routes redirect to /businesses/law-associates/."""
        for path in ['/association/', '/businesses/association/', '/businesses/legal/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 301)
            self.assertEqual(response.url, reverse('core:business_detail', kwargs={'slug': 'law-associates'}))

    def test_navbar_and_footer_contain_bairava_law_associates(self):
        """Test that navbar and footer contain Legal and Bairava Law Associates links."""
        from core.views import home
        req = self.rf.get(reverse('core:home'))
        response = home(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn("LEGAL", content)
        self.assertIn("BAIRAVA LAW ASSOCIATES", content)
        self.assertNotIn("BAIRAVA ASSOCIATION", content)
        self.assertIn("BAIRAVA FINANCE", content)
        self.assertIn("CENTRAL KITCHEN", content)
        self.assertIn("BAIRAVA SPORTS CLUB", content)
        self.assertIn("BAIRAVA MEDIA", content)

    def test_chat_api_law_associates_query(self):
        """Test asking AI chatbot about Bairava Law Associates."""
        url = reverse('core:chat_api')
        payload = {"message": "Tell me about Bairava Law Associates and your practice areas", "conversation_id": "test_conv_law"}
        response = self.client.post(url, json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Bairava Law Associates", data["response"])
        self.assertIn("Corporate & Commercial Law", data["response"])
        self.assertIn("Civil Law", data["response"])


class ConstructionProjectsTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        # Seed the exact 4 canonical projects
        projects_data = [
            {"slug": "bairava-heights", "title": "BAIRAVA HEIGHTS", "location": "Anna Nagar, Chennai", "category": "residential", "status": "ongoing", "description": "Luxury multi-story residential enclave.", "completion_year": "2027", "built_up_area": "24,000 sq.ft", "order": 1},
            {"slug": "bairava-tech-hub", "title": "BAIRAVA TECH HUB", "location": "Perungudi, OMR, Chennai", "category": "commercial", "status": "completed", "description": "Modern corporate IT tech park.", "completion_year": "2025", "built_up_area": "48,000 sq.ft", "order": 2},
            {"slug": "the-golden-villas", "title": "THE GOLDEN VILLAS", "location": "ECR, Chennai", "category": "villas", "status": "completed", "description": "Exclusive beachfront luxury villa estate.", "completion_year": "2024", "built_up_area": "8,500 sq.ft", "order": 3},
            {"slug": "corporate-hq-renovation", "title": "CORPORATE HQ RENOVATION", "location": "Nungambakkam, Chennai", "category": "interiors", "status": "completed", "description": "Comprehensive structural restoration.", "completion_year": "2024", "built_up_area": "16,200 sq.ft", "order": 4},
        ]
        for data in projects_data:
            ConstructionProject.objects.create(**data)

    def test_exactly_four_projects_rendered_without_duplicates(self):
        """Test GET /construction/ returns 200 and renders exactly 4 unique project cards without duplicates."""
        from construction.views import project_list
        req = self.rf.get(reverse('construction:project_list'))
        response = project_list(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertEqual(ConstructionProject.objects.count(), 4)
        
        # Check each project appears exactly once in the rendered HTML
        self.assertEqual(content.count("<h4>BAIRAVA HEIGHTS</h4>"), 1)
        self.assertEqual(content.count("<h4>BAIRAVA TECH HUB</h4>"), 1)
        self.assertEqual(content.count("<h4>THE GOLDEN VILLAS</h4>"), 1)
        self.assertEqual(content.count("<h4>CORPORATE HQ RENOVATION</h4>"), 1)


class JKKitchenTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_kitchen = BusinessDivision.objects.create(
            name="CENTRAL KITCHEN",
            slug="cloud-kitchen",
            tagline="SUSTAINABLE FOOD & HOSPITALITY SOLUTIONS",
            short_description="Central Kitchen delivers sustainable food and hospitality solutions for corporate professionals, students, healthcare teams and industrial workforces.",
            full_description="Operating state-of-the-art commercial culinary hubs, Central Kitchen prepares wholesome regional specialties and contemporary meal packages.",
            division_type="business",
            order=4
        )

    def test_cloud_kitchen_jk_branding_and_brochure(self):
        """Test GET /businesses/cloud-kitchen/ renders JK Kitchen logo, Central Kitchen identity, PDF sections, services, and brochure download links."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'cloud-kitchen'}))
        response = business_detail(req, slug='cloud-kitchen')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Headings & Uppercase Titles
        self.assertIn("JK KITCHEN", content)
        self.assertIn("CENTRAL KITCHEN", content)
        self.assertIn("BAIRAVA GROUPS", content)
        self.assertIn("ABOUT CENTRAL KITCHEN", content)
        self.assertIn("PEOPLE-FIRST APPROACH", content)
        self.assertIn("ABSOLUTE COMPLIANCE", content)
        self.assertIn("SERVICE EXCELLENCE", content)
        self.assertIn("CULINARY INNOVATION &amp; DIETARY EXCELLENCE", content)
        self.assertIn("CHEF-LED INNOVATION", content)
        self.assertIn("DIETITIAN-BACKED MENUS", content)
        self.assertIn("MINDFUL SOURCING", content)
        self.assertIn("OUR SERVICES", content)
        self.assertIn("CORPORATE CATERING", content)
        self.assertIn("INDUSTRIAL CATERING", content)
        self.assertIn("INSTITUTIONAL CATERING", content)
        self.assertIn("RETAIL FOOD SERVICES", content)
        self.assertIn("SPECIAL EVENTS CATERING", content)
        self.assertIn("CORPORATE KITCHEN PLANNING &amp; DESIGN", content)
        self.assertIn("GUEST HOUSE MANAGEMENT", content)
        self.assertIn("FOOD MANAGEMENT CONSULTANCY", content)
        self.assertIn("CULINARY DEVELOPMENT", content)
        self.assertIn("INFRASTRUCTURE &amp; SAFEGUARDS", content)
        self.assertIn("GLOBAL SAFETY CERTIFICATIONS", content)
        self.assertIn("24/7 CONTINUITY", content)
        self.assertIn("CRISIS RESILIENCE", content)
        self.assertIn("WASTE MITIGATION", content)
        self.assertIn("SECTOR FOCUS", content)
        self.assertIn("BUSINESS &amp; INDUSTRY", content)
        self.assertIn("HEALTHCARE &amp; CLINICAL", content)
        self.assertIn("JK KITCHEN PROFILE", content)
        self.assertIn("VIEW BROCHURE", content)
        self.assertIn("DOWNLOAD BROCHURE", content)

        # Uploaded Assets
        self.assertIn("core/images/logos/bairava-kitchen-logo.png", content)
        self.assertIn("core/images/divisions/jk_kitchen_hero.jpg", content)
        self.assertIn("core/images/divisions/gallery_bulk_catering.jpg", content)
        self.assertIn("core/images/divisions/gallery_premium_catering.jpg", content)
        self.assertIn("core/images/divisions/gallery_cloud_kitchen.jpg", content)
        self.assertIn("core/docs/JK-Kitchen-Profile-July-2026.pdf", content)

        # Contact Information
        self.assertIn('href="tel:+919940038991"', content)
        self.assertIn("+91 99400 38991", content)
        self.assertIn('href="https://wa.me/919940038991"', content)
        self.assertIn("2A, TVS NAGAR, Kandigai Street, Korttur, Chennai - 600076", content)
        self.assertIn("SF No 152/15B, Aambal Poo Street, Pondur Village, Sriperumbudur, Tamil Nadu - 602105", content)


class AadukalamPoliticalNewsTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_aadukalam = BusinessDivision.objects.create(
            name="BAIRAVA ஆடுகளம்",
            slug="aadukalam",
            tagline="POLITICS, PEOPLE & THE STORIES THAT SHAPE TOMORROW.",
            short_description="BAIRAVA ஆடுகளம் is a political news platform focused on Tamil Nadu, India and global political developments, presenting important political stories, public issues and policy discussions in a clear and responsible format.",
            full_description="BAIRAVA ஆடுகளம் brings together political news, public policy debates, election insights and weekly digital newspaper editions delivering concise, balanced and responsible political journalism.",
            division_type="business",
            order=7
        )

    def test_aadukalam_political_news_and_weekly_newspaper(self):
        """Test GET /businesses/aadukalam/ renders Political News, Weekly Newspaper, 4-card grid, analysis, and single image."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'aadukalam'}))
        response = business_detail(req, slug='aadukalam')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # 1. SEO, Breadcrumb & Hero
        self.assertIn("BAIRAVA ஆடுகளம் | POLITICAL NEWS & WEEKLY NEWSPAPER", content)
        self.assertIn("POLITICAL NEWS", content)
        self.assertIn("BAIRAVA ஆடுகளம்", content)
        self.assertIn('"POLITICS, PEOPLE & THE STORIES THAT SHAPE TOMORROW."', content)
        self.assertIn("BAIRAVA ஆடுகளம் is a political news platform focused on Tamil Nadu, India and global political developments", content)
        self.assertIn("WEEKLY NEWSPAPER", content)
        self.assertIn("LATEST POLITICAL NEWS", content)

        # 2. Hero Single Image (Strictly 1 image on entire page)
        self.assertIn("core/images/news/hero_studio.jpg", content)
        self.assertNotIn("core/images/news/tamilnadu.jpg", content)
        self.assertNotIn("core/images/news/india.jpg", content)
        self.assertNotIn("core/images/news/world.jpg", content)

        # 3. Weekly Political Newspaper Section
        self.assertIn("WEEKLY POLITICAL NEWSPAPER", content)
        self.assertIn("THIS WEEK'S EDITION", content)
        self.assertIn("POLITICAL NEWS • ANALYSIS • PUBLIC ISSUES", content)
        self.assertIn("PUBLICATION:", content)
        self.assertIn("WEEKLY", content)
        self.assertIn("FORMAT:", content)
        self.assertIn("DIGITAL NEWSPAPER", content)
        self.assertIn("VIEW NEWSPAPER", content)
        self.assertIn("DOWNLOAD NEWSPAPER", content)

        # 4. Political News Section (4 text-based cards)
        self.assertIn("POLITICAL NEWS", content)
        self.assertIn("TAMIL NADU POLITICS", content)
        self.assertIn("Political developments, public issues, government decisions and important state-level discussions.", content)
        self.assertIn("INDIAN POLITICS", content)
        self.assertIn("Parliament, national policy, elections and major political developments across India.", content)
        self.assertIn("POLICY &amp; GOVERNANCE", content)
        self.assertIn("Important government policies, legislative developments and issues affecting citizens.", content)
        self.assertIn("WORLD POLITICS", content)
        self.assertIn("Major international political developments and their wider impact.", content)

        # 5. Political Analysis Section
        self.assertIn("POLITICAL ANALYSIS", content)
        self.assertIn("KEY ISSUES", content)
        self.assertIn("POLICY &amp; GOVERNANCE", content)
        self.assertIn("ELECTION WATCH", content)

        # 6. Our Weekly Edition Section
        self.assertIn("OUR WEEKLY EDITION", content)
        self.assertIn("WEEKLY EDITION", content)
        self.assertIn("EVERY WEEK", content)
        self.assertIn("READ THIS WEEK'S EDITION", content)

        # 7. Verify no old sports content on public page
        self.assertNotIn("HERITAGE &amp; COMMUNITY SPORTS", content)
        self.assertNotIn("HERITAGE & COMMUNITY SPORTS", content)
        self.assertNotIn("TRADITIONAL SPORTS", content)
        self.assertNotIn("KABADDI", content)
        self.assertNotIn("COMMUNITY GAMES", content)
        self.assertNotIn("SPORTS ACTIVITIES", content)


class BairavaSportsClubGalleryTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_sports, _ = BusinessDivision.objects.update_or_create(
            slug="sports-club",
            defaults={
                "name": "BAIRAVA SPORTS CLUB",
                "tagline": "Nurturing Athletic Talent & Active Communities.",
                "short_description": "Bairava Sports Club promotes sports, fitness, training and community participation.",
                "full_description": "Premier athletic training facilities, fitness academies, and sports tournaments.",
                "division_type": "business",
                "order": 5,
            }
        )

    def test_sports_club_real_photo_gallery(self):
        """Test GET /businesses/sports-club/ renders the static frame photo gallery with all 9 original photos, thumbnails, counter & lightbox."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'sports-club'}))
        response = business_detail(req, slug='sports-club')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # 1. Gallery Section & Headings
        self.assertIn("OUR SPORTS GALLERY", content)
        self.assertIn("Moments of Passion, Teamwork &amp; Triumph.", content)
        self.assertIn("MOMENTS &amp; TRIUMPHS", content)
        self.assertIn("AUTO ROTATING", content)
        self.assertIn('<span id="totalSlidesNum">09</span>', content)

        # 2. All 9 Real Uploaded Photographs
        self.assertIn("core/images/sports/sports-gallery-01.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-02.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-03.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-04.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-05.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-06.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-07.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-08.jpg", content)
        self.assertIn("core/images/sports/sports-gallery-09.jpg", content)

        # 3. Accessibility Alt Texts
        self.assertIn('alt="Bairava Sports Club fitness team"', content)
        self.assertIn('alt="Bairava Sports Club gym athletes"', content)
        self.assertIn('alt="Bairava Sports Club tournament team"', content)
        self.assertIn('alt="Bairava Sports Club sports event"', content)
        self.assertIn('alt="Bairava Sports Club trophy celebration"', content)
        self.assertIn('alt="Bairava Sports Club squad gathering"', content)
        self.assertIn('alt="Bairava Sports Club official team jersey lineup"', content)
        self.assertIn('alt="Bairava Sports Club team felicitation"', content)
        self.assertIn('alt="Bairava Sports Club annual awards presentation"', content)

        # 4. Captions
        self.assertIn("FITNESS &amp; STRENGTH CONDITIONING TEAM", content)
        self.assertIn("GYM ATHLETES &amp; BODYBUILDING SQUAD", content)
        self.assertIn("OFFICIAL TEAM JERSEY FELICITATION", content)
        self.assertIn("TEAM GATHERING &amp; CELEBRATION", content)
        self.assertIn("TOURNAMENT CHAMPIONSHIP &amp; TROPHY CELEBRATION", content)
        self.assertIn("SPORTS CLUB SQUAD &amp; COMMUNITY MEET", content)
        self.assertIn("OFFICIAL BAIRAVA TEAM JERSEY LINEUP", content)
        self.assertIn("HONORARY FELICITATION &amp; TEAM RECOGNITION", content)
        self.assertIn("ANNUAL SPORTS AWARDS &amp; MEMENTO PRESENTATION", content)

        # 5. Controls, Static Frame, Thumbnails & Lightbox
        self.assertIn("galleryPhotoFrame", content)
        self.assertIn("galleryPrevBtn", content)
        self.assertIn("galleryNextBtn", content)
        self.assertIn("galleryDots", content)
        self.assertIn("galleryThumbsList", content)
        self.assertIn("sportsLightbox", content)
        self.assertIn("lightboxCloseBtn", content)
        self.assertIn("lightboxPrevBtn", content)
        self.assertIn("lightboxNextBtn", content)


class BairavaLawAssociatesGalleryTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_law, _ = BusinessDivision.objects.update_or_create(
            slug="law-associates",
            defaults={
                "name": "BAIRAVA LAW ASSOCIATES",
                "tagline": "Your Trusted Legal Partner.",
                "short_description": "Delivering practical, professional and client-focused legal solutions for individuals, businesses and organizations with integrity, expertise and commitment.",
                "full_description": "Bairava Law Associates provides practical legal guidance and professional support for individuals, businesses and organizations.",
                "division_type": "business",
                "order": 11,
            }
        )

    def test_law_associates_photo_gallery(self):
        """Test GET /businesses/law-associates/ renders the static frame photo gallery with all original photos, thumbnails, counter & lightbox."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'law-associates'}))
        response = business_detail(req, slug='law-associates')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # 1. Gallery Section & Headings
        self.assertIn("OUR LAW ASSOCIATES GALLERY", content)
        self.assertIn("People, Practice, Community &amp; Professional Moments.", content)
        self.assertIn("PRACTICE &amp; PROFESSIONAL LIFE", content)
        self.assertIn("AUTO ROTATING", content)
        self.assertIn('<span id="lawTotalSlidesNum">05</span>', content)

        # 2. Uploaded Original Photographs
        self.assertIn("core/images/law_associates/law-associates-gallery-01.jpg", content)
        self.assertIn("core/images/law_associates/law-associates-gallery-02.jpg", content)
        self.assertIn("core/images/law_associates/law-associates-gallery-03.jpg", content)
        self.assertIn("core/images/law_associates/law-associates-gallery-04.jpg", content)
        self.assertIn("core/images/law_associates/law-associates-gallery-05.jpg", content)

        # 3. Accessibility Alt Texts
        self.assertIn('alt="Bairava Law Associates team gathering"', content)
        self.assertIn('alt="Bairava Law Associates legal team"', content)
        self.assertIn('alt="Bairava Law Associates commemorative event"', content)
        self.assertIn('alt="Bairava Law Associates advocates cohort"', content)
        self.assertIn('alt="Bairava Law Associates professional honors"', content)

        # 4. Captions
        self.assertIn("LEGAL TEAM &amp; ASSOCIATES GATHERING", content)
        self.assertIn("ADVOCATE LEADERSHIP &amp; LEGAL PRACTICE TEAM", content)
        self.assertIn("COMMEMORATIVE RECOGNITION &amp; FELICITATION", content)
        self.assertIn("BAR ADVOCATES COHORT &amp; LEGAL FRATERNITY", content)
        self.assertIn("LEGAL PROFESSIONAL HONORS &amp; CELEBRATION", content)

        # 5. Controls, Static Frame, Thumbnails & Lightbox
        self.assertIn("lawGalleryPhotoFrame", content)
        self.assertIn("lawGalleryPrevBtn", content)
        self.assertIn("lawGalleryNextBtn", content)
        self.assertIn("lawGalleryDots", content)
        self.assertIn("lawGalleryThumbsList", content)
        self.assertIn("lawLightbox", content)
        self.assertIn("lawLightboxCloseBtn", content)
        self.assertIn("lawLightboxPrevBtn", content)
        self.assertIn("lawLightboxNextBtn", content)


class BairavaAboutAchievementsGalleryTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()

    def test_about_achievements_and_moments_gallery(self):
        """Test GET /about/ renders the static frame achievements and moments gallery with all original photos, thumbnails, counter & lightbox."""
        from core.views import about_view
        req = self.rf.get(reverse('core:about'))
        response = about_view(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # 1. Gallery Section & Headings
        self.assertIn("ACHIEVEMENTS &amp; MOMENTS", content)
        self.assertIn("Celebrating milestones, recognition, community and meaningful moments.", content)
        self.assertIn("MILESTONES &amp; HONORS", content)
        self.assertIn("AUTO ROTATING", content)
        self.assertIn('<span id="aboutTotalSlidesNum">05</span>', content)

        # 2. Uploaded Original Photographs
        self.assertIn("core/images/about/about-achievement-01.jpg", content)
        self.assertIn("core/images/about/about-achievement-02.jpg", content)
        self.assertIn("core/images/about/about-achievement-03.jpg", content)
        self.assertIn("core/images/about/about-achievement-04.jpg", content)
        self.assertIn("core/images/about/about-achievement-05.jpg", content)

        # 3. Accessibility Alt Texts
        self.assertIn('alt="Bairava Groups leadership stage recognition and flower bouquet felicitation"', content)
        self.assertIn('alt="Bairava Groups honored at YEF Business Awards with traditional shawl"', content)
        self.assertIn('alt="Bairava Foundation traditional lamp lighting and prayer ceremony"', content)
        self.assertIn('alt="Bairava Groups team and delegates gathering at awards celebration"', content)
        self.assertIn('alt="YEF Business Awards presentation ceremony with eminent dignitaries"', content)

        # 4. Captions
        self.assertIn("LEADERSHIP FELICITATION &amp; HONORS", content)
        self.assertIn("YEF BUSINESS AWARDS HONORS", content)
        self.assertIn("FOUNDATION INAUGURAL BLESSINGS", content)
        self.assertIn("TEAM UNITY &amp; DELEGATES COHORT", content)
        self.assertIn("BUSINESS EXCELLENCE &amp; DIGNITARY HONORS", content)

        # 5. Controls, Static Frame, Thumbnails & Lightbox
        self.assertIn("aboutGalleryPhotoFrame", content)
        self.assertIn("aboutGalleryPrevBtn", content)
        self.assertIn("aboutGalleryNextBtn", content)
        self.assertIn("aboutGalleryDots", content)
        self.assertIn("aboutGalleryThumbsList", content)
        self.assertIn("aboutLightbox", content)
        self.assertIn("aboutLightboxCloseBtn", content)
        self.assertIn("aboutLightboxPrevBtn", content)
        self.assertIn("aboutLightboxNextBtn", content)













