# Bairava Groups Website

A modern, responsive, and feature-rich corporate portal and web application for **Bairava Groups**, showcasing the group's diverse business enterprises, philanthropic trusts, future initiatives, and an intelligent AI chatbot assistant.

---

## Overview

The **Bairava Groups Website** serves as the central digital platform representing all commercial enterprises, sports clubs, community trusts, and upcoming business ventures under the Bairava umbrella. Built with a robust Django backend and high-performance frontend styling, the platform delivers an intuitive user experience across desktop and mobile devices.

---

## Business Divisions

The website features dedicated sections and enquiry interfaces for each operational division:

1. **Bairava Finance** — Comprehensive financial advisory, business funding, and financial solutions.
2. **Bairava Construction & Land Promoters** — Turnkey residential & commercial construction, land development, and architectural projects.
3. **Bairava Cloud Kitchen** — Premium culinary operations, bulk catering, and modern food delivery.
4. **Bairava Sports Club** — Premier athletic training facilities, fitness academies, and sports tournaments.
5. **Bairava Event Management** — End-to-end corporate event planning, weddings, cultural celebrations, and exhibitions.
6. **Bairava Aadukalam** — State-of-the-art sports arenas, turf bookings, and competitive sports leagues.
7. **Bairava Media** — Digital media production, brand promotion, video production, and advertising services.

---

## Foundation & Trust

- **Bairava Foundation** — Community development initiatives, social empowerment programs, and outreach campaigns.
- **Bairava Trust** — Educational scholarships, healthcare assistance, and charitable services supporting underprivileged communities.

---

## Future Plan

Exciting upcoming ventures currently under development:

- **Bairava Water Solutions** — *(Coming Soon)* — Advanced water purification, industrial treatment, and sustainable distribution networks.
- **Bairava Jewellery** — *(Coming Soon)* — Exquisite handcrafted gold, diamond, and traditional jewellery collections.

---

## Technology

The application is built using modern, production-ready web technologies:

- **Backend**: Python 3.12+, Django 5.2
- **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Design System with Glassmorphism & Animations), JavaScript (ES6+)
- **Static Assets**: WhiteNoise (Compressed & cached static file delivery)
- **Database**: SQLite (Local development / dynamic storage)
- **AI Integration**: OpenAI / Compatible REST API with session-based rate limiting and RAG context retrieval
- **Deployment & Hosting**: Vercel Serverless WSGI

---

## AI Chatbot

The website includes an intelligent, division-aware **Bairava Groups Virtual Assistant**:
- Real-time conversational AI powered by secure backend endpoints (`/api/chat/`).
- Contextual understanding of all Bairava Group divisions, services, and future plans.
- Dynamic quick-prompt suggestions based on current user navigation.
- Built-in session security, CSRF protection, and rate limiting.

---

## Local Setup

Follow these steps to run the application locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Adithyann010/BhairavaFoundation.git
cd BhairavaFoundation
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template file `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your configuration values (e.g., `DJANGO_SECRET_KEY`, `AI_API_KEY`).

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

*(Optional) Populate initial business and division data:*
```bash
python populate_db.py
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your web browser.

---

## Deployment

The project is configured for serverless deployment on **Vercel**:
- `vercel.json` defines WSGI routing and Python serverless function handlers.
- `build_files.sh` handles automated dependency installation and static asset compilation during Vercel builds.

---

## License & Copyright

© Bairava Groups. All rights reserved.
