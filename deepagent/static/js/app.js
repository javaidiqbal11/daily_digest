/**
 * DeepAgent Web UI — Application Logic
 * Handles chat interactions, agent switching, and UI state.
 */

// ─── State ──────────────────────────────────────────────────────────────────
const state = {
    sessionId: generateSessionId(),
    agentType: 'research',
    isLoading: false,
    messageCount: 0,
};

// ─── DOM Elements ───────────────────────────────────────────────────────────
const messagesContainer = document.getElementById('messages-container');
const messagesList = document.getElementById('messages-list');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const welcomeScreen = document.getElementById('welcome-screen');
const typingIndicator = document.getElementById('typing-indicator');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const headerTitle = document.getElementById('header-title');
const headerDesc = document.getElementById('header-desc');
const sidebar = document.getElementById('sidebar');
const menuToggle = document.getElementById('menu-toggle');

// Agent info mapping
const AGENT_INFO = {
    research: {
        title: '🔬 Research Agent',
        desc: 'Deep multi-step research with web search, planning, and sub-agents'
    },
    code: {
        title: '💻 Code Agent',
        desc: 'Programming assistant for writing, debugging, and reviewing code'
    },
    general: {
        title: '🌐 General Agent',
        desc: 'Versatile multi-purpose assistant for any task'
    }
};

// ─── Utilities ──────────────────────────────────────────────────────────────
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatMarkdown(text) {
    if (!text) return '';
    
    let html = escapeHtml(text);
    
    // Code blocks (```...```)
    html = html.replace(/```(\w*)\n?([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
    });
    
    // Inline code (`...`)
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold (**...**)
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Italic (*...*)
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    
    // Blockquotes
    html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
    
    // Unordered lists
    html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    
    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr>');
    
    // Line breaks to paragraphs
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');
    
    // Wrap in paragraph
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }
    
    return html;
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
}

// ─── UI Updates ─────────────────────────────────────────────────────────────
function setStatus(status, text) {
    statusDot.className = 'status-dot' + (status !== 'ready' ? ` ${status}` : '');
    statusText.textContent = text;
}

function setLoading(loading) {
    state.isLoading = loading;
    sendBtn.disabled = loading;
    messageInput.disabled = loading;
    typingIndicator.style.display = loading ? 'flex' : 'none';
    
    if (loading) {
        setStatus('busy', 'Processing...');
    } else {
        setStatus('ready', 'Ready');
    }
    
    if (loading) {
        scrollToBottom();
    }
}

function hideWelcomeScreen() {
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }
}

function addMessage(role, content) {
    hideWelcomeScreen();
    state.messageCount++;
    
    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.id = `msg-${state.messageCount}`;
    
    const avatarEmoji = role === 'user' ? '👤' : '🤖';
    const roleLabel = role === 'user' ? 'You' : 'DeepAgent';
    
    messageEl.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div class="message-content">
            <div class="message-role">${roleLabel}</div>
            <div class="message-body">${role === 'user' ? escapeHtml(content) : formatMarkdown(content)}</div>
        </div>
    `;
    
    messagesList.appendChild(messageEl);
    scrollToBottom();
}

// ─── API Communication ─────────────────────────────────────────────────────
async function sendMessage(content) {
    if (!content.trim() || state.isLoading) return;
    
    // Add user message
    addMessage('user', content);
    messageInput.value = '';
    autoResizeTextarea();
    
    // Set loading state
    setLoading(true);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: content,
                agent_type: state.agentType,
                session_id: state.sessionId,
            }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }
        
        const data = await response.json();
        
        // Update session ID if changed
        if (data.session_id) {
            state.sessionId = data.session_id;
        }
        
        // Add assistant response
        addMessage('assistant', data.response);
        
    } catch (error) {
        console.error('Chat error:', error);
        addMessage('assistant', `❌ **Error:** ${error.message}\n\nPlease check that the server is running and your API keys are configured.`);
        setStatus('error', 'Error');
    } finally {
        setLoading(false);
    }
}

// ─── Event Handlers ─────────────────────────────────────────────────────────

// Send button
sendBtn.addEventListener('click', () => {
    sendMessage(messageInput.value);
});

// Textarea: Enter to send, Shift+Enter for new line
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(messageInput.value);
    }
});

// Auto-resize textarea
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 150) + 'px';
}

messageInput.addEventListener('input', autoResizeTextarea);

// Agent selection
document.querySelectorAll('.agent-option').forEach(btn => {
    btn.addEventListener('click', () => {
        // Update active state
        document.querySelectorAll('.agent-option').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update state
        state.agentType = btn.dataset.agent;
        
        // Update header
        const info = AGENT_INFO[state.agentType];
        headerTitle.textContent = info.title;
        headerDesc.textContent = info.desc;
        
        // Close mobile sidebar
        sidebar.classList.remove('open');
        document.querySelector('.sidebar-overlay')?.classList.remove('active');
    });
});

// New conversation
document.getElementById('btn-new-chat').addEventListener('click', () => {
    state.sessionId = generateSessionId();
    state.messageCount = 0;
    messagesList.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    
    // Close mobile sidebar
    sidebar.classList.remove('open');
    document.querySelector('.sidebar-overlay')?.classList.remove('active');
});

// View reports
document.getElementById('btn-reports').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();
        addMessage('assistant', data.reports || 'No reports found.');
    } catch (error) {
        addMessage('assistant', '❌ Could not load reports.');
    }
    
    // Close mobile sidebar
    sidebar.classList.remove('open');
    document.querySelector('.sidebar-overlay')?.classList.remove('active');
});

// Mobile menu toggle
menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    
    // Create or toggle overlay
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }
    overlay.classList.toggle('active');
});

// ─── Suggestion Cards ───────────────────────────────────────────────────────
function useSuggestion(card) {
    const text = card.querySelector('.suggestion-text').textContent;
    messageInput.value = text;
    autoResizeTextarea();
    sendMessage(text);
}

// ─── Particles Background ───────────────────────────────────────────────────
function createParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 3 + 1}px;
            height: ${Math.random() * 3 + 1}px;
            background: rgba(99, 102, 241, ${Math.random() * 0.15 + 0.05});
            border-radius: 50%;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            animation: particleFloat ${Math.random() * 20 + 15}s linear infinite;
            animation-delay: ${Math.random() * 10}s;
        `;
        container.appendChild(particle);
    }
    
    // Add keyframe animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translate(${Math.random() * 200 - 100}px, -100vh) rotate(360deg); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// ─── Init ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    messageInput.focus();
    
    // Check API health
    fetch('/api/health')
        .then(r => r.json())
        .then(data => {
            if (data.status === 'healthy') {
                setStatus('ready', 'Connected');
            }
        })
        .catch(() => {
            setStatus('error', 'Disconnected');
        });
});
