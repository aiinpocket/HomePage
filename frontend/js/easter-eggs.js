// ========================================
// 隱藏彩蛋系統
// ========================================

class EasterEggSystem {
    constructor() {
        this.keySequence = [];
        this.targetSequence = ['p', 'o', 'c', 'k', 'e', 't'];
        this.konamiCode = [
            'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
            'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
            'b', 'a'
        ];
        this.konamiSequence = [];

        this.init();
    }

    init() {
        this.setupLogoHover();
        this.setupKeyboardListener();
        this.setupModalClose();
        this.setupKonamiCode();
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

            // 點擊 logo 也可以觸發
            logo.addEventListener('click', () => {
                secretInfo.classList.toggle('show');
            });
        }
    }

    // 鍵盤輸入 "pocket" 彩蛋
    setupKeyboardListener() {
        document.addEventListener('keydown', (e) => {
            // 如果正在輸入框中，不觸發
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }

            const key = e.key.toLowerCase();
            this.keySequence.push(key);

            // 只保留最後 6 個字符
            if (this.keySequence.length > this.targetSequence.length) {
                this.keySequence.shift();
            }

            // 檢查是否匹配
            if (this.keySequence.join('') === this.targetSequence.join('')) {
                this.triggerPocketEasterEgg();
                this.keySequence = [];
            }
        });
    }

    // 觸發 "pocket" 彩蛋
    triggerPocketEasterEgg() {
        const modal = document.getElementById('easter-egg-modal');
        if (modal) {
            modal.classList.add('show');
            this.createFloatingText();
            this.playSound();
        }
    }

    // 創建浮動文字效果
    createFloatingText() {
        const messages = [
            'AI is in your pocket!',
            '魔法已啟動',
            '彩蛋發現者',
            '稀有成就解鎖'
        ];

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

                setTimeout(() => {
                    floatText.remove();
                }, 3000);
            }, index * 200);
        });

        // 添加浮動動畫
        if (!document.getElementById('float-animation-style')) {
            const style = document.createElement('style');
            style.id = 'float-animation-style';
            style.textContent = `
                @keyframes floatUp {
                    0% {
                        opacity: 0;
                        transform: translateX(-50%) translateY(0);
                    }
                    20% {
                        opacity: 1;
                    }
                    100% {
                        opacity: 0;
                        transform: translateX(-50%) translateY(-100px) scale(1.5);
                    }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // 模擬音效（可選）
    playSound() {
        // 使用 Web Audio API 創建簡單的提示音
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

    // 關閉彈窗
    setupModalClose() {
        const modal = document.getElementById('easter-egg-modal');
        const closeBtn = document.getElementById('modal-close');
        const overlay = document.getElementById('modal-overlay');

        if (modal && closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('show');
            });
        }

        if (modal && overlay) {
            overlay.addEventListener('click', () => {
                modal.classList.remove('show');
            });
        }

        // ESC 鍵關閉
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal) {
                modal.classList.remove('show');
            }
        });
    }

    // Konami Code 彩蛋
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

    // 觸發 Konami Code 彩蛋
    triggerKonamiEasterEgg() {
        console.log('Konami Code Activated!');

        // 開啟矩陣效果
        this.matrixEffect();

        // 顯示特殊訊息
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
            ">
                <h2 style="color: #7FFF00; font-size: 2.5rem; margin-bottom: 1rem;">
                    開發者模式已啟動
                </h2>
                <p style="color: #87CEEB; font-size: 1.2rem;">
                    你發現了隱藏的開發者彩蛋！<br>
                    歡迎來到 AiInPocket 的秘密世界
                </p>
                <p style="color: #A0D8EF; margin-top: 2rem; font-family: monospace;">
                    System Status: <span style="color: #7FFF00;">ONLINE</span><br>
                    Access Level: <span style="color: #7FFF00;">DEVELOPER</span><br>
                    Matrix Mode: <span style="color: #7FFF00;">ACTIVATED</span>
                </p>
            </div>
        `;

        document.body.appendChild(announcement);

        setTimeout(() => {
            announcement.remove();
        }, 5000);

        // 播放音效序列
        this.playKonamiSound();
    }

    // 矩陣雨效果
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

    // Konami Code 音效
    playKonamiSound() {
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const notes = [523, 659, 784, 1047]; // C, E, G, C (高八度)

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
    console.log('%c試試輸入 "pocket" 或是 Konami Code (↑↑↓↓←→←→BA)', 'font-size: 12px; color: #87CEEB;');
    console.log('%c我們正在尋找像你一樣好奇的人才', 'font-size: 14px; color: #A0D8EF;');
});
