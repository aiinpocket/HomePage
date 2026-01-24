// ========================================
// 隱藏彩蛋系統
// ========================================

class EasterEggSystem {
    constructor() {
        this.keySequence = [];
        this.targetSequence = ['a', 'i', 'i', 'n', 'p', 'o', 'c', 'k', 'e', 't'];
        this.konamiCode = [
            'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
            'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
            'b', 'a'
        ];
        this.konamiSequence = [];
        this.logoClickCount = 0;
        this.logoClickTimer = null;
        this.hackerMode = false;
        this.nKeyCount = 0;
        this.nKeyTimer = null;
        this.visitedPages = new Set();

        this.init();
    }

    init() {
        this.setupLogoHover();
        this.setupKeyboardListener();
        this.setupModalClose();
        this.setupKonamiCode();
        this.setupPocketDoubleClick();
        this.setupHackerMode();
        this.setupExplorerBadge();
    }

    // Logo hover 顯示委託資訊
    setupLogoHover() {
        const logo = document.getElementById('logo-secret');
        const secretInfo = document.getElementById('secret-info');

        if (logo && secretInfo) {
            logo.addEventListener('mouseenter', () => {
                secretInfo.classList.add('show');
            });

            logo.addEventListener('mouseleave', () => {
                secretInfo.classList.remove('show');
            });

            // 點擊 logo - 點擊 10 次觸發彩蛋
            logo.addEventListener('click', () => {
                secretInfo.classList.toggle('show');

                // 增加點擊計數
                this.logoClickCount++;

                // 清除之前的計時器
                if (this.logoClickTimer) {
                    clearTimeout(this.logoClickTimer);
                }

                // 3 秒內沒有點擊則重置
                this.logoClickTimer = setTimeout(() => {
                    this.logoClickCount = 0;
                }, 3000);

                // 達到 10 次點擊
                if (this.logoClickCount === 10) {
                    this.triggerLogoClickEasterEgg();
                    this.logoClickCount = 0;
                }
            });
        }
    }

    // 觸發 Logo 點擊彩蛋
    async triggerLogoClickEasterEgg() {
        try {
            const response = await fetch(`${window.API_BASE_URL}/api/easter-egg/click_logo_10`, {
                method: 'POST'
            });
            const data = await response.json();

            this.showPromoCodeModal('你發現了 Logo 彩蛋！', '恭喜你的好奇心得到了獎勵！', data.promo_code, data.discount);
            localStorage.setItem('promo_code', data.promo_code);
            this.playSound();

        } catch (error) {
            console.error('Failed to get promo code:', error);
            // Fallback: 顯示無優惠碼的訊息
            this.showAchievementModal('你發現了 Logo 彩蛋！', '恭喜你的好奇心得到了獎勵！');
        }
    }

