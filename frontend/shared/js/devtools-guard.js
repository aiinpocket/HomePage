/**
 * DevTools 防護機制
 * 當開發者工具開啟時，阻止所有點擊操作並跳轉回首頁
 */

(function() {
    let devtoolsOpen = false;
    const threshold = 160; // DevTools 寬度閾值

    // 檢測 DevTools 是否開啟
    const detectDevTools = () => {
        const widthThreshold = window.outerWidth - window.innerWidth > threshold;
        const heightThreshold = window.outerHeight - window.innerHeight > threshold;
        const orientation = widthThreshold ? 'vertical' : 'horizontal';

        if (widthThreshold || heightThreshold) {
            if (!devtoolsOpen) {
                devtoolsOpen = true;
                console.log('DevTools detected');
            }
        } else {
            devtoolsOpen = false;
        }
    };

    // 使用多種方法檢測
    const checkDevTools = () => {
        const before = new Date();
        debugger;
        const after = new Date();
        if (after - before > 100) {
            devtoolsOpen = true;
        }
    };

    // 定期檢測窗口大小變化
    setInterval(detectDevTools, 500);

    // 檢測右鍵檢查元素
    document.addEventListener('contextmenu', () => {
        setTimeout(detectDevTools, 500);
    });

    // 攔截所有點擊事件
    document.addEventListener('click', function(e) {
        if (devtoolsOpen) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            // 顯示警告訊息（三語同時顯示）
            showDevToolsWarning();

            // 延遲跳轉，讓用戶看到訊息
            setTimeout(() => {
                // 跳轉回首頁
                if (window.location.pathname.includes('/corporate/') ||
                    window.location.pathname.includes('/generator/')) {
                    window.location.href = '/index.html';
                } else if (window.location.pathname !== '/index.html' &&
                           window.location.pathname !== '/') {
                    window.location.href = '/';
                }
            }, 2000);

            return false;
        }
    }, true); // 使用捕獲階段，優先級最高

    // 顯示警告訊息
    function showDevToolsWarning() {
        // 移除已存在的警告框
        const existing = document.getElementById('devtools-warning');
        if (existing) {
            existing.remove();
        }

        // 創建警告框
        const warning = document.createElement('div');
        warning.id = 'devtools-warning';
        warning.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            z-index: 999999;
            text-align: center;
            font-family: 'Segoe UI', Arial, sans-serif;
            animation: fadeInScale 0.3s ease-out;
            max-width: 90%;
            border: 2px solid rgba(255,255,255,0.3);
        `;

        warning.innerHTML = `
            <style>
                @keyframes fadeInScale {
                    from {
                        opacity: 0;
                        transform: translate(-50%, -50%) scale(0.8);
                    }
                    to {
                        opacity: 1;
                        transform: translate(-50%, -50%) scale(1);
                    }
                }
                @keyframes fadeOut {
                    to {
                        opacity: 0;
                        transform: translate(-50%, -50%) scale(0.8);
                    }
                }
            </style>
            <div style="font-size: 48px; margin-bottom: 20px;">🔒</div>
            <div style="font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #FFD700;">
                不可以偷看我的小秘密喔～
            </div>
            <div style="font-size: 16px; opacity: 0.9; margin-bottom: 10px;">
                You can't peek at my secrets!
            </div>
            <div style="font-size: 16px; opacity: 0.9; margin-bottom: 20px;">
                私の秘密を覗かないで！
            </div>
            <div style="font-size: 14px; opacity: 0.7;">
                正在返回首頁... / Returning to home... / ホームに戻ります...
            </div>
        `;

        document.body.appendChild(warning);

        // 1.5 秒後開始淡出動畫
        setTimeout(() => {
            warning.style.animation = 'fadeOut 0.5s ease-out forwards';
        }, 1500);
    }

    // 阻止常見的 DevTools 快捷鍵
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            setTimeout(detectDevTools, 100);
        }
        // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C
        if (e.ctrlKey && e.shiftKey && (e.keyCode === 73 || e.keyCode === 74 || e.keyCode === 67)) {
            setTimeout(detectDevTools, 100);
        }
        // Ctrl+U (查看源代碼)
        if (e.ctrlKey && e.keyCode === 85) {
            setTimeout(detectDevTools, 100);
        }
    });

    console.log('🔒 DevTools Guard Active');
})();
