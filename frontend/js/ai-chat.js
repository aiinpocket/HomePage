// ========================================
// AI 聊天機器人系統
// ========================================

class AIChatBot {
    constructor() {
        this.apiUrl = window.location.hostname === 'localhost'
            ? 'http://localhost:8000/api'
            : '/api';

        this.sessionId = this.generateSessionId();
        this.isOpen = false;
        this.messages = [];

        this.init();
    }

    init() {
        this.createChatUI();
        this.attachEventListeners();
        this.showWelcomeMessage();
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // 創建聊天 UI
    createChatUI() {
        const chatHTML = `
            <!-- AI 聊天機器人 -->
            <div id="ai-chat-container" class="ai-chat-container">
                <!-- 聊天按鈕 -->
                <button id="chat-toggle-btn" class="chat-toggle-btn">
                    <span class="chat-icon">🤖</span>
                    <span class="chat-dot"></span>
                </button>

                <!-- 聊天視窗 -->
                <div id="chat-window" class="chat-window">
                    <!-- 標題列 -->
                    <div class="chat-header">
                        <div class="chat-header-info">
                            <span class="chat-bot-avatar">🤖</span>
                            <div>
                                <h3>AI 小助手</h3>
                                <p class="chat-status">隨時為您服務</p>
                            </div>
                        </div>
                        <button id="chat-close-btn" class="chat-close-btn">✕</button>
                    </div>

                    <!-- 訊息區域 -->
                    <div id="chat-messages" class="chat-messages">
                        <!-- 訊息會動態插入這裡 -->
                    </div>

                    <!-- 快速選項 -->
                    <div id="quick-actions" class="quick-actions">
                        <button class="quick-btn" data-action="portfolio">📁 查看作品集</button>
                        <button class="quick-btn" data-action="contact">📧 聯絡我們</button>
                        <button class="quick-btn" data-action="tech">💻 技術棧</button>
                        <button class="quick-btn" data-action="about">👥 關於我們</button>
                    </div>

                    <!-- 輸入區域 -->
                    <div class="chat-input-container">
                        <input
                            type="text"
                            id="chat-input"
                            class="chat-input"
                            placeholder="輸入訊息或問題..."
                            autocomplete="off"
                        />
                        <button id="chat-send-btn" class="chat-send-btn">
                            <span>發送</span>
                        </button>
                    </div>

                    <!-- 載入指示器 -->
                    <div id="chat-loading" class="chat-loading" style="display: none;">
                        <div class="loading-dots">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 聊天機器人樣式 -->
            <style>
                .ai-chat-container {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 999;
                }

                .chat-toggle-btn {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #87CEEB, #7FFF00);
                    border: none;
                    cursor: pointer;
                    box-shadow: 0 5px 25px rgba(127, 255, 0, 0.4);
                    transition: all 0.3s ease;
                    position: relative;
                }

                .chat-toggle-btn:hover {
                    transform: scale(1.1);
                    box-shadow: 0 8px 30px rgba(127, 255, 0, 0.6);
                }

                .chat-icon {
                    font-size: 28px;
                }

                .chat-dot {
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    width: 12px;
                    height: 12px;
                    background: #7FFF00;
                    border-radius: 50%;
                    animation: pulse-dot 2s ease-in-out infinite;
                }

                @keyframes pulse-dot {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.3); opacity: 0.7; }
                }

                .chat-window {
                    position: absolute;
                    bottom: 80px;
                    right: 0;
                    width: 380px;
                    height: 600px;
                    background: rgba(15, 25, 50, 0.95);
                    border: 1px solid rgba(135, 206, 235, 0.3);
                    border-radius: 20px;
                    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
                    display: none;
                    flex-direction: column;
                    backdrop-filter: blur(10px);
                    animation: slideIn 0.3s ease;
                }

                .chat-window.show {
                    display: flex;
                }

                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(20px) scale(0.95);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                    }
                }

                .chat-header {
                    padding: 1.2rem;
                    background: linear-gradient(135deg, rgba(135, 206, 235, 0.2), rgba(127, 255, 0, 0.2));
                    border-bottom: 1px solid rgba(135, 206, 235, 0.3);
                    border-radius: 20px 20px 0 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .chat-header-info {
                    display: flex;
                    align-items: center;
                    gap: 0.8rem;
                }

                .chat-bot-avatar {
                    font-size: 2rem;
                }

                .chat-header h3 {
                    color: #87CEEB;
                    font-size: 1.1rem;
                    margin: 0;
                }

                .chat-status {
                    color: #7FFF00;
                    font-size: 0.75rem;
                    margin: 0;
                }

                .chat-close-btn {
                    background: none;
                    border: none;
                    color: #A0D8EF;
                    font-size: 1.5rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .chat-close-btn:hover {
                    color: #7FFF00;
                    transform: rotate(90deg);
                }

                .chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 1.5rem;
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }

                .chat-messages::-webkit-scrollbar {
                    width: 6px;
                }

                .chat-messages::-webkit-scrollbar-thumb {
                    background: rgba(135, 206, 235, 0.3);
                    border-radius: 3px;
                }

                .chat-message {
                    display: flex;
                    gap: 0.8rem;
                    animation: fadeInMessage 0.3s ease;
                }

                @keyframes fadeInMessage {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                .chat-message.user {
                    flex-direction: row-reverse;
                }

                .message-avatar {
                    font-size: 1.5rem;
                    flex-shrink: 0;
                }

                .message-content {
                    background: rgba(135, 206, 235, 0.1);
                    padding: 0.8rem 1.2rem;
                    border-radius: 15px;
                    max-width: 70%;
                    color: #E8F4F8;
                    line-height: 1.5;
                }

                .chat-message.user .message-content {
                    background: linear-gradient(135deg, rgba(135, 206, 235, 0.3), rgba(127, 255, 0, 0.3));
                    border: 1px solid rgba(127, 255, 0, 0.3);
                }

                .message-time {
                    font-size: 0.7rem;
                    color: #6B8FA3;
                    margin-top: 0.3rem;
                }

                .quick-actions {
                    padding: 1rem;
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem;
                    border-top: 1px solid rgba(135, 206, 235, 0.2);
                }

                .quick-btn {
                    padding: 0.5rem 1rem;
                    background: rgba(135, 206, 235, 0.1);
                    border: 1px solid rgba(135, 206, 235, 0.3);
                    border-radius: 20px;
                    color: #87CEEB;
                    font-size: 0.85rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .quick-btn:hover {
                    background: rgba(127, 255, 0, 0.2);
                    border-color: #7FFF00;
                    color: #7FFF00;
                    transform: translateY(-2px);
                }

                .chat-input-container {
                    padding: 1rem;
                    border-top: 1px solid rgba(135, 206, 235, 0.2);
                    display: flex;
                    gap: 0.8rem;
                }

                .chat-input {
                    flex: 1;
                    background: rgba(135, 206, 235, 0.05);
                    border: 1px solid rgba(135, 206, 235, 0.3);
                    border-radius: 25px;
                    padding: 0.8rem 1.2rem;
                    color: #E8F4F8;
                    font-size: 0.95rem;
                    outline: none;
                    transition: all 0.3s ease;
                }

                .chat-input:focus {
                    border-color: #7FFF00;
                    box-shadow: 0 0 15px rgba(127, 255, 0, 0.3);
                }

                .chat-send-btn {
                    background: linear-gradient(135deg, #87CEEB, #7FFF00);
                    border: none;
                    border-radius: 25px;
                    padding: 0.8rem 1.5rem;
                    color: #0a0e27;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }

                .chat-send-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(127, 255, 0, 0.4);
                }

                .chat-loading {
                    padding: 1rem;
                    text-align: center;
                }

                .loading-dots {
                    display: inline-flex;
                    gap: 0.5rem;
                }

                .loading-dots span {
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: #87CEEB;
                    animation: loading 1.4s ease-in-out infinite;
                }

                .loading-dots span:nth-child(2) {
                    animation-delay: 0.2s;
                }

                .loading-dots span:nth-child(3) {
                    animation-delay: 0.4s;
                }

                @keyframes loading {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.5); opacity: 0.5; }
                }

                @media (max-width: 768px) {
                    .chat-window {
                        width: calc(100vw - 40px);
                        height: calc(100vh - 120px);
                        right: -10px;
                    }
                }
            </style>
        `;

        document.body.insertAdjacentHTML('beforeend', chatHTML);
    }

    // 附加事件監聽器
    attachEventListeners() {
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const closeBtn = document.getElementById('chat-close-btn');
        const sendBtn = document.getElementById('chat-send-btn');
        const input = document.getElementById('chat-input');
        const quickBtns = document.querySelectorAll('.quick-btn');

        toggleBtn.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        quickBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.getAttribute('data-action');
                this.handleQuickAction(action);
            });
        });
    }

    // 切換聊天視窗
    toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        const isShow = chatWindow.classList.toggle('show');
        this.isOpen = isShow;

        if (isShow && this.messages.length === 0) {
            this.showWelcomeMessage();
        }
    }

    closeChat() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.remove('show');
        this.isOpen = false;
    }

    // 顯示歡迎訊息
    showWelcomeMessage() {
        setTimeout(() => {
            this.addMessage('bot', '你好！我是 AiInPocket 的 AI 小助手 🤖');
            setTimeout(() => {
                this.addMessage('bot', '我可以幫你瀏覽網站、回答問題，或是引導你到想去的頁面。試試問我一些問題吧！');
            }, 800);
        }, 300);
    }

    // 添加訊息
    addMessage(role, content, time = null) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageTime = time || new Date().toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' });

        const avatar = role === 'user' ? '👤' : '🤖';
        const messageClass = role === 'user' ? 'user' : 'bot';

        const messageHTML = `
            <div class="chat-message ${messageClass}">
                <div class="message-avatar">${avatar}</div>
                <div>
                    <div class="message-content">${content}</div>
                    <div class="message-time">${messageTime}</div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        this.messages.push({ role, content, time: messageTime });
    }

    // 發送訊息
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // 顯示使用者訊息
        this.addMessage('user', message);
        input.value = '';

        // 顯示載入動畫
        this.showLoading(true);

        try {
            // 呼叫後端 API
            const response = await this.callAPI(message);

            // 隱藏載入動畫
            this.showLoading(false);

            // 顯示 AI 回應
            this.addMessage('bot', response.reply);

            // 執行動作（如果有）
            if (response.action) {
                this.executeAction(response.action);
            }

        } catch (error) {
            this.showLoading(false);
            console.error('Error:', error);
            this.addMessage('bot', '抱歉，我遇到了一些問題。請稍後再試或直接透過聯絡表單與我們聯繫。');
        }
    }

    // 呼叫 AI API
    async callAPI(message) {
        // 在本地開發時，使用模擬回應
        if (window.location.hostname === 'localhost' && !window.location.port.includes('8000')) {
            return this.getMockResponse(message);
        }

        const response = await fetch(`${this.apiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: this.sessionId
            })
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        return await response.json();
    }

    // 模擬回應（用於測試）
    getMockResponse(message) {
        return new Promise((resolve) => {
            setTimeout(() => {
                const msg = message.toLowerCase();

                if (msg.includes('作品') || msg.includes('專案') || msg.includes('portfolio')) {
                    resolve({
                        reply: '好的！讓我帶你去看我們的作品集 📁',
                        action: { type: 'navigate', target: '/portfolio.html' }
                    });
                } else if (msg.includes('聯絡') || msg.includes('contact') || msg.includes('email')) {
                    resolve({
                        reply: '沒問題！我會幫你跳轉到聯絡頁面 📧',
                        action: { type: 'navigate', target: '/contact.html' }
                    });
                } else if (msg.includes('技術') || msg.includes('tech')) {
                    resolve({
                        reply: '讓我為你展示我們的技術棧 💻',
                        action: { type: 'navigate', target: '/tech-stack.html' }
                    });
                } else if (msg.includes('關於') || msg.includes('about') || msg.includes('團隊')) {
                    resolve({
                        reply: '帶你了解 AiInPocket 團隊！👥',
                        action: { type: 'navigate', target: '/about.html' }
                    });
                } else if (msg.includes('首頁') || msg.includes('home')) {
                    resolve({
                        reply: '回到首頁！🏠',
                        action: { type: 'navigate', target: '/index.html' }
                    });
                } else {
                    resolve({
                        reply: `我收到你的訊息了："${message}"。目前我還在學習中，可以試試問我「帶我去看作品集」或「我想聯絡你們」等問題！`,
                        action: null
                    });
                }
            }, 1000);
        });
    }

    // 執行動作
    executeAction(action) {
        switch (action.type) {
            case 'navigate':
                setTimeout(() => {
                    window.location.href = action.target;
                }, 1000);
                break;

            case 'scroll':
                const element = document.getElementById(action.target);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                }
                break;

            case 'highlight':
                action.targets.forEach(targetId => {
                    const el = document.getElementById(targetId);
                    if (el) {
                        el.style.animation = 'highlight 2s ease';
                        setTimeout(() => {
                            el.style.animation = '';
                        }, 2000);
                    }
                });
                break;

            default:
                console.log('Unknown action type:', action.type);
        }
    }

    // 快速動作
    handleQuickAction(action) {
        const actions = {
            portfolio: '帶我去看作品集',
            contact: '我想聯絡你們',
            tech: '介紹一下技術棧',
            about: '告訴我關於你們的資訊'
        };

        const message = actions[action];
        if (message) {
            document.getElementById('chat-input').value = message;
            this.sendMessage();
        }
    }

    // 顯示/隱藏載入動畫
    showLoading(show) {
        const loading = document.getElementById('chat-loading');
        loading.style.display = show ? 'block' : 'none';
    }
}

// 初始化 AI 聊天機器人
document.addEventListener('DOMContentLoaded', () => {
    new AIChatBot();
});
