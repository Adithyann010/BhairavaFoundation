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
        self.assertIn("Copyrights 2026 Bairava Groups All Rights Reserved. Chennai, Tamil Nadu.", content)

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


class BhairavaAssociationAndLegalTestCase(TestCase):
    def setUp(self):
        from django.test import RequestFactory
        self.rf = RequestFactory()
        self.div_assoc = BusinessDivision.objects.create(
            name="BHAIRAVA ASSOCIATION",
            slug="bhairava-association",
            tagline="COMMUNITY • CONNECTION • COLLABORATION",
            short_description="Building stronger communities through networking, collaboration, engagement and collective growth.",
            full_description="Bhairava Association is focused on bringing people, professionals, businesses and communities together through meaningful connections, collaboration and organized initiatives.",
            division_type="business",
            order=8
        )
        DivisionOffering.objects.create(
            division=self.div_assoc,
            title="COMMUNITY NETWORKING",
            badge="NETWORKING",
            description="Building meaningful connections among members, professionals and local communities.",
            order=1
        )

    def test_bhairava_association_page(self):
        """Test GET /businesses/bhairava-association/ returns 200 and renders association template."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'bhairava-association'}))
        response = business_detail(req, slug='bhairava-association')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn("BHAIRAVA ASSOCIATION", content)
        self.assertIn("COMMUNITY • CONNECTION • COLLABORATION", content)
        self.assertIn("COMMUNITY NETWORKING", content)
        self.assertIn("core/images/divisions/association.jpg", content)

    def test_navbar_businesses_count_and_association(self):
        """Test that navbar shows BUSINESSES (8 DIVISIONS) and includes BHAIRAVA ASSOCIATION."""
        from core.views import home
        req = self.rf.get(reverse('core:home'))
        response = home(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn("BUSINESSES (8 DIVISIONS)", content)
        self.assertIn("BHAIRAVA ASSOCIATION", content)
        self.assertIn("BAIRAVA FINANCE", content)
        self.assertIn("BAIRAVA MEDIA", content)

    def test_legal_page_content_and_image(self):
        """Test GET /legal/ returns 200 and renders updated Legal Associates content & image."""
        from law_associates.views import legal_index
        req = self.rf.get(reverse('law_associates:index'))
        response = legal_index(req)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        self.assertIn("LEGAL", content)
        self.assertIn("LEGAL ASSOCIATES", content)
        self.assertIn("CORPORATE &amp; BUSINESS LAW", content)
        self.assertIn("CONTRACTS &amp; AGREEMENTS", content)
        self.assertIn("PROPERTY &amp; REAL ESTATE LAW", content)
        self.assertIn("COMPLIANCE &amp; DOCUMENTATION", content)
        self.assertIn("LEGAL ADVISORY", content)
        self.assertIn("DISPUTE SUPPORT", content)
        self.assertIn("core/images/divisions/legal.jpg", content)


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
            name="BAIRAVA CLOUD KITCHEN",
            slug="cloud-kitchen",
            tagline="HYGIENIC, AUTHENTIC & FLAVORFUL CULINARY EXPERIENCES",
            short_description="Bairava Cloud Kitchen brings convenient food experiences to customers through professionally managed kitchen operations and carefully prepared menus.",
            full_description="Operating state-of-the-art commercial culinary hubs, Bairava Cloud Kitchen prepares wholesome regional specialties and contemporary meal packages.",
            division_type="business",
            order=4
        )

    def test_cloud_kitchen_jk_branding_and_brochure(self):
        """Test GET /businesses/cloud-kitchen/ renders JK Kitchen logo, poster, gallery, and brochure download links."""
        from core.views import business_detail
        req = self.rf.get(reverse('core:business_detail', kwargs={'slug': 'cloud-kitchen'}))
        response = business_detail(req, slug='cloud-kitchen')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')

        # Headings & Uppercase Titles
        self.assertIn("BAIRAVA CLOUD KITCHEN", content)
        self.assertIn("JK KITCHEN", content)
        self.assertIn("CULINARY EXCELLENCE • EVERY DAY", content)
        self.assertIn("FRESH &amp; HYGIENIC", content)
        self.assertIn("AUTHENTIC FLAVOURS", content)
        self.assertIn("CORPORATE &amp; INSTITUTIONAL", content)
        self.assertIn("SPECIAL DIET SOLUTIONS", content)
        self.assertIn("FOOD &amp; CATERING GALLERY", content)
        self.assertIn("BULK CATERING", content)
        self.assertIn("CLOUD KITCHEN", content)
        self.assertIn("EVENT &amp; PARTY CATERING", content)
        self.assertIn("PREMIUM CATERING", content)
        self.assertIn("JK KITCHEN PROFILE", content)
        self.assertIn("VIEW BROCHURE", content)
        self.assertIn("DOWNLOAD BROCHURE", content)

        # Uploaded Assets
        self.assertIn("core/images/divisions/bairava_cloud_kitchen_logo.jpg", content)
        self.assertIn("core/images/divisions/jk_kitchen_poster.jpg", content)
        self.assertIn("core/images/divisions/gallery_bulk_catering.jpg", content)
        self.assertIn("core/images/divisions/gallery_cloud_kitchen.jpg", content)
        self.assertIn("core/images/divisions/gallery_event_party.jpg", content)
        self.assertIn("core/images/divisions/gallery_premium_catering.jpg", content)
        self.assertIn("core/docs/JK-Kitchen-Profile-July-2026.pdf", content)

        # Brochure View & Download Attributes
        self.assertIn('target="_blank"', content)
        self.assertIn('rel="noopener noreferrer"', content)
        self.assertIn('download="JK-Kitchen-Profile-July-2026.pdf"', content)


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










