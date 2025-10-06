"""
Email 模板 - 多語言支援
支援：繁體中文、英文、日文
"""

EMAIL_TEMPLATES = {
    # 繁體中文
    'zh-TW': {
        'contact_confirmation': {
            'subject': '感謝您的聯繫 - AiInPocket 口袋智慧',
            'body': '''
親愛的 {name}，

感謝您聯繫 AiInPocket（口袋智慧）！

我們已收到您的訊息：

==========================================
感興趣的服務：{service}
訊息內容：
{message}
==========================================

我們的團隊會在 24 小時內仔細審閱您的需求，並盡快與您聯繫。

如有緊急需求，請直接撥打我們的客服專線或透過以下方式聯繫：
📧 Email: help@aiinpocket.com
💬 官網即時聊天：https://aiinpocket.com

再次感謝您對 AiInPocket 的關注！

最誠摯的問候，
AiInPocket 團隊
口袋智慧 | 讓智慧觸手可及

---
此郵件由系統自動發送，請勿直接回覆。
            '''
        },
        'website_generated': {
            'subject': '您的 AI 網站已生成完成 - AiInPocket',
            'body': '''
親愛的 {name}，

您的客製化網站已成功生成！

網站資訊：
- 公司名稱：{company_name}
- 風格：{template}
- 生成時間：{timestamp}

您可以：
1. 線上預覽：{preview_url}
2. 下載完整網站：{download_url}

生成的網站包含：
✓ 完整的 HTML/CSS/JS 檔案
✓ 響應式設計（支援手機、平板、桌面）
✓ 可選的 AI 聊天助手功能
✓ 部署說明文件

如需進一步客製化或有任何問題，歡迎隨時聯繫我們！

祝您使用愉快！

AiInPocket 團隊
口袋智慧 | AI Website Generator

---
預覽連結將在 7 天後失效，請記得下載保存。
            '''
        }
    },

    # English
    'en': {
        'contact_confirmation': {
            'subject': 'Thank You for Contacting Us - AiInPocket',
            'body': '''
Dear {name},

Thank you for contacting AiInPocket!

We have received your inquiry:

==========================================
Service Interest: {service}
Message:
{message}
==========================================

Our team will carefully review your requirements and get back to you within 24 hours.

For urgent matters, please contact us directly:
📧 Email: help@aiinpocket.com
💬 Live Chat: https://aiinpocket.com

Thank you for your interest in AiInPocket!

Best regards,
AiInPocket Team
Intelligence at Your Fingertips

---
This is an automated message. Please do not reply directly.
            '''
        },
        'website_generated': {
            'subject': 'Your AI-Generated Website is Ready - AiInPocket',
            'body': '''
Dear {name},

Your customized website has been successfully generated!

Website Information:
- Company Name: {company_name}
- Style: {template}
- Generated: {timestamp}

You can:
1. Preview Online: {preview_url}
2. Download Complete Site: {download_url}

Your generated website includes:
✓ Complete HTML/CSS/JS files
✓ Responsive design (mobile, tablet, desktop)
✓ Optional AI chat assistant
✓ Deployment instructions

Feel free to contact us for further customization or if you have any questions!

Enjoy!

AiInPocket Team
AI Website Generator

---
Preview link will expire in 7 days. Please download your website.
            '''
        }
    },

    # 日本語
    'ja': {
        'contact_confirmation': {
            'subject': 'お問い合わせありがとうございます - AiInPocket',
            'body': '''
{name} 様

AiInPocketへのお問い合わせありがとうございます！

お問い合わせ内容を受け取りました：

==========================================
ご興味のあるサービス：{service}
メッセージ：
{message}
==========================================

チームがお客様のご要望を慎重に検討し、24時間以内にご連絡いたします。

緊急の場合は、直接お問い合わせください：
📧 メール: help@aiinpocket.com
💬 ライブチャット：https://aiinpocket.com

AiInPocketへのご関心をお寄せいただき、ありがとうございます！

よろしくお願いいたします、
AiInPocketチーム
知能を手の届くところに

---
これは自動送信メールです。直接返信しないでください。
            '''
        },
        'website_generated': {
            'subject': 'AIウェブサイトが完成しました - AiInPocket',
            'body': '''
{name} 様

カスタマイズされたウェブサイトの生成が完了しました！

ウェブサイト情報：
- 会社名：{company_name}
- スタイル：{template}
- 生成日時：{timestamp}

以下のことができます：
1. オンラインプレビュー：{preview_url}
2. サイト全体をダウンロード：{download_url}

生成されたウェブサイトには以下が含まれます：
✓ 完全なHTML/CSS/JSファイル
✓ レスポンシブデザイン（モバイル、タブレット、デスクトップ）
✓ オプションのAIチャットアシスタント
✓ デプロイ手順書

さらなるカスタマイズやご質問がございましたら、お気軽にお問い合わせください！

お楽しみください！

AiInPocketチーム
AI Website Generator

---
プレビューリンクは7日後に期限切れとなります。ウェブサイトをダウンロードしてください。
            '''
        }
    }
}

# 服務類型翻譯
SERVICE_TRANSLATIONS = {
    'zh-TW': {
        'ai': 'AI 解決方案',
        'cloud': '雲端架構',
        'devops': 'DevOps 工程',
        'consulting': '技術諮詢',
        'other': '其他'
    },
    'en': {
        'ai': 'AI Solutions',
        'cloud': 'Cloud Architecture',
        'devops': 'DevOps Engineering',
        'consulting': 'Technical Consulting',
        'other': 'Other'
    },
    'ja': {
        'ai': 'AIソリューション',
        'cloud': 'クラウドアーキテクチャ',
        'devops': 'DevOpsエンジニアリング',
        'consulting': '技術コンサルティング',
        'other': 'その他'
    }
}


def get_email_template(template_name: str, language: str = 'zh-TW'):
    """
    取得指定語言的 Email 模板

    Args:
        template_name: 模板名稱 ('contact_confirmation', 'website_generated')
        language: 語言代碼 ('zh-TW', 'en', 'ja')

    Returns:
        dict: 包含 subject 和 body 的字典
    """
    # 預設繁體中文
    if language not in EMAIL_TEMPLATES:
        language = 'zh-TW'

    templates = EMAIL_TEMPLATES.get(language, EMAIL_TEMPLATES['zh-TW'])
    return templates.get(template_name, templates['contact_confirmation'])


def translate_service(service_code: str, language: str = 'zh-TW'):
    """
    翻譯服務類型

    Args:
        service_code: 服務代碼 ('ai', 'cloud', 'devops', etc.)
        language: 語言代碼

    Returns:
        str: 翻譯後的服務名稱
    """
    if language not in SERVICE_TRANSLATIONS:
        language = 'zh-TW'

    translations = SERVICE_TRANSLATIONS.get(language, SERVICE_TRANSLATIONS['zh-TW'])
    return translations.get(service_code, service_code)


def format_email(template_name: str, language: str, **kwargs):
    """
    格式化 Email 內容

    Args:
        template_name: 模板名稱
        language: 語言代碼
        **kwargs: 模板變數

    Returns:
        dict: {'subject': str, 'body': str}
    """
    template = get_email_template(template_name, language)

    # 翻譯服務類型（如果存在）
    if 'service' in kwargs:
        kwargs['service'] = translate_service(kwargs['service'], language)

    # 格式化主旨和內容
    subject = template['subject'].format(**kwargs)
    body = template['body'].format(**kwargs)

    return {
        'subject': subject,
        'body': body
    }
