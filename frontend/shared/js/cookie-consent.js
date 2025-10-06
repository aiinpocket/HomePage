/**
 * Cookie 同意橫幅（GDPR/CCPA 合規）
 * Google AdSense 必備
 */

document.addEventListener('DOMContentLoaded', () => {
    // 檢查是否已同意
    const hasConsent = localStorage.getItem('cookieConsent');

    if (!hasConsent) {
        showCookieBanner();
    } else {
        // 已同意，載入廣告和分析
        loadAnalytics();
    }
});

function showCookieBanner() {
    const banner = document.createElement('div');
    banner.className = 'cookie-consent-banner';
    banner.innerHTML = `
        <div class="cookie-content">
            <div class="cookie-text">
                <h3 data-i18n="cookie.title">🍪 Cookie 使用聲明</h3>
                <p data-i18n="cookie.description">
                    本網站使用 Cookie 來改善使用體驗，並透過 Google AdSense 展示廣告。
                    繼續瀏覽即表示您同意我們使用 Cookie。
                    <a href="/corporate/privacy.html" data-i18n="cookie.learnMore">了解更多</a>
                </p>
            </div>
            <div class="cookie-buttons">
                <button id="cookie-accept" class="btn btn-primary" data-i18n="cookie.accept">
                    接受所有 Cookie
                </button>
                <button id="cookie-reject" class="btn btn-secondary" data-i18n="cookie.reject">
                    僅必要 Cookie
                </button>
            </div>
        </div>
    `;

    document.body.appendChild(banner);

    // 套用翻譯（如果 i18n 已載入）
    if (typeof updatePageContent === 'function') {
        updatePageContent();
    }

    // 綁定事件
    document.getElementById('cookie-accept').addEventListener('click', () => {
        acceptCookies();
        banner.remove();
    });

    document.getElementById('cookie-reject').addEventListener('click', () => {
        rejectCookies();
        banner.remove();
    });
}

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    loadAnalytics();
    loadAds();
}

function rejectCookies() {
    localStorage.setItem('cookieConsent', 'rejected');
    localStorage.setItem('cookieConsentDate', new Date().toISOString());
    // 僅載入必要功能，不載入廣告和分析
}

function loadAnalytics() {
    // Google Analytics 4
    const GA_ID = 'G-XXXXXXXXXX'; // 替換為您的 GA4 ID

    // 載入 gtag.js
    const script1 = document.createElement('script');
    script1.async = true;
    script1.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
    document.head.appendChild(script1);

    // 初始化 gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', GA_ID, {
        'anonymize_ip': true, // 匿名化 IP（GDPR 合規）
        'cookie_flags': 'SameSite=None;Secure'
    });

    console.log('[Analytics] Google Analytics loaded');
}

function loadAds() {
    // Google AdSense
    const ADSENSE_ID = 'ca-pub-XXXXXXXXXXXXXXXX'; // 替換為您的 AdSense ID

    const script = document.createElement('script');
    script.async = true;
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_ID}`;
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);

    console.log('[Ads] Google AdSense loaded');
}