    // 顯示優惠碼彈窗
    showPromoCodeModal(title, subtitle, promoCode, discount) {
        const announcement = document.createElement('div');
        announcement.className = 'easter-egg-announcement';
        announcement.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(10, 14, 39, 0.95);
                border: 2px solid #87CEEB;
                border-radius: 20px;
                padding: 3rem;
                text-align: center;
                z-index: 10000;
                box-shadow: 0 0 50px rgba(135, 206, 235, 0.6);
                animation: bounceIn 0.5s ease-out;
                max-width: 90vw;
            ">
                <h2 style="color: #87CEEB; font-size: 2rem; margin-bottom: 1rem;">${title}</h2>
                <p style="color: #7FFF00; font-size: 1.2rem;">${subtitle}</p>
                <div style="
                    background: linear-gradient(135deg, rgba(135, 206, 235, 0.1), rgba(127, 255, 0, 0.1));
                    border: 1px solid #87CEEB;
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 2rem 0;
                ">
                    <p style="color: #7FFF00; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">獲得優惠碼！</p>
                    <p style="color: #87CEEB; font-size: 2rem; font-family: monospace; letter-spacing: 3px;">${promoCode}</p>
                    <p style="color: #A0D8EF; font-size: 1rem; margin-top: 0.5rem;">${discount}% OFF - AiInPocket 服務</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    padding: 0.8rem 2rem;
                    background: linear-gradient(135deg, #87CEEB, #7FFF00);
                    border: none;
                    border-radius: 25px;
                    color: #0a0e27;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 1rem;
                ">太棒了！</button>
            </div>
        `;
        this.addBounceAnimation();
        document.body.appendChild(announcement);
    }

    // 顯示成就彈窗（無優惠碼）
    showAchievementModal(title, message) {
        const announcement = document.createElement('div');
        announcement.className = 'easter-egg-announcement';
        announcement.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(10, 14, 39, 0.95);
                border: 2px solid #7FFF00;
                border-radius: 20px;
                padding: 3rem;
                text-align: center;
                z-index: 10000;
                box-shadow: 0 0 50px rgba(127, 255, 0, 0.6);
                animation: bounceIn 0.5s ease-out;
                max-width: 90vw;
            ">
                <h2 style="color: #7FFF00; font-size: 2rem; margin-bottom: 1rem;">${title}</h2>
                <p style="color: #87CEEB; font-size: 1.2rem;">${message}</p>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    margin-top: 2rem;
                    padding: 0.8rem 2rem;
                    background: linear-gradient(135deg, #87CEEB, #7FFF00);
                    border: none;
                    border-radius: 25px;
                    color: #0a0e27;
                    font-weight: bold;
                    cursor: pointer;
                    font-size: 1rem;
                ">讚！</button>
            </div>
        `;
        this.addBounceAnimation();
        document.body.appendChild(announcement);
        this.playSound();
    }

    // 添加彈跳動畫
    addBounceAnimation() {
        if (!document.getElementById('bounce-animation')) {
            const style = document.createElement('style');
            style.id = 'bounce-animation';
            style.textContent = `
                @keyframes bounceIn {
                    0% { transform: translate(-50%, -50%) scale(0.3); opacity: 0; }
                    50% { transform: translate(-50%, -50%) scale(1.05); }
                    70% { transform: translate(-50%, -50%) scale(0.9); }
                    100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // ========================================
    // 新彩蛋 1: Pocket 雙擊特效
    // ========================================
    setupPocketDoubleClick() {
        document.addEventListener('dblclick', (e) => {
            const target = e.target;
            const text = target.textContent || '';

            // 檢查是否雙擊了包含 "Pocket" 或 "口袋" 的文字
            if (text.toLowerCase().includes('pocket') || text.includes('口袋')) {
                this.triggerPocketMagic(e.clientX, e.clientY);
            }
        });
    }

    triggerPocketMagic(x, y) {
        // 創建星星飛出效果
        const particles = ['✨', '⭐', '🤖', '💡', '🚀'];

        for (let i = 0; i < 12; i++) {
            const particle = document.createElement('div');
            particle.textContent = particles[Math.floor(Math.random() * particles.length)];
            particle.style.cssText = `
                position: fixed;
                left: ${x}px;
                top: ${y}px;
                font-size: 24px;
                pointer-events: none;
                z-index: 10000;
                animation: pocketExplode 1s ease-out forwards;
                --angle: ${(i / 12) * 360}deg;
                --distance: ${50 + Math.random() * 50}px;
            `;
            document.body.appendChild(particle);

            setTimeout(() => particle.remove(), 1000);
        }

        // 添加爆炸動畫
        if (!document.getElementById('pocket-explode-animation')) {
            const style = document.createElement('style');
            style.id = 'pocket-explode-animation';
            style.textContent = `
                @keyframes pocketExplode {
                    0% {
                        transform: translate(0, 0) scale(0);
                        opacity: 1;
                    }
                    100% {
                        transform: translate(
                            calc(cos(var(--angle)) * var(--distance)),
                            calc(sin(var(--angle)) * var(--distance))
                        ) scale(1.5);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        // 顯示訊息
        this.showToast('你發現了口袋的秘密！ 🎉');
        this.playSound();
    }

    // 顯示 Toast 訊息
    showToast(message) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 100px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #87CEEB, #7FFF00);
            color: #0a0e27;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            z-index: 10000;
            animation: toastIn 0.3s ease-out, toastOut 0.3s ease-in 2s forwards;
        `;

        if (!document.getElementById('toast-animation')) {
            const style = document.createElement('style');
            style.id = 'toast-animation';
            style.textContent = `
                @keyframes toastIn {
                    from { opacity: 0; transform: translateX(-50%) translateY(20px); }
                    to { opacity: 1; transform: translateX(-50%) translateY(0); }
                }
                @keyframes toastOut {
                    from { opacity: 1; }
                    to { opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
    }

    // ========================================
    // 新彩蛋 2: 夜間駭客模式 (Shift + N x 3)
    // ========================================
    setupHackerMode() {
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            if (e.shiftKey && e.key.toLowerCase() === 'n') {
                this.nKeyCount++;

                if (this.nKeyTimer) clearTimeout(this.nKeyTimer);
                this.nKeyTimer = setTimeout(() => this.nKeyCount = 0, 1000);

                if (this.nKeyCount >= 3) {
                    this.toggleHackerMode();
                    this.nKeyCount = 0;
                }
            }
        });
    }

    toggleHackerMode() {
        this.hackerMode = !this.hackerMode;

        if (this.hackerMode) {
            document.body.classList.add('hacker-mode');
            this.showToast('駭客模式已啟動 🖥️');
            this.startPermanentMatrix();
        } else {
            document.body.classList.remove('hacker-mode');
            this.showToast('駭客模式已關閉');
            this.stopPermanentMatrix();
        }

        // 添加駭客模式樣式
        if (!document.getElementById('hacker-mode-style')) {
            const style = document.createElement('style');
            style.id = 'hacker-mode-style';
            style.textContent = `
                body.hacker-mode {
                    filter: hue-rotate(90deg) saturate(1.5);
                }
                body.hacker-mode .navbar {
                    background: rgba(0, 20, 0, 0.95) !important;
                    border-bottom: 1px solid #0f0;
                }
                body.hacker-mode * {
                    font-family: 'Courier New', monospace !important;
                }
                body.hacker-mode .hero-title,
                body.hacker-mode .section-title,
                body.hacker-mode h1, body.hacker-mode h2, body.hacker-mode h3 {
                    color: #0f0 !important;
                    text-shadow: 0 0 10px #0f0 !important;
                }
            `;
            document.head.appendChild(style);
        }

        this.playKonamiSound();
    }

    startPermanentMatrix() {
        if (this.matrixCanvas) return;

        this.matrixCanvas = document.createElement('canvas');
        this.matrixCanvas.id = 'permanent-matrix';
        this.matrixCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.3;
            pointer-events: none;
        `;
        this.matrixCanvas.width = window.innerWidth;
        this.matrixCanvas.height = window.innerHeight;
        document.body.appendChild(this.matrixCanvas);

        const ctx = this.matrixCanvas.getContext('2d');
        const chars = '01アイウエオカキクケコ';
        const fontSize = 14;
        const columns = this.matrixCanvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        this.matrixInterval = setInterval(() => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, this.matrixCanvas.width, this.matrixCanvas.height);

            ctx.fillStyle = '#0f0';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > this.matrixCanvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }, 50);
    }

    stopPermanentMatrix() {
        if (this.matrixInterval) {
            clearInterval(this.matrixInterval);
            this.matrixInterval = null;
        }
        if (this.matrixCanvas) {
            this.matrixCanvas.remove();
            this.matrixCanvas = null;
        }
    }

    // ========================================
    // 新彩蛋 3: 探索家徽章收集
    // ========================================
    setupExplorerBadge() {
        // 從 localStorage 讀取已訪問的頁面
        const visited = localStorage.getItem('visited_pages');
        if (visited) {
            this.visitedPages = new Set(JSON.parse(visited));
        }

        // 記錄當前頁面
        const currentPage = window.location.pathname.split('/').pop() || 'index.html';
        this.visitedPages.add(currentPage);
        localStorage.setItem('visited_pages', JSON.stringify([...this.visitedPages]));

        // 顯示徽章進度
        this.updateBadgeProgress();

        // 檢查是否完成全部收集
        const allPages = ['index.html', 'about.html', 'contact.html', 'portfolio.html', 'tech-stack.html', 'privacy.html'];
        const allVisited = allPages.every(page => this.visitedPages.has(page));

        if (allVisited && !localStorage.getItem('explorer_badge_claimed')) {
            this.triggerExplorerBadge();
        }
    }

    updateBadgeProgress() {
        const allPages = ['index.html', 'about.html', 'contact.html', 'portfolio.html', 'tech-stack.html', 'privacy.html'];
        const visitedCount = allPages.filter(page => this.visitedPages.has(page)).length;

        // 如果還沒收集完，顯示進度
        if (visitedCount < allPages.length && visitedCount > 0) {
            const indicator = document.createElement('div');
            indicator.id = 'explorer-progress';
            indicator.innerHTML = `
                <div style="
                    position: fixed;
                    bottom: 20px;
                    left: 20px;
                    background: rgba(10, 14, 39, 0.9);
                    border: 1px solid #87CEEB;
                    border-radius: 10px;
                    padding: 10px 15px;
                    z-index: 1000;
                    font-size: 12px;
                    color: #A0D8EF;
                ">
                    🏆 探索進度: ${visitedCount}/${allPages.length}
                </div>
            `;

            // 3 秒後移除
            document.body.appendChild(indicator);
            setTimeout(() => indicator.remove(), 3000);
        }
    }

    async triggerExplorerBadge() {
        localStorage.setItem('explorer_badge_claimed', 'true');

        try {
            const response = await fetch(`${window.API_BASE_URL}/api/easter-egg/explorer`, {
                method: 'POST'
            });
            const data = await response.json();

            this.showPromoCodeModal(
                '🏆 探索家成就解鎖！',
                '你已經瀏覽了網站的所有頁面！',
                data.promo_code,
                data.discount
            );
            localStorage.setItem('explorer_promo_code', data.promo_code);

        } catch (error) {
            console.error('Failed to get explorer badge:', error);
            this.showAchievementModal('🏆 探索家成就解鎖！', '你已經瀏覽了網站的所有頁面！恭喜！');
        }

        this.playKonamiSound();
    }

    // ========================================
    // 原有功能
    // ========================================

    // 鍵盤輸入 "aiinpocket" 彩蛋
    setupKeyboardListener() {
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            const key = e.key.toLowerCase();
            this.keySequence.push(key);

            if (this.keySequence.length > this.targetSequence.length) {
                this.keySequence.shift();
            }

            if (this.keySequence.join('') === this.targetSequence.join('')) {
                this.triggerPocketEasterEgg();
                this.keySequence = [];
            }
        });
    }

    triggerPocketEasterEgg() {
        const modal = document.getElementById('easter-egg-modal');
        if (modal) {
            modal.classList.add('show');
            modal.setAttribute('aria-hidden', 'false');
            this.createFloatingText();
            this.playSound();
        }
    }

    createFloatingText() {
        const messages = ['AI is in your pocket!', '魔法已啟動', '彩蛋發現者', '稀有成就解鎖'];

        messages.forEach((msg, index) => {
            setTimeout(() => {
                const floatText = document.createElement('div');
                floatText.textContent = msg;
                floatText.style.cssText = `
                    position: fixed;
                    left: 50%;
                    top: ${20 + index * 60}px;
                    transform: translateX(-50%);
                    font-size: 2rem;
                    font-weight: 700;
                    background: linear-gradient(135deg, #87CEEB, #7FFF00);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    z-index: 9999;
                    pointer-events: none;
                    animation: floatUp 3s ease-out forwards;
                `;

                document.body.appendChild(floatText);
                setTimeout(() => floatText.remove(), 3000);
            }, index * 200);
        });

        if (!document.getElementById('float-animation-style')) {
            const style = document.createElement('style');
            style.id = 'float-animation-style';
            style.textContent = `
                @keyframes floatUp {
                    0% { opacity: 0; transform: translateX(-50%) translateY(0); }
                    20% { opacity: 1; }
                    100% { opacity: 0; transform: translateX(-50%) translateY(-100px) scale(1.5); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    playSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = 800;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (e) {
            console.log('Audio not supported');
        }
    }

    setupModalClose() {
        const modal = document.getElementById('easter-egg-modal');
        const closeBtn = document.getElementById('modal-close');
        const overlay = document.getElementById('modal-overlay');

        if (modal && closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('show');
                modal.setAttribute('aria-hidden', 'true');
            });
        }

        if (modal && overlay) {
            overlay.addEventListener('click', () => {
                modal.classList.remove('show');
                modal.setAttribute('aria-hidden', 'true');
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
                modal.classList.remove('show');
                modal.setAttribute('aria-hidden', 'true');
            }
        });
    }

    setupKonamiCode() {
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            this.konamiSequence.push(e.key);

            if (this.konamiSequence.length > this.konamiCode.length) {
                this.konamiSequence.shift();
            }

            if (this.konamiSequence.join(',') === this.konamiCode.join(',')) {
                this.triggerKonamiEasterEgg();
                this.konamiSequence = [];
            }
        });
    }

    async triggerKonamiEasterEgg() {
        console.log('Konami Code Activated!');
        this.matrixEffect();

        try {
            const response = await fetch(`${window.API_BASE_URL}/api/easter-egg/konami`, {
                method: 'POST'
            });
            const data = await response.json();

            const announcement = document.createElement('div');
            announcement.innerHTML = `
                <div style="
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(10, 14, 39, 0.95);
                    border: 2px solid #7FFF00;
                    border-radius: 20px;
                    padding: 3rem;
                    text-align: center;
                    z-index: 10000;
                    box-shadow: 0 0 50px rgba(127, 255, 0, 0.6);
                    max-width: 90vw;
                ">
                    <h2 style="color: #7FFF00; font-size: 2rem; margin-bottom: 1rem;">開發者模式已啟動</h2>
                    <p style="color: #87CEEB; font-size: 1.2rem;">你發現了隱藏的開發者彩蛋！</p>
                    <div style="
                        background: linear-gradient(135deg, rgba(135, 206, 235, 0.1), rgba(127, 255, 0, 0.1));
                        border: 1px solid #7FFF00;
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin: 2rem 0;
                    ">
                        <p style="color: #7FFF00; font-size: 1.5rem; font-weight: bold;">獲得優惠碼！</p>
                        <p style="color: #87CEEB; font-size: 2rem; font-family: monospace; letter-spacing: 3px;">${data.promo_code}</p>
                        <p style="color: #A0D8EF; font-size: 1rem; margin-top: 0.5rem;">${data.discount}% OFF</p>
                    </div>
                    <p style="color: #A0D8EF; margin-top: 2rem; font-family: monospace;">
                        System Status: <span style="color: #7FFF00;">ONLINE</span><br>
                        Access Level: <span style="color: #7FFF00;">DEVELOPER</span>
                    </p>
                    <button onclick="this.parentElement.parentElement.remove()" style="
                        margin-top: 2rem;
                        padding: 0.8rem 2rem;
                        background: linear-gradient(135deg, #87CEEB, #7FFF00);
                        border: none;
                        border-radius: 25px;
                        color: #0a0e27;
                        font-weight: bold;
                        cursor: pointer;
                        font-size: 1rem;
                    ">關閉</button>
                </div>
            `;

            document.body.appendChild(announcement);
            localStorage.setItem('promo_code', data.promo_code);

        } catch (error) {
            console.error('Failed to get promo code:', error);
            this.showAchievementModal('開發者模式已啟動', '你發現了隱藏的開發者彩蛋！歡迎來到秘密世界。');
        }

        this.playKonamiSound();
    }

    matrixEffect() {
        const canvas = document.createElement('canvas');
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9998;
            pointer-events: none;
        `;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        const chars = '01アイウエオカキクケコサシスセソ';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        let frame = 0;
        const maxFrames = 200;

        function draw() {
            ctx.fillStyle = 'rgba(10, 14, 39, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = '#7FFF00';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }

            frame++;
            if (frame < maxFrames) {
                requestAnimationFrame(draw);
            } else {
                canvas.remove();
            }
        }

        draw();
    }

    playKonamiSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const notes = [523, 659, 784, 1047];

            notes.forEach((freq, index) => {
                setTimeout(() => {
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();

                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);

                    oscillator.frequency.value = freq;
                    oscillator.type = 'square';

                    gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.3);
                }, index * 150);
            });
        } catch (e) {
            console.log('Audio not supported');
        }
    }
}

// 初始化彩蛋系統
document.addEventListener('DOMContentLoaded', () => {
    new EasterEggSystem();

    // 控制台彩蛋訊息
    console.log('%cAiInPocket', 'font-size: 30px; font-weight: bold; background: linear-gradient(135deg, #87CEEB, #7FFF00); -webkit-background-clip: text; color: transparent;');
    console.log('%c嘿！你發現了控制台！', 'font-size: 16px; color: #7FFF00;');
    console.log('%c試試這些彩蛋：', 'font-size: 14px; color: #87CEEB;');
    console.log('%c  • 輸入 "aiinpocket"', 'font-size: 12px; color: #A0D8EF;');
    console.log('%c  • Konami Code (↑↑↓↓←→←→BA)', 'font-size: 12px; color: #A0D8EF;');
    console.log('%c  • 雙擊 "Pocket" 文字', 'font-size: 12px; color: #A0D8EF;');
    console.log('%c  • Shift + N × 3 (駭客模式)', 'font-size: 12px; color: #A0D8EF;');
    console.log('%c  • 瀏覽全部 6 個頁面', 'font-size: 12px; color: #A0D8EF;');
    console.log('%c我們正在尋找像你一樣好奇的人才 help@aiinpocket.com', 'font-size: 14px; color: #7FFF00;');
});
