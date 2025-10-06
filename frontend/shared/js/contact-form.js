/**
 * 聯絡表單處理（支援多語言）
 */

document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');

    if (!contactForm) return;

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 取得當前語言
        const language = getCurrentLanguage();

        // 取得表單資料
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            company: document.getElementById('company')?.value || '',
            service: document.getElementById('service').value,
            message: document.getElementById('message').value,
            language: language  // 添加語言資訊
        };

        // 顯示載入狀態
        const submitBtn = contactForm.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.innerHTML;
        submitBtn.disabled = true;

        const loadingTexts = {
            'zh-TW': '送出中...',
            'en': 'Sending...',
            'ja': '送信中...'
        };
        submitBtn.innerHTML = `<span>${loadingTexts[language] || loadingTexts['zh-TW']}</span>`;

        try {
            // 發送 API 請求
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // 顯示成功訊息
                contactForm.style.display = 'none';
                const successDiv = document.getElementById('form-success');
                if (successDiv) {
                    successDiv.style.display = 'block';
                }

                // 重置表單
                contactForm.reset();

                // 3 秒後恢復表單
                setTimeout(() => {
                    contactForm.style.display = 'block';
                    if (successDiv) {
                        successDiv.style.display = 'none';
                    }
                }, 5000);
            } else {
                // 顯示錯誤訊息
                alert(result.message);
            }

        } catch (error) {
            console.error('Form submission error:', error);

            const errorMessages = {
                'zh-TW': '提交失敗，請稍後再試',
                'en': 'Submission failed. Please try again later.',
                'ja': '送信に失敗しました。後でもう一度お試しください'
            };

            alert(errorMessages[language] || errorMessages['zh-TW']);
        } finally {
            // 恢復按鈕
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalBtnText;
        }
    });
});
