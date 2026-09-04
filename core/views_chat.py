"""
Django API Views for the AI Chatbot.
Handles POST /api/chat/ and GET /api/chat/suggestions/.
"""

import json
import time
import logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings

from services.ai_chat import process_chat_message
from services.rag_retriever import get_suggested_questions

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 1000
RATE_LIMIT_WINDOW_SECONDS = 60
DEFAULT_RATE_LIMIT = getattr(settings, 'AI_CHAT_RATE_LIMIT', 30)


def _check_rate_limit(request) -> bool:
    """
    Simple session-based rate limiter.
    Allows up to DEFAULT_RATE_LIMIT requests within 60 seconds.
    """
    now = time.time()
    chat_requests = request.session.get('ai_chat_request_timestamps', [])

    # Filter out timestamps older than the rate limit window
    chat_requests = [ts for ts in chat_requests if now - ts < RATE_LIMIT_WINDOW_SECONDS]

    if len(chat_requests) >= DEFAULT_RATE_LIMIT:
        return False

    chat_requests.append(now)
    request.session['ai_chat_request_timestamps'] = chat_requests
    return True


@require_http_methods(["POST"])
def chat_api(request):
    """
    POST /api/chat/
    Payload:
    {
        "message": "...",
        "conversation_id": "...",
        "current_page": "/businesses/construction/",
        "division_context": "construction"
    }
    """
    # 1. Rate Limiting Check
    if not _check_rate_limit(request):
        return JsonResponse({
            "error": "Too many requests. Please wait a moment before sending another message.",
            "response": "You are sending messages too quickly. Please pause for a moment before asking another question."
        }, status=429)

    # 2. Parse Request JSON
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({
            "error": "Invalid JSON request payload.",
            "response": "Invalid request format."
        }, status=400)

    message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id', '').strip()
    current_page = data.get('current_page', '').strip()
    division_context = data.get('division_context', '').strip()

    # 3. Input Validation
    if not message:
        return JsonResponse({
            "error": "Message is required.",
            "response": "Please enter a message to get started."
        }, status=400)

    if len(message) > MAX_MESSAGE_LENGTH:
        return JsonResponse({
            "error": f"Message exceeds maximum allowed length of {MAX_MESSAGE_LENGTH} characters.",
            "response": f"Your message is too long (maximum {MAX_MESSAGE_LENGTH} characters). Please ask a shorter question."
        }, status=400)

    # 4. Process Chat Message
    try:
        result = process_chat_message(
            message=message,
            conversation_id=conversation_id,
            current_page=current_page,
            division_context=division_context
        )
        return JsonResponse(result, status=200)
    except Exception as exc:
        logger.exception(f"Unexpected error in chat API: {exc}")
        return JsonResponse({
            "response": "Sorry, the AI assistant is temporarily unavailable. Please use the Contact Us page to reach the Bairava Groups team.",
            "conversation_id": conversation_id,
            "suggestions": get_suggested_questions(current_page),
            "action_links": [{"title": "Contact Us", "url": "/contact/"}]
        }, status=200)


@require_http_methods(["GET"])
@ensure_csrf_cookie
def chat_suggestions_api(request):
    """
    GET /api/chat/suggestions/?current_page=/businesses/construction/
    """
    current_page = request.GET.get('current_page', '')
    suggestions = get_suggested_questions(current_page)
    return JsonResponse({
        "suggestions": suggestions,
        "current_page": current_page
    })
