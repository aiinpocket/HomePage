// ========================================
// 主要互動邏輯
// ========================================

class MainController {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupScrollEffects();
        this.setupStatsCounter();
        this.setupPortfolioFilter();
        this.setupContactForm();
        this.setupSmoothScroll();
    }

    // 導航列功能
    setupNavigation() {
        const navToggle = document.getElementById('nav-toggle');
        const navMenu = document.querySelector('.nav-menu');

        if (navToggle && navMenu) {
            navToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                navToggle.classList.toggle('active');
            });

            // 點擊導航連結後關閉選單
            document.querySelectorAll('.nav-menu a').forEach(link => {
                link.addEventListener('click', () => {
                    navMenu.classList.remove('active');
                    navToggle.classList.remove('active');
                });
            });
        }

        // 滾動時改變導航列樣式
        let lastScroll = 0;
        const navbar = document.querySelector('.navbar');

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                navbar.style.background = 'rgba(10, 14, 39, 0.98)';
                navbar.style.boxShadow = '0 5px 20px rgba(0, 0, 0, 0.5)';
            } else {
                navbar.style.background = 'rgba(10, 14, 39, 0.9)';
                navbar.style.boxShadow = 'none';
            }

            lastScroll = currentScroll;
        });
    }

    // 滾動效果
    setupScrollEffects() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // 為所有卡片添加淡入效果
        document.querySelectorAll('.service-card, .portfolio-card, .tech-item, .team-member, .value-item, .faq-item').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(el);
        });
    }

    // 數據計數器動畫
    setupStatsCounter() {
        const stats = document.querySelectorAll('.stat-number');

        const animateCount = (element) => {
            const target = parseInt(element.getAttribute('data-target'));
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCount = () => {
                current += step;
                if (current < target) {
                    element.textContent = Math.floor(current);
                    requestAnimationFrame(updateCount);
                } else {
                    element.textContent = target;
                }
            };

            updateCount();
        };

        const observerOptions = {
            threshold: 0.5
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && entry.target.textContent === '0') {
                    animateCount(entry.target);
                }
            });
        }, observerOptions);

        stats.forEach(stat => observer.observe(stat));
    }

    // 作品集篩選
    setupPortfolioFilter() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        const portfolioItems = document.querySelectorAll('.portfolio-item');

        if (filterButtons.length === 0) return;

        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                const filter = button.getAttribute('data-filter');

                // 更新按鈕狀態
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // 篩選項目
                portfolioItems.forEach(item => {
                    const category = item.getAttribute('data-category');

                    if (filter === 'all' || category === filter) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 10);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // 聯絡表單處理
    setupContactForm() {
        const form = document.getElementById('contact-form');
        const successMessage = document.getElementById('form-success');

        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // 獲取表單數據
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                company: document.getElementById('company').value,
                service: document.getElementById('service').value,
                message: document.getElementById('message').value
            };

            // 這裡可以連接到後端 API
            console.log('Form data:', formData);

            // 模擬提交
            try {
                // 實際應用中，這裡應該呼叫 API
                // const response = await fetch('/api/contact', {
                //     method: 'POST',
                //     headers: { 'Content-Type': 'application/json' },
                //     body: JSON.stringify(formData)
                // });

                // 模擬成功
                await new Promise(resolve => setTimeout(resolve, 1000));

                // 隱藏表單，顯示成功訊息
                form.style.display = 'none';
                successMessage.style.display = 'block';

                // 3 秒後重置
                setTimeout(() => {
                    form.style.display = 'flex';
                    successMessage.style.display = 'none';
                    form.reset();
                }, 3000);

            } catch (error) {
                console.error('Error submitting form:', error);
                alert('提交失敗，請稍後再試或直接發送 Email 給我們。');
            }
        });
    }

    // 平滑滾動
    setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    const offsetTop = target.offsetTop - 80;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
}

// ========================================
// 工具函數
// ========================================

// 防抖函數
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 節流函數
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ========================================
// 頁面載入動畫
// ========================================

class PageLoader {
    constructor() {
        this.init();
    }

    init() {
        // 頁面載入完成後的淡入效果
        window.addEventListener('load', () => {
            document.body.style.opacity = '0';
            setTimeout(() => {
                document.body.style.transition = 'opacity 0.5s ease';
                document.body.style.opacity = '1';
            }, 100);
        });

        // 監聽頁面可見性變化
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('再見！');
            } else {
                console.log('歡迎回來！');
            }
        });
    }
}

// ========================================
// 性能監控（開發用）
// ========================================

class PerformanceMonitor {
    constructor() {
        if (window.location.hostname === 'localhost') {
            this.logPerformance();
        }
    }

    logPerformance() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                const connectTime = perfData.responseEnd - perfData.requestStart;
                const renderTime = perfData.domComplete - perfData.domLoading;

                console.log('%c[Performance Metrics]', 'font-size: 14px; font-weight: bold; color: #7FFF00;');
                console.log(`Page Load: ${pageLoadTime}ms`);
                console.log(`Connect: ${connectTime}ms`);
                console.log(`Render: ${renderTime}ms`);
            }, 0);
        });
    }
}

// ========================================
// 初始化所有模組
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    new MainController();
    new PageLoader();
    new PerformanceMonitor();

    // 設定動態年份
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }

    // 添加一個小的載入歡迎訊息
    console.log('%cAiInPocket 已成功載入', 'font-size: 12px; color: #87CEEB;');
    console.log('%cTip: 試試看在頁面上輸入 "aiinpocket"', 'font-size: 10px; color: #A0D8EF;');
});

// 導出工具函數供其他模組使用
window.utils = {
    debounce,
    throttle
};
