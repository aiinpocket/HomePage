"""
網站風格模板配置
定義 25+ 種不同風格的網站模板元數據
"""

TEMPLATE_STYLES = {
    # 生活服務類 (1-5)
    "perfume": {
        "id": "perfume",
        "name": "香水/美妝",
        "category": "lifestyle",
        "description": "優雅溫馨的美妝香水網站，適合化妝品、香水品牌",
        "colors": {
            "primary": "#FFE4E1",
            "secondary": "#D4AF37",
            "accent": "#FF6B9D",
            "background": "#FFF0F5",
            "text": "#4A0E4E"
        },
        "fonts": {
            "heading": "Georgia, serif",
            "body": "Georgia, serif"
        },
        "style_keywords": ["優雅", "溫馨", "浪漫", "精緻", "女性化"],
        "sample_file": "perfume.html"
    },
    "travel": {
        "id": "travel",
        "name": "旅遊/探險",
        "category": "lifestyle",
        "description": "活力探索的旅遊網站，適合旅行社、探險活動",
        "colors": {
            "primary": "#0077BE",
            "secondary": "#FF6B35",
            "accent": "#87CEEB",
            "background": "#F4E8C1",
            "text": "#333333"
        },
        "fonts": {
            "heading": "Arial, sans-serif",
            "body": "Helvetica, sans-serif"
        },
        "style_keywords": ["冒險", "活力", "自由", "探索", "陽光"],
        "sample_file": "travel.html"
    },
    "restaurant": {
        "id": "restaurant",
        "name": "餐廳/美食",
        "category": "lifestyle",
        "description": "溫暖食慾的餐廳網站，適合餐廳、咖啡廳、美食部落格",
        "colors": {
            "primary": "#8B4513",
            "secondary": "#FF4500",
            "accent": "#FFD700",
            "background": "#FFF8DC",
            "text": "#2F4F4F"
        },
        "fonts": {
            "heading": "Playfair Display, serif",
            "body": "Lato, sans-serif"
        },
        "style_keywords": ["美味", "溫暖", "舒適", "家庭", "傳統"]
    },
    "fitness": {
        "id": "fitness",
        "name": "健身/運動",
        "category": "lifestyle",
        "description": "動感活力的健身網站，適合健身房、運動中心、教練",
        "colors": {
            "primary": "#FF4500",
            "secondary": "#000000",
            "accent": "#FFD700",
            "background": "#F5F5F5",
            "text": "#1A1A1A"
        },
        "fonts": {
            "heading": "Impact, sans-serif",
            "body": "Arial, sans-serif"
        },
        "style_keywords": ["活力", "強壯", "運動", "健康", "專業"]
    },
    "photography": {
        "id": "photography",
        "name": "攝影/工作室",
        "category": "creative",
        "description": "視覺藝術的攝影網站，適合攝影師、工作室、藝術家",
        "colors": {
            "primary": "#000000",
            "secondary": "#FFFFFF",
            "accent": "#FF6B6B",
            "background": "#FAFAFA",
            "text": "#333333"
        },
        "fonts": {
            "heading": "Montserrat, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "style_keywords": ["簡約", "視覺", "藝術", "專業", "現代"]
    },

    # 專業服務類 (6-10)
    "engineer": {
        "id": "engineer",
        "name": "工程師個人頁面",
        "category": "professional",
        "description": "科技簡約的工程師網站，適合軟體工程師、開發者",
        "colors": {
            "primary": "#0A0E27",
            "secondary": "#87CEEB",
            "accent": "#7FFF00",
            "background": "#1A1E35",
            "text": "#E0E0E0"
        },
        "fonts": {
            "heading": "Roboto Mono, monospace",
            "body": "Roboto, sans-serif"
        },
        "style_keywords": ["科技", "極簡", "專業", "代碼", "未來感"]
    },
    "accountant": {
        "id": "accountant",
        "name": "會計師/財務",
        "category": "professional",
        "description": "專業信任的會計網站，適合會計師、財務顧問",
        "colors": {
            "primary": "#003366",
            "secondary": "#FFD700",
            "accent": "#4169E1",
            "background": "#F8F9FA",
            "text": "#2C3E50"
        },
        "fonts": {
            "heading": "Times New Roman, serif",
            "body": "Arial, sans-serif"
        },
        "style_keywords": ["專業", "信任", "穩重", "金融", "權威"]
    },
    "lawyer": {
        "id": "lawyer",
        "name": "律師/法律",
        "category": "professional",
        "description": "權威正式的法律網站，適合律師事務所、法律顧問",
        "colors": {
            "primary": "#1C1C1C",
            "secondary": "#B8860B",
            "accent": "#8B4513",
            "background": "#FFFFFF",
            "text": "#2F4F4F"
        },
        "fonts": {
            "heading": "Garamond, serif",
            "body": "Georgia, serif"
        },
        "style_keywords": ["權威", "專業", "正式", "信賴", "傳統"]
    },
    "doctor": {
        "id": "doctor",
        "name": "醫生/診所",
        "category": "professional",
        "description": "醫療關懷的診所網站，適合診所、醫生、醫療機構",
        "colors": {
            "primary": "#00A8E8",
            "secondary": "#4CAF50",
            "accent": "#FF6B6B",
            "background": "#FFFFFF",
            "text": "#333333"
        },
        "fonts": {
            "heading": "Lato, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "style_keywords": ["關懷", "專業", "清潔", "信任", "健康"]
    },
    "realtor": {
        "id": "realtor",
        "name": "房地產仲介",
        "category": "professional",
        "description": "現代商務的房地產網站，適合房仲、建商、物業管理",
        "colors": {
            "primary": "#2C3E50",
            "secondary": "#E74C3C",
            "accent": "#3498DB",
            "background": "#ECF0F1",
            "text": "#34495E"
        },
        "fonts": {
            "heading": "Raleway, sans-serif",
            "body": "Lato, sans-serif"
        },
        "style_keywords": ["現代", "商務", "專業", "豪華", "信賴"]
    },

    # 創意產業類 (11-15)
    "designer": {
        "id": "designer",
        "name": "設計師作品集",
        "category": "creative",
        "description": "創意視覺的設計作品集，適合平面設計師、UI/UX 設計師",
        "colors": {
            "primary": "#FF006E",
            "secondary": "#8338EC",
            "accent": "#FFBE0B",
            "background": "#FFFFFF",
            "text": "#1A1A1A"
        },
        "fonts": {
            "heading": "Bebas Neue, sans-serif",
            "body": "Roboto, sans-serif"
        },
        "style_keywords": ["創意", "大膽", "視覺", "現代", "藝術"]
    },
    "artist": {
        "id": "artist",
        "name": "藝術家/畫廊",
        "category": "creative",
        "description": "藝術典雅的畫廊網站，適合藝術家、畫廊、展覽",
        "colors": {
            "primary": "#2F2F2F",
            "secondary": "#D4AF37",
            "accent": "#8B0000",
            "background": "#F5F5F5",
            "text": "#1A1A1A"
        },
        "fonts": {
            "heading": "Crimson Text, serif",
            "body": "EB Garamond, serif"
        },
        "style_keywords": ["藝術", "典雅", "文化", "精緻", "歷史"]
    },
    "musician": {
        "id": "musician",
        "name": "音樂家/樂團",
        "category": "creative",
        "description": "音樂節奏的音樂網站，適合音樂家、樂團、DJ",
        "colors": {
            "primary": "#1DB954",
            "secondary": "#191414",
            "accent": "#FF1744",
            "background": "#121212",
            "text": "#FFFFFF"
        },
        "fonts": {
            "heading": "Oswald, sans-serif",
            "body": "Montserrat, sans-serif"
        },
        "style_keywords": ["音樂", "節奏", "活力", "現代", "娛樂"]
    },
    "writer": {
        "id": "writer",
        "name": "作家/部落格",
        "category": "creative",
        "description": "文字閱讀的部落格網站，適合作家、部落客、記者",
        "colors": {
            "primary": "#5D4E37",
            "secondary": "#F4E8C1",
            "accent": "#8B4513",
            "background": "#FFFEF7",
            "text": "#3E2723"
        },
        "fonts": {
            "heading": "Merriweather, serif",
            "body": "Lora, serif"
        },
        "style_keywords": ["文學", "閱讀", "溫暖", "知性", "傳統"]
    },
    "wedding": {
        "id": "wedding",
        "name": "婚紗/婚禮",
        "category": "creative",
        "description": "浪漫夢幻的婚禮網站，適合婚紗攝影、婚禮策劃",
        "colors": {
            "primary": "#FFB6C1",
            "secondary": "#FFD700",
            "accent": "#FF69B4",
            "background": "#FFF5F8",
            "text": "#4A0E4E"
        },
        "fonts": {
            "heading": "Playfair Display, serif",
            "body": "Raleway, sans-serif"
        },
        "style_keywords": ["浪漫", "夢幻", "優雅", "幸福", "典禮"]
    },

    # 商業科技類 (16-20)
    "tech_startup": {
        "id": "tech_startup",
        "name": "科技新創",
        "category": "business",
        "description": "未來創新的科技網站，適合新創公司、科技產品",
        "colors": {
            "primary": "#667EEA",
            "secondary": "#764BA2",
            "accent": "#F093FB",
            "background": "#FFFFFF",
            "text": "#1A202C"
        },
        "fonts": {
            "heading": "Inter, sans-serif",
            "body": "Inter, sans-serif"
        },
        "style_keywords": ["創新", "未來", "科技", "簡潔", "專業"]
    },
    "ecommerce": {
        "id": "ecommerce",
        "name": "電商/購物",
        "category": "business",
        "description": "商品展示的電商網站，適合線上商店、零售業",
        "colors": {
            "primary": "#FF6B6B",
            "secondary": "#4ECDC4",
            "accent": "#FFE66D",
            "background": "#FFFFFF",
            "text": "#2D3748"
        },
        "fonts": {
            "heading": "Poppins, sans-serif",
            "body": "Roboto, sans-serif"
        },
        "style_keywords": ["商品", "購物", "現代", "活潑", "友善"]
    },
    "saas": {
        "id": "saas",
        "name": "SaaS 軟體",
        "category": "business",
        "description": "專業簡潔的 SaaS 網站，適合軟體服務、B2B 公司",
        "colors": {
            "primary": "#2563EB",
            "secondary": "#10B981",
            "accent": "#F59E0B",
            "background": "#F9FAFB",
            "text": "#111827"
        },
        "fonts": {
            "heading": "DM Sans, sans-serif",
            "body": "Inter, sans-serif"
        },
        "style_keywords": ["專業", "簡潔", "商務", "現代", "科技"]
    },
    "gaming": {
        "id": "gaming",
        "name": "遊戲/娛樂",
        "category": "business",
        "description": "趣味互動的遊戲網站，適合遊戲公司、娛樂產業",
        "colors": {
            "primary": "#9D4EDD",
            "secondary": "#FF006E",
            "accent": "#FFB703",
            "background": "#000000",
            "text": "#FFFFFF"
        },
        "fonts": {
            "heading": "Orbitron, sans-serif",
            "body": "Rajdhani, sans-serif"
        },
        "style_keywords": ["趣味", "遊戲", "活力", "酷炫", "互動"]
    },
    "nonprofit": {
        "id": "nonprofit",
        "name": "非營利組織",
        "category": "business",
        "description": "溫暖使命的公益網站，適合非營利組織、社會企業",
        "colors": {
            "primary": "#2F855A",
            "secondary": "#DD6B20",
            "accent": "#3182CE",
            "background": "#FFFFFF",
            "text": "#2D3748"
        },
        "fonts": {
            "heading": "Source Sans Pro, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "style_keywords": ["溫暖", "使命", "希望", "社會", "關懷"]
    },

    # 其他類別 (21-25)
    "education": {
        "id": "education",
        "name": "教育/課程",
        "category": "service",
        "description": "學習成長的教育網站，適合學校、線上課程、補習班",
        "colors": {
            "primary": "#3B82F6",
            "secondary": "#10B981",
            "accent": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#1F2937"
        },
        "fonts": {
            "heading": "Nunito, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "style_keywords": ["學習", "成長", "知識", "友善", "專業"]
    },
    "pet": {
        "id": "pet",
        "name": "寵物/動物",
        "category": "service",
        "description": "可愛療癒的寵物網站，適合寵物店、動物醫院",
        "colors": {
            "primary": "#FF6B9D",
            "secondary": "#4ECDC4",
            "accent": "#FFD93D",
            "background": "#FFF9F0",
            "text": "#2D3748"
        },
        "fonts": {
            "heading": "Quicksand, sans-serif",
            "body": "Nunito, sans-serif"
        },
        "style_keywords": ["可愛", "溫暖", "療癒", "友善", "活潑"]
    },
    "consulting": {
        "id": "consulting",
        "name": "咨詢顧問",
        "category": "professional",
        "description": "專業服務的顧問網站，適合管理顧問、諮詢公司",
        "colors": {
            "primary": "#1E40AF",
            "secondary": "#0891B2",
            "accent": "#F59E0B",
            "background": "#F9FAFB",
            "text": "#111827"
        },
        "fonts": {
            "heading": "Source Serif Pro, serif",
            "body": "Source Sans Pro, sans-serif"
        },
        "style_keywords": ["專業", "信賴", "商務", "權威", "經驗"]
    },
    "event": {
        "id": "event",
        "name": "活動/會議",
        "category": "service",
        "description": "活動宣傳的會議網站，適合活動策劃、展覽、研討會",
        "colors": {
            "primary": "#EC4899",
            "secondary": "#8B5CF6",
            "accent": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#1F2937"
        },
        "fonts": {
            "heading": "Montserrat, sans-serif",
            "body": "Lato, sans-serif"
        },
        "style_keywords": ["活動", "熱鬧", "現代", "專業", "吸引"]
    },
    "resume": {
        "id": "resume",
        "name": "個人簡歷",
        "category": "personal",
        "description": "專業履歷的個人網站，適合求職者、專業人士",
        "colors": {
            "primary": "#374151",
            "secondary": "#6366F1",
            "accent": "#10B981",
            "background": "#FFFFFF",
            "text": "#1F2937"
        },
        "fonts": {
            "heading": "Roboto, sans-serif",
            "body": "Open Sans, sans-serif"
        },
        "style_keywords": ["專業", "簡潔", "清晰", "現代", "正式"]
    },

    # 特殊選項
    "custom": {
        "id": "custom",
        "name": "自訂風格",
        "category": "custom",
        "description": "根據您上傳的圖片或文字描述，由 AI 生成專屬風格",
        "colors": None,  # 由 AI 動態生成
        "fonts": None,   # 由 AI 動態生成
        "style_keywords": ["自訂", "獨特", "個性化", "AI 生成"],
        "requires_input": True  # 需要使用者輸入
    }
}

# 按類別分組
CATEGORIES = {
    "lifestyle": "生活服務",
    "professional": "專業服務",
    "creative": "創意產業",
    "business": "商業科技",
    "service": "其他服務",
    "personal": "個人頁面",
    "custom": "自訂風格"
}


def get_all_templates():
    """獲取所有模板列表"""
    return TEMPLATE_STYLES


def get_template_by_id(template_id):
    """根據 ID 獲取模板"""
    return TEMPLATE_STYLES.get(template_id)


def get_templates_by_category(category):
    """根據類別獲取模板"""
    return {
        k: v for k, v in TEMPLATE_STYLES.items()
        if v.get("category") == category
    }


def search_templates(keywords):
    """根據關鍵字搜尋模板"""
    results = []
    for template_id, template in TEMPLATE_STYLES.items():
        style_keywords = template.get("style_keywords", [])
        if any(keyword.lower() in " ".join(style_keywords).lower() for keyword in keywords):
            results.append(template)
    return results
