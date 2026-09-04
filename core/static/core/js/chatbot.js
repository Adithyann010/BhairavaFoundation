/**
 * BAIRAVA GROUPS — AI CHATBOT JAVASCRIPT CONTROLLER
 * Handles interactive messaging, session history, RAG queries, markdown rendering,
 * and smart dynamic page context.
 */

(function() {
  'use strict';

  // Constants
  const STORAGE_KEY_CONV_ID = 'bairava_chat_conv_id';
  const STORAGE_KEY_HISTORY = 'bairava_chat_history';
  const STORAGE_KEY_IS_OPEN = 'bairava_chat_open';

  // DOM Elements
  let rootEl, toggleBtn, windowEl, clearBtn, minimizeBtn, closeBtn;
  let messagesEl, quickActionsEl, typingEl, formEl, inputEl, sendBtn;
  let contextBarEl, contextTextEl;

  // State
  let conversationId = '';
  let currentPage = '/';
  let apiUrl = '/api/chat/';
  let suggestionsUrl = '/api/chat/suggestions/';
  let isGenerating = false;

  // Default Quick Actions
  const DEFAULT_QUICK_ACTIONS = [
    { label: "Explore Businesses", query: "What businesses does Bairava Groups have?" },
    { label: "Construction & Land Promoters", query: "Tell me about Bairava Construction & Land Promoters" },
    { label: "Bairava Foundation", query: "Tell me about Bairava Foundation" },
    { label: "Bairava Trust", query: "What activities does Bairava Trust conduct?" },
    { label: "Contact Us", query: "How can I contact Bairava Groups?" }
  ];

  const INITIAL_WELCOME_TEXT = "Welcome to Bairava Groups. I’m the Bairava AI Assistant. I can help you explore our businesses, projects, services, events and community initiatives.";

  /**
   * Initialize Chatbot Widget
   */
  function init() {
    rootEl = document.getElementById('bairavaChatbotRoot');
    if (!rootEl) return;

    toggleBtn = document.getElementById('chatbotToggleBtn');
    windowEl = document.getElementById('chatbotWindow');
    clearBtn = document.getElementById('chatbotClearBtn');
    minimizeBtn = document.getElementById('chatbotMinimizeBtn');
    closeBtn = document.getElementById('chatbotCloseBtn');
    messagesEl = document.getElementById('chatbotMessages');
    quickActionsEl = document.getElementById('chatbotQuickActions');
    typingEl = document.getElementById('chatbotTyping');
    formEl = document.getElementById('chatbotForm');
    inputEl = document.getElementById('chatbotInput');
    sendBtn = document.getElementById('chatbotSendBtn');
    contextBarEl = document.getElementById('chatPageContextBar');
    contextTextEl = document.getElementById('chatPageContextText');

    currentPage = rootEl.getAttribute('data-current-page') || window.location.pathname;
    apiUrl = rootEl.getAttribute('data-api-url') || '/api/chat/';
    suggestionsUrl = rootEl.getAttribute('data-suggestions-url') || '/api/chat/suggestions/';

    // Generate or restore conversation ID
    conversationId = sessionStorage.getItem(STORAGE_KEY_CONV_ID);
    if (!conversationId) {
      conversationId = 'bairava_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
      sessionStorage.setItem(STORAGE_KEY_CONV_ID, conversationId);
    }

    // Set up page context banner
    setupPageContext();

    // Bind Event Listeners
    bindEvents();

    // Restore or initialize messages
    restoreChatHistory();

    // Check if was previously open in this session
    if (sessionStorage.getItem(STORAGE_KEY_IS_OPEN) === 'true') {
      openChat(false);
    }
  }

  /**
   * Bind DOM Events
   */
  function bindEvents() {
    toggleBtn.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', closeChat);
    minimizeBtn.addEventListener('click', minimizeChat);
    clearBtn.addEventListener('click', clearConversation);

    formEl.addEventListener('submit', handleFormSubmit);

    // Auto-expand and enter-to-send in textarea
    inputEl.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleFormSubmit(e);
      }
    });

    inputEl.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && rootEl.classList.contains('chat-open')) {
        closeChat();
      }
    });
  }

  /**
   * Identify page context and show sub-header
   */
  function setupPageContext() {
    const p = currentPage.toLowerCase();
    let name = '';

    if (p.includes('/construction')) name = 'Construction & Land Promoters';
    else if (p.includes('/foundation')) name = 'Bairava Foundation';
    else if (p.includes('/trust')) name = 'Bairava Trust';
    else if (p.includes('/event')) name = 'Bairava Event Management';
    else if (p.includes('/finance')) name = 'Bairava Finance';
    else if (p.includes('/cloud-kitchen')) name = 'Bairava Cloud Kitchen';
    else if (p.includes('/sports')) name = 'Bairava Sports Club';
    else if (p.includes('/aadukalam')) name = 'Bairava Aadukalam';
    else if (p.includes('/media')) name = 'Bairava Media';
    else if (p.includes('/contact')) name = 'Contact & Enquiries';

    if (name && contextBarEl && contextTextEl) {
      contextTextEl.textContent = 'Viewing ' + name;
      contextBarEl.style.display = 'flex';
    }
  }

  /**
   * Toggle Chat Window
   */
  function toggleChat() {
    if (rootEl.classList.contains('chat-open')) {
      closeChat();
    } else {
      openChat(true);
    }
  }

  /**
   * Open Chat Window
   */
  function openChat(focusInput) {
    rootEl.classList.remove('chat-minimized');
    rootEl.classList.add('chat-open');
    toggleBtn.setAttribute('aria-expanded', 'true');
    windowEl.setAttribute('aria-hidden', 'false');
    sessionStorage.setItem(STORAGE_KEY_IS_OPEN, 'true');

    scrollToBottom();
    if (focusInput !== false && inputEl) {
      setTimeout(function() {
        inputEl.focus();
      }, 250);
    }
  }

  /**
   * Close Chat Window
   */
  function closeChat() {
    rootEl.classList.remove('chat-open');
    rootEl.classList.remove('chat-minimized');
    toggleBtn.setAttribute('aria-expanded', 'false');
    windowEl.setAttribute('aria-hidden', 'true');
    sessionStorage.setItem(STORAGE_KEY_IS_OPEN, 'false');
  }

  /**
   * Minimize Chat Window
   */
  function minimizeChat() {
    rootEl.classList.remove('chat-open');
    rootEl.classList.add('chat-minimized');
    toggleBtn.setAttribute('aria-expanded', 'false');
    windowEl.setAttribute('aria-hidden', 'true');
    sessionStorage.setItem(STORAGE_KEY_IS_OPEN, 'false');
  }

  /**
   * Format Time (e.g. 10:45 AM)
   */
  function formatTimestamp(d) {
    const date = d ? new Date(d) : new Date();
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  /**
   * Simple Safe Markdown Formatter
   */
  function renderMarkdown(text) {
    if (!text) return '';

    // Escape basic HTML entities first
    let escaped = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Markdown Bold: **text**
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Markdown Links: [label](url)
    escaped = escaped.replace(/\[(.*?)\]\((.*?)\)/g, function(match, label, url) {
      return '<a href="' + url + '" target="_self" rel="noopener">' + label + '</a>';
    });

    // Split lines into paragraphs and lists
    const lines = escaped.split('\n');
    let html = '';
    let inList = false;
    let listType = 'ul';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (!line) {
        if (inList) {
          html += '</' + listType + '>';
          inList = false;
        }
        continue;
      }

      // Check bullet list item
      if (line.startsWith('- ') || line.startsWith('• ') || line.startsWith('* ')) {
        if (!inList || listType !== 'ul') {
          if (inList) html += '</' + listType + '>';
          html += '<ul>';
          inList = true;
          listType = 'ul';
        }
        html += '<li>' + line.substring(2).trim() + '</li>';
      }
      // Check numbered list item (e.g. 1. )
      else if (/^\d+\.\s/.test(line)) {
        if (!inList || listType !== 'ol') {
          if (inList) html += '</' + listType + '>';
          html += '<ol>';
          inList = true;
          listType = 'ol';
        }
        html += '<li>' + line.replace(/^\d+\.\s/, '').trim() + '</li>';
      } else {
        if (inList) {
          html += '</' + listType + '>';
          inList = false;
        }
        html += '<p>' + line + '</p>';
      }
    }

    if (inList) {
      html += '</' + listType + '>';
    }

    return html;
  }

  /**
   * Append Message to UI
   */
  function appendMessage(sender, text, timestamp, actionLinks) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg chat-msg-' + sender;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'msg-bubble';
    bubbleDiv.innerHTML = sender === 'ai' ? renderMarkdown(text) : '<p>' + escapeHtml(text) + '</p>';

    // Add action links if any
    if (sender === 'ai' && actionLinks && actionLinks.length > 0) {
      const actionsDiv = document.createElement('div');
      actionsDiv.className = 'msg-actions-container';

      actionLinks.forEach(function(link) {
        const a = document.createElement('a');
        a.className = 'msg-action-card-btn';
        a.href = link.url;
        a.innerHTML = link.title + ' <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
        actionsDiv.appendChild(a);
      });
      bubbleDiv.appendChild(actionsDiv);
    }

    const metaDiv = document.createElement('div');
    metaDiv.className = 'msg-meta';
    metaDiv.textContent = formatTimestamp(timestamp);

    msgDiv.appendChild(bubbleDiv);
    msgDiv.appendChild(metaDiv);

    messagesEl.appendChild(msgDiv);
    scrollToBottom();
  }

  /**
   * Escape pure text for user message
   */
  function escapeHtml(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /**
   * Render Quick Actions & Suggested Prompts
   */
  function renderQuickActions(customList) {
    quickActionsEl.innerHTML = '';
    const items = customList && customList.length > 0 ? customList : DEFAULT_QUICK_ACTIONS;

    items.forEach(function(item) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'quick-action-chip';
      
      const label = typeof item === 'string' ? item : item.label;
      const query = typeof item === 'string' ? item : item.query;

      btn.textContent = label;
      btn.addEventListener('click', function() {
        sendUserMessage(query);
      });
      quickActionsEl.appendChild(btn);
    });
  }

  /**
   * Scroll Messages thread to bottom
   */
  function scrollToBottom() {
    if (messagesEl) {
      setTimeout(function() {
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }, 50);
    }
  }

  /**
   * Restore Chat History from Session Storage
   */
  function restoreChatHistory() {
    messagesEl.innerHTML = '';
    const stored = sessionStorage.getItem(STORAGE_KEY_HISTORY);

    if (stored) {
      try {
        const history = JSON.parse(stored);
        if (Array.isArray(history) && history.length > 0) {
          history.forEach(function(msg) {
            appendMessage(msg.sender, msg.text, msg.timestamp, msg.actionLinks);
          });
          // Fetch dynamic page suggestions
          fetchPageSuggestions();
          return;
        }
      } catch (e) {
        console.warn("Could not parse chat history", e);
      }
    }

    // Default Initial State
    appendMessage('ai', INITIAL_WELCOME_TEXT, new Date(), null);
    renderQuickActions(DEFAULT_QUICK_ACTIONS);
    saveMessageToHistory('ai', INITIAL_WELCOME_TEXT, new Date(), null);
  }

  /**
   * Save a single message to session storage history
   */
  function saveMessageToHistory(sender, text, timestamp, actionLinks) {
    let history = [];
    const stored = sessionStorage.getItem(STORAGE_KEY_HISTORY);
    if (stored) {
      try {
        history = JSON.parse(stored);
      } catch (e) {
        history = [];
      }
    }
    history.push({
      sender: sender,
      text: text,
      timestamp: timestamp || new Date().toISOString(),
      actionLinks: actionLinks || []
    });
    sessionStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(history));
  }

  /**
   * Clear Chat Conversation
   */
  function clearConversation() {
    sessionStorage.removeItem(STORAGE_KEY_HISTORY);
    conversationId = 'bairava_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
    sessionStorage.setItem(STORAGE_KEY_CONV_ID, conversationId);

    messagesEl.innerHTML = '';
    appendMessage('ai', INITIAL_WELCOME_TEXT, new Date(), null);
    renderQuickActions(DEFAULT_QUICK_ACTIONS);
    saveMessageToHistory('ai', INITIAL_WELCOME_TEXT, new Date(), null);
  }

  /**
   * Fetch dynamic suggestions for the active page
   */
  function fetchPageSuggestions() {
    fetch(suggestionsUrl + '?current_page=' + encodeURIComponent(currentPage))
      .then(function(res) { return res.json(); })
      .then(function(data) {
        if (data && data.suggestions && data.suggestions.length > 0) {
          renderQuickActions(data.suggestions);
        } else {
          renderQuickActions(DEFAULT_QUICK_ACTIONS);
        }
      })
      .catch(function(err) {
        renderQuickActions(DEFAULT_QUICK_ACTIONS);
      });
  }

  /**
   * Extract CSRF Token from Cookie or Input
   */
  function getCsrfToken() {
    const input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (input) return input.value;

    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  /**
   * Handle Form Submit
   */
  function handleFormSubmit(e) {
    if (e) e.preventDefault();
    const query = inputEl.value.trim();
    if (!query || isGenerating) return;

    inputEl.value = '';
    inputEl.style.height = 'auto';
    sendUserMessage(query);
  }

  /**
   * Send User Message to Django AI Backend API
   */
  function sendUserMessage(text) {
    if (!text || isGenerating) return;

    isGenerating = true;
    sendBtn.disabled = true;

    // Append User Message to UI & History
    const now = new Date();
    appendMessage('user', text, now);
    saveMessageToHistory('user', text, now);

    // Show Typing Indicator
    if (typingEl) typingEl.style.display = 'flex';
    quickActionsEl.innerHTML = '';
    scrollToBottom();

    const csrfToken = getCsrfToken();

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({
        message: text,
        conversation_id: conversationId,
        current_page: currentPage,
        division_context: currentPage.replace('/businesses/', '').replace(/\//g, '')
      })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (typingEl) typingEl.style.display = 'none';
      isGenerating = false;
      sendBtn.disabled = false;

      const aiText = data.response || "I don't have that information in the Bairava Groups website data. Please contact the Bairava Groups team for accurate information.";
      const actionLinks = data.action_links || [];
      const aiTime = new Date();

      appendMessage('ai', aiText, aiTime, actionLinks);
      saveMessageToHistory('ai', aiText, aiTime, actionLinks);

      if (data.suggestions && data.suggestions.length > 0) {
        renderQuickActions(data.suggestions);
      } else {
        fetchPageSuggestions();
      }
    })
    .catch(function(error) {
      console.error("Chat API error:", error);
      if (typingEl) typingEl.style.display = 'none';
      isGenerating = false;
      sendBtn.disabled = false;

      const errorText = "Sorry, the AI assistant is temporarily unavailable. Please use the Contact Us page to reach the Bairava Groups team.";
      const fallbackLinks = [{ title: "Contact Us", url: "/contact/" }];
      const aiTime = new Date();

      appendMessage('ai', errorText, aiTime, fallbackLinks);
      saveMessageToHistory('ai', errorText, aiTime, fallbackLinks);
      renderQuickActions(DEFAULT_QUICK_ACTIONS);
    });
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
