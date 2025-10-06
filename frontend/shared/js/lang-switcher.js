/**
 * 語言切換器初始化
 */

// 頁面載入時初始化語言切換器
document.addEventListener('DOMContentLoaded', () => {
    // 建立語言切換器 HTML
    const languageSwitcher = document.createElement('div');
    languageSwitcher.className = 'language-switcher';
    languageSwitcher.innerHTML = `
        <button class="lang-btn ${getCurrentLanguage() === 'zh-TW' ? 'active' : ''}" data-lang="zh-TW">中文</button>
        <button class="lang-btn ${getCurrentLanguage() === 'en' ? 'active' : ''}" data-lang="en">EN</button>
        <button class="lang-btn ${getCurrentLanguage() === 'ja' ? 'active' : ''}" data-lang="ja">日本語</button>
    `;

    // 插入到 body
    document.body.appendChild(languageSwitcher);

    // 綁定語言切換事件
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            setLanguage(lang);

            // 更新按鈕狀態
            document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // 初始化頁面語言
    updatePageContent();
});

// 監聽語言變更事件（用於後端 API 調用）
document.addEventListener('languageChanged', (e) => {
    const language = e.detail.language;
    console.log(`Language changed to: ${language}`);

    // 可在此處添加額外的語言變更處理邏輯
    // 例如：重新載入特定內容、通知後端等
});
