/**
 * 多語言系統 (i18n)
 * 支援：繁體中文 (zh-TW)、英文 (en)、日文 (ja)
 */

const translations = {
    // 繁體中文
    'zh-TW': {
        // 導航列
        nav: {
            home: '首頁',
            portfolio: '作品集',
            techStack: '技術棧',
            about: '關於我們',
            contact: '聯絡我們',
            generator: 'AI 生成器'
        },

        // 首頁
        home: {
            hero: {
                title1: '將未來科技',
                title2: '裝進你的口袋',
                subtitle: '人工智慧 × 雲端架構 × DevOps 自動化',
                desc1: 'AiInPocket 致力於將最先進的 AI 技術與雲端解決方案，',
                desc2: '以最簡潔的方式交付到您的手中。',
                startBtn: '開始合作',
                portfolioBtn: '查看案例'
            },
            services: {
                title: '核心服務',
                ai: {
                    title: 'AI 解決方案',
                    desc: '深度學習、自然語言處理、電腦視覺、智能自動化。打造專屬的 AI 模型，賦能您的業務。',
                    feature1: '客製化 AI 模型訓練',
                    feature2: 'LLM 應用整合',
                    feature3: '智能數據分析',
                    feature4: '自動化決策系統'
                },
                cloud: {
                    title: '雲端架構',
                    desc: '可擴展、高可用、成本優化的雲端方案。從零開始或優化現有架構。',
                    feature1: '雲原生架構設計',
                    feature2: '容器化與編排',
                    feature3: '無伺服器架構',
                    feature4: '多雲策略'
                },
                devops: {
                    title: 'DevOps 工程',
                    desc: 'CI/CD 流程、基礎設施即代碼、監控告警。加速開發，提升穩定性。',
                    feature1: '自動化部署管道',
                    feature2: '基礎設施即代碼 (IaC)',
                    feature3: '監控與日誌系統',
                    feature4: '安全性掃描'
                }
            },
            stats: {
                satisfaction: '客戶滿意度',
                projects: '專案交付',
                support: '全天候支援',
                years: '服務年限',
                yearsUnit: '年+'
            },
            cta: {
                title: '準備好開啟 AI 之旅了嗎？',
                desc: '讓我們一起探索無限可能，打造屬於您的智能解決方案',
                btn: '立即聯繫'
            },
            easterEgg: {
                title: '[彩蛋觸發！]',
                text: '你發現了隱藏的魔法咒語！',
                close: '關閉'
            }
        },

        // 作品集
        portfolio: {
            header: {
                title: '作品集',
                subtitle: '我們引以為傲的專案成果'
            },
            filters: {
                all: '全部',
                ai: 'AI 解決方案',
                cloud: '雲端架構',
                devops: 'DevOps'
            },
            project1: {
                tag: 'AI 解決方案',
                title: '智能客服系統',
                desc: '為大型電商平台打造的 AI 客服系統，結合 GPT-4 與客製化知識庫，大幅提升客戶滿意度並降低 60% 人力成本。',
                stat1: '<strong>60%</strong> 成本降低',
                stat2: '<strong>95%</strong> 準確率',
                stat3: '<strong>24/7</strong> 全天候服務'
            },
            project2: {
                tag: '雲端架構',
                title: '微服務架構遷移',
                desc: '協助金融科技公司從單體架構遷移至 Kubernetes 微服務架構，實現高可用性與彈性擴展。',
                stat1: '<strong>99.9%</strong> 可用性',
                stat2: '<strong>3x</strong> 性能提升',
                stat3: '<strong>50%</strong> 成本優化'
            },
            project3: {
                tag: 'DevOps',
                title: 'CI/CD 自動化流程',
                desc: '建立完整的自動化部署管道，從代碼提交到生產環境部署，縮短發布週期至每日多次部署。',
                stat1: '<strong>10x</strong> 部署頻率',
                stat2: '<strong>80%</strong> 時間節省',
                stat3: '<strong>0</strong> 停機部署'
            },
            project4: {
                tag: '雲端架構',
                title: '全球 CDN 部署',
                desc: '為跨國媒體平台設計全球內容分發網路，優化全球用戶訪問速度與體驗。',
                stat1: '<strong>70%</strong> 延遲降低',
                stat2: '<strong>150+</strong> 節點',
                stat3: '<strong>5大洲</strong> 覆蓋'
            },
            project5: {
                tag: 'DevOps',
                title: '安全性自動化掃描',
                desc: '整合多種安全掃描工具至 CI/CD 流程，自動化漏洞檢測與合規性檢查。',
                stat1: '<strong>100%</strong> 代碼掃描',
                stat2: '<strong>90%</strong> 漏洞減少',
                stat3: '<strong>自動化</strong> 修復建議'
            },
            opensource: {
                title: '開源項目',
                project1: {
                    title: 'AI 每日分析台股籌碼',
                    desc: '每日自動分析台灣股市三大法人籌碼動向，提供視覺化報表與趨勢洞察。'
                },
                project2: {
                    title: '智慧流程編排引擎',
                    badge: '開發中',
                    desc: '智慧化的工作流程編排引擎，讓複雜的自動化流程變得簡單直覺。'
                }
            },
            cta: {
                title: '想要看到您的專案在這裡嗎？',
                desc: '讓我們一起打造下一個成功案例',
                btn: '開始合作'
            }
        },

        // 技術棧
        techStack: {
            header: {
                title: '技術棧',
                subtitle: '我們使用最前沿的技術工具'
            },
            ai: {
                title: 'AI & Machine Learning',
                python: 'AI 整合與自動化',
                openai: 'GPT-4 API 串接',
                ollama: '本地 LLM 部署',
                linebot: '聊天機器人開發',
                langchain: 'LLM 應用框架',
                pytorch: '研究與生產環境',
                huggingface: '預訓練模型'
            },
            cloud: {
                title: 'Cloud & Infrastructure',
                openshift: '企業級容器平台',
                gcp: '雲端服務',
                k8s: '容器編排',
                docker: '容器化技術',
                ansible: '自動化配置',
                serverless: '無伺服器架構'
            },
            devops: {
                title: 'DevOps & CI/CD'
            },
            languages: {
                title: '程式語言'
            },
            systems: {
                title: '系統操作'
            },
            tools: {
                title: '工具與平台'
            },
            web: {
                title: 'Web & Backend'
            },
            philosophy: {
                title: '我們的技術理念',
                principle1: {
                    title: '適用性優先',
                    desc: '選擇最適合問題的工具，而非最熱門的技術'
                },
                principle2: {
                    title: '持續學習',
                    desc: '緊跟技術趨勢，定期評估並更新技術棧'
                },
                principle3: {
                    title: '性能為王',
                    desc: '追求極致性能，優化每一個環節'
                },
                principle4: {
                    title: '安全第一',
                    desc: '從設計階段就考慮安全性，而非事後補救'
                }
            },
            cta: {
                title: '想了解我們如何運用這些技術？',
                desc: '查看我們的實際案例或直接與我們聊聊',
                portfolioBtn: '查看作品集',
                contactBtn: '聯絡我們'
            }
        },

        // 關於我們
        about: {
            header: {
                title: '關於我們',
                subtitle: '讓智慧觸手可及的使命'
            },
            mission: {
                title: '我們的願景',
                text1: '在這個 AI 快速發展的時代，我們相信科技應該是<strong>觸手可及</strong>的。AiInPocket 致力於將最先進的人工智慧技術、雲端架構與 DevOps 解決方案，以最簡潔、最高效的方式交付到每位客戶手中。',
                text2: '就像口袋一樣 —— <strong>隨時可用、隨處可及、隨心所欲</strong>。'
            },
            values: {
                value1: {
                    title: '專注客戶',
                    desc: '深入理解客戶需求，提供量身訂製的解決方案'
                },
                value2: {
                    title: '追求卓越',
                    desc: '不斷精進技術，追求極致性能與品質'
                },
                value3: {
                    title: '誠信合作',
                    desc: '以透明溝通與長期夥伴關係為基礎'
                },
                value4: {
                    title: '持續創新',
                    desc: '擁抱變化，積極探索新技術與新可能'
                }
            },
            team: {
                title: '核心團隊',
                member1: {
                    name: '技術長',
                    role: 'Chief Technology Officer',
                    bio: '10+ 年軟體開發與 DevOps 經驗，專精於雲端架構設計與自動化流程'
                },
                member2: {
                    name: 'AI 應用主管',
                    role: 'Head of AI Applications',
                    bio: '專注於 AI 的應用整合，思考如何組合搭配各種 AI 工具與技術，以滿足客戶的實際需求'
                },
                member3: {
                    name: '全端工程師',
                    role: 'Full-Stack Engineer',
                    bio: '精通前後端開發，致力於打造流暢的使用者體驗與高效能系統'
                },
                member4: {
                    name: '品質保證工程師',
                    role: 'QA Engineer',
                    bio: '進行大量測試確保產品品質，並設計自動化部署流程中的重點測試項目'
                }
            },
            timeline: {
                title: '發展歷程',
                year1: {
                    title: '創立初期',
                    desc: 'AiInPocket 成立，專注於 AI 與雲端技術諮詢'
                },
                year2: {
                    title: 'AI 助手元年',
                    desc: '結合 GPT-3 技術，為企業打造本地化 AI 小助手'
                },
                year3: {
                    title: '普及 AI 應用',
                    desc: '推出 LINE 自動問答機器人，協助大眾輕鬆接觸 AI'
                },
                year4: {
                    title: '企業代管服務',
                    desc: '為中小企業提供 SRE 代管服務，管理 50+ 雲端應用'
                },
                year5: {
                    title: '深化整合',
                    desc: '協助企業串接金流系統與政府單位自動化申報服務'
                }
            },
            whyUs: {
                title: '為什麼選擇 AiInPocket？',
                reason1: {
                    title: '實戰經驗',
                    desc: '50+ 專案經驗，涵蓋各產業領域，從金融到製造業'
                },
                reason2: {
                    title: '技術深度',
                    desc: '團隊成員皆具備深厚技術背景，持續追蹤最新技術趨勢'
                },
                reason3: {
                    title: '快速交付',
                    desc: '敏捷開發流程，從需求到上線平均僅需 2-4 週'
                },
                reason4: {
                    title: '長期支援',
                    desc: '提供 7x24 技術支援，確保系統穩定運行'
                }
            },
            cta: {
                title: '準備好與我們一起創造未來了嗎？',
                desc: '讓我們開始對話，探索無限可能',
                btn: '聯絡我們'
            }
        },

        // 聯絡我們
        contact: {
            header: {
                title: '聯絡我們',
                subtitle: '讓我們開始對話'
            },
            info: {
                email: {
                    title: 'Email',
                    note: '24 小時內回覆'
                },
                chat: {
                    title: '即時對話',
                    value: 'AI 助手',
                    note: '點擊右下角聊天按鈕'
                },
                social: {
                    title: '社群媒體',
                    note: '關注我們的最新動態'
                },
                hours: {
                    title: '服務時間',
                    value: '全年無休',
                    note: '7x24 技術支援'
                }
            },
            form: {
                title: '快速諮詢',
                name: '姓名 *',
                namePlaceholder: '您的姓名',
                email: 'Email *',
                emailPlaceholder: 'your@email.com',
                company: '公司名稱',
                companyPlaceholder: '您的公司（選填）',
                service: '感興趣的服務 *',
                serviceOption0: '請選擇...',
                serviceOption1: 'AI 解決方案',
                serviceOption2: '雲端架構',
                serviceOption3: 'DevOps 工程',
                serviceOption4: '技術諮詢',
                serviceOption5: '其他',
                message: '訊息 *',
                messagePlaceholder: '請描述您的需求或想法...',
                submit: '送出訊息',
                note: '提交後，我們會在 24 小時內回覆您',
                successTitle: '訊息已送出！',
                successMessage: '感謝您的聯繫，我們會盡快回覆您。'
            },
            faq: {
                title: '常見問題',
                q1: {
                    question: '專案通常需要多久時間？',
                    answer: '依專案複雜度而定，一般的 AI 應用或雲端架構專案約需 2-8 週。我們會在初步評估後提供詳細時程規劃。'
                },
                q2: {
                    question: '如何收費？',
                    answer: '我們提供彈性的計費方式，包括專案制、時數制、或長期技術顧問合約。會根據您的需求提供最適合的方案。'
                },
                q3: {
                    question: '提供哪些技術支援？',
                    answer: '我們提供 7x24 技術支援，包括系統監控、緊急修復、定期維護、以及技術諮詢服務。'
                },
                q4: {
                    question: '可以客製化解決方案嗎？',
                    answer: '當然！我們專注於提供量身訂製的解決方案，會深入了解您的業務需求並設計最適合的技術架構。'
                },
                q5: {
                    question: '是否提供教育訓練？',
                    answer: '是的，我們會在專案交付時提供完整的文件與培訓，確保您的團隊能夠順利接手維運。'
                },
                q6: {
                    question: '如何開始合作？',
                    answer: '只需填寫上方表單或直接來信，我們會安排免費的初步諮詢，了解您的需求並提供初步建議。'
                }
            },
            process: {
                title: '合作流程',
                step1: {
                    title: '需求諮詢',
                    desc: '深入了解您的需求與目標'
                },
                step2: {
                    title: '方案規劃',
                    desc: '設計技術架構與實施計畫'
                },
                step3: {
                    title: '開發實作',
                    desc: '敏捷開發，定期交付成果'
                },
                step4: {
                    title: '部署上線',
                    desc: '確保穩定運行並提供支援'
                }
            }
        },

        // 隱私權政策
        privacy: {
            header: {
                title: '隱私權政策',
                subtitle: '最後更新：2025 年 10 月 6 日'
            },
            section1: {
                title: '1. 資訊收集',
                intro: '我們收集以下類型的資訊：',
                item1: '<strong>個人資訊：</strong>當您透過聯絡表單與我們聯繫時，我們會收集您的姓名、電子郵件地址和訊息內容。',
                item2: '<strong>使用資訊：</strong>我們使用 Google Analytics 來收集網站使用統計資訊，包括瀏覽器類型、訪問時間、頁面瀏覽記錄等。',
                item3: '<strong>Cookie：</strong>我們使用 Cookie 來改善使用者體驗和網站功能。'
            },
            section2: {
                title: '2. Google AdSense 廣告',
                intro: '本網站使用 Google AdSense 來展示廣告。Google 及其合作夥伴可能會：',
                item1: '使用 Cookie 來根據您過去對本網站或其他網站的訪問來顯示廣告',
                item2: '使用廣告 Cookie 讓 Google 及其合作夥伴根據使用者造訪本網站和/或網際網路上其他網站的情形向使用者放送廣告',
                item3: '您可以前往 <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">廣告設定</a> 停用個人化廣告'
            },
            section3: {
                title: '3. Cookie 使用聲明',
                intro: '本網站使用以下類型的 Cookie：',
                item1: '<strong>必要 Cookie：</strong>用於網站基本功能（如語言選擇）',
                item2: '<strong>分析 Cookie：</strong>Google Analytics 用於分析網站流量',
                item3: '<strong>廣告 Cookie：</strong>Google AdSense 用於展示相關廣告',
                note: '您可以透過瀏覽器設定管理或刪除 Cookie。請注意，禁用 Cookie 可能會影響網站功能。'
            },
            section4: {
                title: '4. 資訊使用',
                intro: '我們使用收集的資訊來：',
                item1: '回應您的詢問和提供服務',
                item2: '改善網站內容和使用者體驗',
                item3: '發送產品更新和行銷資訊（僅在您同意的情況下）',
                item4: '分析網站使用趨勢'
            },
            section5: {
                title: '5. 第三方服務',
                intro: '本網站使用以下第三方服務：',
                item1: '<strong>Google Analytics：</strong><a href="https://policies.google.com/privacy" target="_blank" rel="noopener">隱私權政策</a>',
                item2: '<strong>Google AdSense：</strong><a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">廣告政策</a>'
            },
            section6: {
                title: '6. 資料安全',
                intro: '我們採取合理的技術和組織措施來保護您的個人資訊，包括：',
                item1: '使用 HTTPS 加密傳輸',
                item2: '限制資料存取權限',
                item3: '定期安全審查'
            },
            section7: {
                title: '7. 您的權利',
                intro: '根據 GDPR 和相關法規，您有權：',
                item1: '存取您的個人資料',
                item2: '更正不準確的資料',
                item3: '要求刪除資料',
                item4: '反對處理您的資料',
                item5: '資料可攜性',
                contact: '如需行使這些權利，請聯繫：<a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>'
            },
            section8: {
                title: '8. 兒童隱私',
                text: '本網站不針對 13 歲以下兒童。我們不會故意收集兒童的個人資訊。'
            },
            section9: {
                title: '9. 政策變更',
                text: '我們可能會不時更新本隱私權政策。重大變更時，我們會在網站上發布通知。'
            },
            section10: {
                title: '10. 聯絡我們',
                intro: '如對本隱私權政策有任何疑問，請聯繫：',
                item1: '<strong>Email：</strong><a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>',
                item2: '<strong>一般聯繫：</strong><a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>'
            }
        },

        // Footer
        footer: {
            tagline: '讓智慧觸手可及',
            services: '服務',
            contactUs: '聯絡',
            privacy: '隱私權政策',
            email: 'Email',
            copyright: 'AiInPocket. All rights reserved.',
            poweredBy: '/// Powered by AI & Innovation ///'
        },

        // 彩蛋
        easterEgg: {
            title: '[彩蛋觸發！]',
            text: '你發現了隱藏的魔法咒語！',
            magic: 'AI is in your pocket now!',
            btnClose: '關閉'
        },

        landing: {
            title: 'AI 網站生成器',
            subtitle: '選擇您的目的地：訪問公司網站或開始生成 AI 驅動的網站。',
            startGenerator: '開始生成',
            corporateWebsite: '公司網站'
        },

        cookie: {
            title: '🍪 Cookie 使用聲明',
            description: '本網站使用 Cookie 來改善使用體驗，並透過 Google AdSense 展示廣告。繼續瀏覽即表示您同意我們使用 Cookie。',
            learnMore: '了解更多',
            accept: '接受所有 Cookie',
            reject: '僅必要 Cookie'
        }
    },

    // English
    'en': {
        nav: {
            home: 'Home',
            portfolio: 'Portfolio',
            techStack: 'Tech Stack',
            about: 'About Us',
            contact: 'Contact',
            generator: 'AI Generator'
        },

        home: {
            hero: {
                title1: 'Future Technology',
                title2: 'In Your Pocket',
                subtitle: 'AI × Cloud × DevOps Automation',
                desc1: 'AiInPocket delivers cutting-edge AI and cloud solutions',
                desc2: 'in the most streamlined way possible.',
                startBtn: 'Get Started',
                portfolioBtn: 'View Cases'
            },
            services: {
                title: 'Core Services',
                ai: {
                    title: 'AI Solutions',
                    desc: 'Deep learning, NLP, computer vision, intelligent automation. Build custom AI models to empower your business.',
                    feature1: 'Custom AI Model Training',
                    feature2: 'LLM Application Integration',
                    feature3: 'Intelligent Data Analysis',
                    feature4: 'Automated Decision Systems'
                },
                cloud: {
                    title: 'Cloud Architecture',
                    desc: 'Scalable, highly available, cost-optimized cloud solutions. Build from scratch or optimize existing infrastructure.',
                    feature1: 'Cloud-Native Architecture Design',
                    feature2: 'Containerization & Orchestration',
                    feature3: 'Serverless Architecture',
                    feature4: 'Multi-Cloud Strategy'
                },
                devops: {
                    title: 'DevOps Engineering',
                    desc: 'CI/CD pipelines, infrastructure as code, monitoring & alerting. Accelerate development and improve stability.',
                    feature1: 'Automated Deployment Pipelines',
                    feature2: 'Infrastructure as Code (IaC)',
                    feature3: 'Monitoring & Logging Systems',
                    feature4: 'Security Scanning'
                }
            },
            stats: {
                satisfaction: 'Client Satisfaction',
                projects: 'Projects Delivered',
                support: '24/7 Support',
                years: 'Years of Service',
                yearsUnit: 'Years+'
            },
            cta: {
                title: 'Ready to Start Your AI Journey?',
                desc: 'Let\'s explore infinite possibilities and build your intelligent solutions',
                btn: 'Contact Us'
            },
            easterEgg: {
                title: '[Easter Egg Triggered!]',
                text: 'You discovered the hidden magic spell!',
                close: 'Close'
            }
        },

        portfolio: {
            header: {
                title: 'Portfolio',
                subtitle: 'Projects We\'re Proud Of'
            },
            filters: {
                all: 'All',
                ai: 'AI Solutions',
                cloud: 'Cloud Architecture',
                devops: 'DevOps'
            },
            project1: {
                tag: 'AI Solutions',
                title: 'AI Customer Service',
                desc: 'AI-powered customer service system for major e-commerce platform, combining GPT-4 with custom knowledge base, significantly improving satisfaction while reducing costs by 60%.',
                stat1: '<strong>60%</strong> Cost Reduction',
                stat2: '<strong>95%</strong> Accuracy',
                stat3: '<strong>24/7</strong> Service'
            },
            project2: {
                tag: 'Cloud Architecture',
                title: 'Microservices Migration',
                desc: 'Helped fintech company migrate from monolith to Kubernetes microservices architecture, achieving high availability and elastic scaling.',
                stat1: '<strong>99.9%</strong> Availability',
                stat2: '<strong>3x</strong> Performance',
                stat3: '<strong>50%</strong> Cost Optimization'
            },
            project3: {
                tag: 'DevOps',
                title: 'CI/CD Automation',
                desc: 'Built complete automated deployment pipeline from code commit to production, reducing release cycle to multiple deployments per day.',
                stat1: '<strong>10x</strong> Deploy Frequency',
                stat2: '<strong>80%</strong> Time Saved',
                stat3: '<strong>0</strong> Downtime'
            },
            project4: {
                tag: 'Cloud Architecture',
                title: 'Global CDN Deployment',
                desc: 'Designed global content delivery network for international media platform, optimizing access speed and user experience worldwide.',
                stat1: '<strong>70%</strong> Latency Reduced',
                stat2: '<strong>150+</strong> Nodes',
                stat3: '<strong>5 Continents</strong> Coverage'
            },
            project5: {
                tag: 'DevOps',
                title: 'Security Automation',
                desc: 'Integrated security scanning tools into CI/CD pipeline, automating vulnerability detection and compliance checks.',
                stat1: '<strong>100%</strong> Code Scanned',
                stat2: '<strong>90%</strong> Vulnerabilities Reduced',
                stat3: '<strong>Automated</strong> Fix Suggestions'
            },
            opensource: {
                title: 'Open Source Projects',
                project1: {
                    title: 'AI Daily TW Stock Institutional Analysis',
                    desc: 'Daily automated analysis of Taiwan stock market institutional investor trends, providing visual reports and trend insights.'
                },
                project2: {
                    title: 'Smart Workflow Orchestration Engine',
                    badge: 'In Development',
                    desc: 'An intelligent workflow orchestration engine that makes complex automation processes simple and intuitive.'
                }
            },
            cta: {
                title: 'Want to See Your Project Here?',
                desc: 'Let\'s build the next success story together',
                btn: 'Get Started'
            }
        },

        techStack: {
            header: {
                title: 'Tech Stack',
                subtitle: 'Cutting-Edge Technologies We Use'
            },
            ai: {
                title: 'AI & Machine Learning',
                python: 'AI Integration & Automation',
                openai: 'GPT-4 API Integration',
                ollama: 'Local LLM Deployment',
                linebot: 'Chatbot Development',
                langchain: 'LLM Application Framework',
                pytorch: 'Research & Production',
                huggingface: 'Pre-trained Models'
            },
            cloud: {
                title: 'Cloud & Infrastructure',
                openshift: 'Enterprise Container Platform',
                gcp: 'Cloud Services',
                k8s: 'Container Orchestration',
                docker: 'Containerization',
                ansible: 'Configuration Automation',
                serverless: 'Serverless Architecture'
            },
            devops: {
                title: 'DevOps & CI/CD'
            },
            languages: {
                title: 'Programming Languages'
            },
            systems: {
                title: 'System Operations'
            },
            tools: {
                title: 'Tools & Platforms'
            },
            web: {
                title: 'Web & Backend'
            },
            philosophy: {
                title: 'Our Technical Philosophy',
                principle1: {
                    title: 'Fit for Purpose',
                    desc: 'Choose the right tool for the problem, not the trendiest technology'
                },
                principle2: {
                    title: 'Continuous Learning',
                    desc: 'Stay ahead of tech trends, regularly evaluate and update our stack'
                },
                principle3: {
                    title: 'Performance First',
                    desc: 'Pursue optimal performance, optimize every aspect'
                },
                principle4: {
                    title: 'Security by Design',
                    desc: 'Consider security from day one, not as an afterthought'
                }
            },
            cta: {
                title: 'Want to Know How We Use These Technologies?',
                desc: 'Check out our case studies or chat with us',
                portfolioBtn: 'View Portfolio',
                contactBtn: 'Contact Us'
            }
        },

        about: {
            header: {
                title: 'About Us',
                subtitle: 'Our Mission to Make Intelligence Accessible'
            },
            mission: {
                title: 'Our Vision',
                text1: 'In this rapidly evolving AI era, we believe technology should be <strong>accessible</strong>. AiInPocket is dedicated to delivering cutting-edge AI technology, cloud architecture, and DevOps solutions in the most streamlined and efficient way to every client.',
                text2: 'Just like a pocket — <strong>always available, anywhere accessible, at your command</strong>.'
            },
            values: {
                value1: {
                    title: 'Customer Focus',
                    desc: 'Deep understanding of client needs, providing tailored solutions'
                },
                value2: {
                    title: 'Pursuit of Excellence',
                    desc: 'Continuously refining technology, pursuing optimal performance and quality'
                },
                value3: {
                    title: 'Honest Collaboration',
                    desc: 'Building on transparent communication and long-term partnerships'
                },
                value4: {
                    title: 'Continuous Innovation',
                    desc: 'Embracing change, actively exploring new technologies and possibilities'
                }
            },
            team: {
                title: 'Core Team',
                member1: {
                    name: 'Chief Technology Officer',
                    role: 'Chief Technology Officer',
                    bio: '10+ years of software development and DevOps experience, specializing in cloud architecture design and automation'
                },
                member2: {
                    name: 'Head of AI Applications',
                    role: 'Head of AI Applications',
                    bio: 'Focused on AI application integration, designing how to combine and orchestrate various AI tools and technologies to meet client needs'
                },
                member3: {
                    name: 'Full-Stack Engineer',
                    role: 'Full-Stack Engineer',
                    bio: 'Proficient in frontend and backend development, dedicated to creating smooth user experiences and high-performance systems'
                },
                member4: {
                    name: 'QA Engineer',
                    role: 'QA Engineer',
                    bio: 'Conducts extensive testing to ensure product quality and designs critical test cases for automated deployment pipelines'
                }
            },
            timeline: {
                title: 'Our Journey',
                year1: {
                    title: 'Foundation',
                    desc: 'AiInPocket established, focusing on AI and cloud technology consulting'
                },
                year2: {
                    title: 'AI Assistant Era',
                    desc: 'Leveraged GPT-3 to build localized AI assistants for enterprises'
                },
                year3: {
                    title: 'AI for Everyone',
                    desc: 'Launched LINE chatbot to help the public easily embrace AI'
                },
                year4: {
                    title: 'Managed Services',
                    desc: 'Providing SRE managed services for SMEs, managing 50+ cloud applications'
                },
                year5: {
                    title: 'Deep Integration',
                    desc: 'Helping enterprises integrate payment systems and government automated filing'
                }
            },
            whyUs: {
                title: 'Why Choose AiInPocket?',
                reason1: {
                    title: 'Practical Experience',
                    desc: '50+ project experience across industries, from finance to manufacturing'
                },
                reason2: {
                    title: 'Technical Depth',
                    desc: 'Team members with strong technical backgrounds, continuously tracking latest tech trends'
                },
                reason3: {
                    title: 'Fast Delivery',
                    desc: 'Agile development process, averaging only 2-4 weeks from requirements to launch'
                },
                reason4: {
                    title: 'Long-term Support',
                    desc: 'Providing 7x24 technical support, ensuring stable system operation'
                }
            },
            cta: {
                title: 'Ready to Create the Future with Us?',
                desc: 'Let\'s start a conversation and explore infinite possibilities',
                btn: 'Contact Us'
            }
        },

        contact: {
            header: {
                title: 'Contact Us',
                subtitle: 'Let\'s Start a Conversation'
            },
            info: {
                email: {
                    title: 'Email',
                    note: 'Reply within 24 hours'
                },
                chat: {
                    title: 'Live Chat',
                    value: 'AI Assistant',
                    note: 'Click chat button at bottom right'
                },
                social: {
                    title: 'Social Media',
                    note: 'Follow our latest updates'
                },
                hours: {
                    title: 'Service Hours',
                    value: '24/7',
                    note: 'Round-the-clock support'
                }
            },
            form: {
                title: 'Quick Inquiry',
                name: 'Name *',
                namePlaceholder: 'Your name',
                email: 'Email *',
                emailPlaceholder: 'your@email.com',
                company: 'Company',
                companyPlaceholder: 'Your company (optional)',
                service: 'Service Interest *',
                serviceOption0: 'Please select...',
                serviceOption1: 'AI Solutions',
                serviceOption2: 'Cloud Architecture',
                serviceOption3: 'DevOps Engineering',
                serviceOption4: 'Technical Consulting',
                serviceOption5: 'Other',
                message: 'Message *',
                messagePlaceholder: 'Describe your needs or ideas...',
                submit: 'Send Message',
                note: 'We\'ll respond within 24 hours',
                successTitle: 'Message Sent!',
                successMessage: 'Thank you for contacting us. We\'ll get back to you soon.'
            },
            faq: {
                title: 'FAQ',
                q1: {
                    question: 'How long does a project typically take?',
                    answer: 'Depends on complexity. Typical AI or cloud projects take 2-8 weeks. We\'ll provide detailed timeline after initial assessment.'
                },
                q2: {
                    question: 'How do you charge?',
                    answer: 'We offer flexible pricing: project-based, hourly, or long-term technical consulting contracts. We\'ll recommend the best option for your needs.'
                },
                q3: {
                    question: 'What technical support do you provide?',
                    answer: 'We provide 24/7 support including monitoring, emergency fixes, regular maintenance, and technical consulting.'
                },
                q4: {
                    question: 'Can you customize solutions?',
                    answer: 'Absolutely! We specialize in tailored solutions, understanding your business needs deeply to design the optimal technical architecture.'
                },
                q5: {
                    question: 'Do you provide training?',
                    answer: 'Yes, we provide comprehensive documentation and training upon project delivery to ensure your team can maintain operations smoothly.'
                },
                q6: {
                    question: 'How to get started?',
                    answer: 'Simply fill out the form above or email us. We\'ll arrange a free initial consultation to understand your needs and provide recommendations.'
                }
            },
            process: {
                title: 'Collaboration Process',
                step1: {
                    title: 'Requirements',
                    desc: 'Understand your needs and goals'
                },
                step2: {
                    title: 'Planning',
                    desc: 'Design architecture and implementation plan'
                },
                step3: {
                    title: 'Development',
                    desc: 'Agile development with regular deliveries'
                },
                step4: {
                    title: 'Deployment',
                    desc: 'Ensure stable operation and support'
                }
            }
        },

        privacy: {
            header: {
                title: 'Privacy Policy',
                subtitle: 'Last Updated: October 6, 2025'
            },
            section1: {
                title: '1. Information Collection',
                intro: 'We collect the following types of information:',
                item1: '<strong>Personal Information:</strong> When you contact us through the contact form, we collect your name, email address, and message content.',
                item2: '<strong>Usage Information:</strong> We use Google Analytics to collect website usage statistics, including browser type, visit time, and page view history.',
                item3: '<strong>Cookies:</strong> We use cookies to improve user experience and website functionality.'
            },
            section2: {
                title: '2. Google AdSense Advertising',
                intro: 'This website uses Google AdSense to display advertisements. Google and its partners may:',
                item1: 'Use cookies to show ads based on your previous visits to this or other websites',
                item2: 'Use advertising cookies to allow Google and its partners to serve ads based on users\' visits to this website and/or other websites',
                item3: 'You can opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Ad Settings</a>'
            },
            section3: {
                title: '3. Cookie Usage Statement',
                intro: 'This website uses the following types of cookies:',
                item1: '<strong>Essential Cookies:</strong> Used for basic website functions (such as language selection)',
                item2: '<strong>Analytics Cookies:</strong> Google Analytics for website traffic analysis',
                item3: '<strong>Advertising Cookies:</strong> Google AdSense for displaying relevant ads',
                note: 'You can manage or delete cookies through your browser settings. Note that disabling cookies may affect website functionality.'
            },
            section4: {
                title: '4. Information Usage',
                intro: 'We use collected information to:',
                item1: 'Respond to your inquiries and provide services',
                item2: 'Improve website content and user experience',
                item3: 'Send product updates and marketing information (only with your consent)',
                item4: 'Analyze website usage trends'
            },
            section5: {
                title: '5. Third-Party Services',
                intro: 'This website uses the following third-party services:',
                item1: '<strong>Google Analytics:</strong> <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Privacy Policy</a>',
                item2: '<strong>Google AdSense:</strong> <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Advertising Policies</a>'
            },
            section6: {
                title: '6. Data Security',
                intro: 'We take reasonable technical and organizational measures to protect your personal information, including:',
                item1: 'Using HTTPS encrypted transmission',
                item2: 'Restricting data access permissions',
                item3: 'Regular security reviews'
            },
            section7: {
                title: '7. Your Rights',
                intro: 'Under GDPR and related regulations, you have the right to:',
                item1: 'Access your personal data',
                item2: 'Correct inaccurate data',
                item3: 'Request data deletion',
                item4: 'Object to processing of your data',
                item5: 'Data portability',
                contact: 'To exercise these rights, please contact: <a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>'
            },
            section8: {
                title: '8. Children\'s Privacy',
                text: 'This website is not intended for children under 13. We do not knowingly collect personal information from children.'
            },
            section9: {
                title: '9. Policy Changes',
                text: 'We may update this privacy policy from time to time. We will post notices on the website for significant changes.'
            },
            section10: {
                title: '10. Contact Us',
                intro: 'If you have any questions about this privacy policy, please contact:',
                item1: '<strong>Email:</strong> <a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>',
                item2: '<strong>General Contact:</strong> <a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>'
            }
        },

        footer: {
            tagline: 'Intelligence at Your Fingertips',
            services: 'Services',
            contactUs: 'Contact',
            privacy: 'Privacy Policy',
            email: 'Email',
            copyright: 'AiInPocket. All rights reserved.',
            poweredBy: '/// Powered by AI & Innovation ///'
        },

        easterEgg: {
            title: '[Easter Egg Triggered!]',
            text: 'You discovered the hidden magic spell!',
            magic: 'AI is in your pocket now!',
            btnClose: 'Close'
        },

        landing: {
            title: 'AI Website Generator',
            subtitle: 'Choose your destination: Visit the corporate website or start generating AI-powered websites.',
            startGenerator: 'Start Generator',
            corporateWebsite: 'Corporate Website'
        },

        cookie: {
            title: '🍪 Cookie Notice',
            description: 'This website uses cookies to improve user experience and display ads via Google AdSense. By continuing to browse, you agree to our use of cookies.',
            learnMore: 'Learn more',
            accept: 'Accept All Cookies',
            reject: 'Essential Only'
        }
    },

    // 日本語
    'ja': {
        nav: {
            home: 'ホーム',
            portfolio: 'ポートフォリオ',
            techStack: '技術スタック',
            about: '私たちについて',
            contact: 'お問い合わせ',
            generator: 'AI ジェネレーター'
        },

        home: {
            hero: {
                title1: '未来のテクノロジーを',
                title2: 'あなたのポケットに',
                subtitle: 'AI × クラウド × DevOps 自動化',
                desc1: 'AiInPocketは最先端のAI技術とクラウドソリューションを',
                desc2: '最もシンプルな方法でお届けします。',
                startBtn: '始める',
                portfolioBtn: '事例を見る'
            },
            services: {
                title: 'コアサービス',
                ai: {
                    title: 'AIソリューション',
                    desc: 'ディープラーニング、自然言語処理、コンピュータビジョン、インテリジェント自動化。カスタムAIモデルを構築し、ビジネスを強化します。',
                    feature1: 'カスタムAIモデルトレーニング',
                    feature2: 'LLMアプリケーション統合',
                    feature3: 'インテリジェントデータ分析',
                    feature4: '自動意思決定システム'
                },
                cloud: {
                    title: 'クラウドアーキテクチャ',
                    desc: 'スケーラブルで高可用性、コスト最適化されたクラウドソリューション。ゼロから構築または既存インフラの最適化。',
                    feature1: 'クラウドネイティブアーキテクチャ設計',
                    feature2: 'コンテナ化とオーケストレーション',
                    feature3: 'サーバーレスアーキテクチャ',
                    feature4: 'マルチクラウド戦略'
                },
                devops: {
                    title: 'DevOpsエンジニアリング',
                    desc: 'CI/CDパイプライン、Infrastructure as Code、監視とアラート。開発を加速し、安定性を向上させます。',
                    feature1: '自動デプロイパイプライン',
                    feature2: 'Infrastructure as Code (IaC)',
                    feature3: '監視とログシステム',
                    feature4: 'セキュリティスキャン'
                }
            },
            stats: {
                satisfaction: '顧客満足度',
                projects: 'プロジェクト納品',
                support: '24時間サポート',
                years: 'サービス年数',
                yearsUnit: '年以上'
            },
            cta: {
                title: 'AIの旅を始める準備はできましたか？',
                desc: '無限の可能性を探求し、あなたのインテリジェントソリューションを構築しましょう',
                btn: 'お問い合わせ'
            },
            easterEgg: {
                title: '[イースターエッグ発動！]',
                text: '隠された魔法の呪文を発見しました！',
                close: '閉じる'
            }
        },

        portfolio: {
            header: {
                title: 'ポートフォリオ',
                subtitle: '誇りを持ってご紹介するプロジェクト'
            },
            filters: {
                all: 'すべて',
                ai: 'AIソリューション',
                cloud: 'クラウドアーキテクチャ',
                devops: 'DevOps'
            },
            project1: {
                tag: 'AIソリューション',
                title: 'AIカスタマーサービス',
                desc: '大手ECプラットフォーム向けのAIカスタマーサービスシステム。GPT-4とカスタム知識ベースを組み合わせ、満足度を大幅に向上させながらコストを60%削減。',
                stat1: '<strong>60%</strong> コスト削減',
                stat2: '<strong>95%</strong> 精度',
                stat3: '<strong>24/7</strong> サービス'
            },
            project2: {
                tag: 'クラウドアーキテクチャ',
                title: 'マイクロサービス移行',
                desc: 'フィンテック企業のモノリスからKubernetesマイクロサービスアーキテクチャへの移行を支援。高可用性と弾力的なスケーリングを実現。',
                stat1: '<strong>99.9%</strong> 可用性',
                stat2: '<strong>3倍</strong> パフォーマンス',
                stat3: '<strong>50%</strong> コスト最適化'
            },
            project3: {
                tag: 'DevOps',
                title: 'CI/CD自動化',
                desc: 'コードコミットから本番環境デプロイまでの完全な自動化パイプラインを構築。リリースサイクルを1日複数回のデプロイに短縮。',
                stat1: '<strong>10倍</strong> デプロイ頻度',
                stat2: '<strong>80%</strong> 時間節約',
                stat3: '<strong>0</strong> ダウンタイム'
            },
            project4: {
                tag: 'クラウドアーキテクチャ',
                title: 'グローバルCDN展開',
                desc: '国際メディアプラットフォーム向けのグローバルコンテンツ配信ネットワークを設計。世界中のユーザーのアクセス速度とエクスペリエンスを最適化。',
                stat1: '<strong>70%</strong> レイテンシ削減',
                stat2: '<strong>150+</strong> ノード',
                stat3: '<strong>5大陸</strong> カバレッジ'
            },
            project5: {
                tag: 'DevOps',
                title: 'セキュリティ自動化',
                desc: 'セキュリティスキャンツールをCI/CDパイプラインに統合。脆弱性検出とコンプライアンスチェックを自動化。',
                stat1: '<strong>100%</strong> コードスキャン',
                stat2: '<strong>90%</strong> 脆弱性削減',
                stat3: '<strong>自動</strong> 修正提案'
            },
            opensource: {
                title: 'オープンソースプロジェクト',
                project1: {
                    title: 'AI 台湾株式機関投資家分析（日次）',
                    desc: '台湾株式市場の機関投資家動向を毎日自動分析し、ビジュアルレポートとトレンドインサイトを提供。'
                },
                project2: {
                    title: 'スマートワークフローオーケストレーションエンジン',
                    badge: '開発中',
                    desc: 'インテリジェントなワークフローオーケストレーションエンジン。複雑な自動化プロセスをシンプルで直感的に。'
                }
            },
            cta: {
                title: 'あなたのプロジェクトをここに掲載しませんか？',
                desc: '次の成功事例を一緒に作りましょう',
                btn: '始める'
            }
        },

        techStack: {
            header: {
                title: '技術スタック',
                subtitle: '最先端の技術ツール'
            },
            ai: {
                title: 'AI & 機械学習',
                python: 'AI統合と自動化',
                openai: 'GPT-4 API統合',
                ollama: 'ローカルLLMデプロイ',
                linebot: 'チャットボット開発',
                langchain: 'LLMアプリケーションフレームワーク',
                pytorch: '研究と本番環境',
                huggingface: '事前学習済みモデル'
            },
            cloud: {
                title: 'クラウド & インフラ',
                openshift: 'エンタープライズコンテナプラットフォーム',
                gcp: 'クラウドサービス',
                k8s: 'コンテナオーケストレーション',
                docker: 'コンテナ化',
                ansible: '構成自動化',
                serverless: 'サーバーレスアーキテクチャ'
            },
            devops: {
                title: 'DevOps & CI/CD'
            },
            languages: {
                title: 'プログラミング言語'
            },
            systems: {
                title: 'システム運用'
            },
            tools: {
                title: 'ツール & プラットフォーム'
            },
            web: {
                title: 'Web & バックエンド'
            },
            philosophy: {
                title: '私たちの技術哲学',
                principle1: {
                    title: '適合性優先',
                    desc: '最も流行している技術ではなく、問題に最適なツールを選択'
                },
                principle2: {
                    title: '継続的な学習',
                    desc: '技術トレンドを先取りし、定期的にスタックを評価・更新'
                },
                principle3: {
                    title: 'パフォーマンス重視',
                    desc: '最適なパフォーマンスを追求し、あらゆる側面を最適化'
                },
                principle4: {
                    title: 'セキュリティ第一',
                    desc: '事後対応ではなく、設計段階からセキュリティを考慮'
                }
            },
            cta: {
                title: 'これらの技術をどのように活用しているか知りたいですか？',
                desc: '事例をご覧いただくか、直接お話ししましょう',
                portfolioBtn: 'ポートフォリオを見る',
                contactBtn: 'お問い合わせ'
            }
        },

        about: {
            header: {
                title: '私たちについて',
                subtitle: 'インテリジェンスを身近にする私たちの使命'
            },
            mission: {
                title: '私たちのビジョン',
                text1: 'この急速に進化するAI時代において、テクノロジーは<strong>身近なもの</strong>であるべきだと私たちは信じています。AiInPocketは、最先端のAI技術、クラウドアーキテクチャ、DevOpsソリューションを、最も合理的で効率的な方法ですべてのクライアントに提供することに専念しています。',
                text2: 'ポケットのように — <strong>いつでも利用可能、どこでもアクセス可能、自由自在</strong>。'
            },
            values: {
                value1: {
                    title: '顧客重視',
                    desc: 'クライアントのニーズを深く理解し、カスタマイズされたソリューションを提供'
                },
                value2: {
                    title: '卓越性の追求',
                    desc: '技術を継続的に洗練し、最適なパフォーマンスと品質を追求'
                },
                value3: {
                    title: '誠実な協力',
                    desc: '透明なコミュニケーションと長期的なパートナーシップを基盤に'
                },
                value4: {
                    title: '継続的なイノベーション',
                    desc: '変化を受け入れ、新しい技術と可能性を積極的に探求'
                }
            },
            team: {
                title: 'コアチーム',
                member1: {
                    name: '最高技術責任者',
                    role: 'Chief Technology Officer',
                    bio: 'ソフトウェア開発とDevOpsの10年以上の経験、クラウドアーキテクチャ設計と自動化に特化'
                },
                member2: {
                    name: 'AI応用責任者',
                    role: 'Head of AI Applications',
                    bio: 'AI応用統合に注力、様々なAIツールと技術を組み合わせてクライアントのニーズを満たす方法を設計'
                },
                member3: {
                    name: 'フルスタックエンジニア',
                    role: 'Full-Stack Engineer',
                    bio: 'フロントエンドとバックエンド開発に精通、スムーズなユーザーエクスペリエンスと高性能システムの構築に専念'
                },
                member4: {
                    name: '品質保証エンジニア',
                    role: 'QA Engineer',
                    bio: '大量のテストを実施して製品品質を確保し、自動デプロイパイプラインの重要なテストケースを設計'
                }
            },
            timeline: {
                title: '私たちの歩み',
                year1: {
                    title: '創業',
                    desc: 'AiInPocket設立、AIとクラウド技術コンサルティングに注力'
                },
                year2: {
                    title: 'AIアシスタント元年',
                    desc: 'GPT-3を活用し、企業向けローカルAIアシスタントを構築'
                },
                year3: {
                    title: 'AIの普及',
                    desc: 'LINE自動応答ボットをリリース、一般の方がAIを身近に'
                },
                year4: {
                    title: 'マネージドサービス',
                    desc: '中小企業向けSRE代行サービス、50以上のクラウドアプリを管理'
                },
                year5: {
                    title: '深い統合',
                    desc: '企業の決済システム連携と政府機関への自動申告サービスを支援'
                }
            },
            whyUs: {
                title: 'なぜAiInPocketを選ぶのか？',
                reason1: {
                    title: '実践経験',
                    desc: '金融から製造業まで、業界を超えた50以上のプロジェクト経験'
                },
                reason2: {
                    title: '技術の深さ',
                    desc: '強固な技術的背景を持つチームメンバー、最新の技術トレンドを継続的に追跡'
                },
                reason3: {
                    title: '迅速な納品',
                    desc: 'アジャイル開発プロセス、要件からローンチまで平均2〜4週間'
                },
                reason4: {
                    title: '長期サポート',
                    desc: '7x24技術サポートを提供、安定したシステム運用を確保'
                }
            },
            cta: {
                title: '私たちと一緒に未来を創る準備はできていますか？',
                desc: '会話を始め、無限の可能性を探求しましょう',
                btn: 'お問い合わせ'
            }
        },

        contact: {
            header: {
                title: 'お問い合わせ',
                subtitle: '会話を始めましょう'
            },
            info: {
                email: {
                    title: 'メール',
                    note: '24時間以内に返信'
                },
                chat: {
                    title: 'ライブチャット',
                    value: 'AIアシスタント',
                    note: '右下のチャットボタンをクリック'
                },
                social: {
                    title: 'ソーシャルメディア',
                    note: '最新情報をフォロー'
                },
                hours: {
                    title: 'サービス時間',
                    value: '24時間365日',
                    note: '年中無休サポート'
                }
            },
            form: {
                title: 'クイックお問い合わせ',
                name: 'お名前 *',
                namePlaceholder: 'お名前',
                email: 'メール *',
                emailPlaceholder: 'your@email.com',
                company: '会社名',
                companyPlaceholder: '会社名（任意）',
                service: '興味のあるサービス *',
                serviceOption0: '選択してください...',
                serviceOption1: 'AIソリューション',
                serviceOption2: 'クラウドアーキテクチャ',
                serviceOption3: 'DevOpsエンジニアリング',
                serviceOption4: '技術コンサルティング',
                serviceOption5: 'その他',
                message: 'メッセージ *',
                messagePlaceholder: 'ご要望やアイデアをお聞かせください...',
                submit: 'メッセージを送信',
                note: '24時間以内に返信いたします',
                successTitle: 'メッセージが送信されました！',
                successMessage: 'お問い合わせいただきありがとうございます。すぐに返信いたします。'
            },
            faq: {
                title: 'よくある質問',
                q1: {
                    question: 'プロジェクトは通常どのくらいかかりますか？',
                    answer: '複雑さによります。一般的なAIまたはクラウドプロジェクトは2〜8週間かかります。初期評価後に詳細なタイムラインを提供します。'
                },
                q2: {
                    question: '料金はどうなっていますか？',
                    answer: '柔軟な価格設定を提供しています：プロジェクトベース、時間制、または長期技術コンサルティング契約。お客様のニーズに最適なオプションを提案します。'
                },
                q3: {
                    question: 'どのような技術サポートを提供していますか？',
                    answer: '監視、緊急修正、定期メンテナンス、技術コンサルティングを含む24時間365日のサポートを提供します。'
                },
                q4: {
                    question: 'カスタマイズソリューションは可能ですか？',
                    answer: 'もちろんです！カスタマイズソリューションを専門としており、ビジネスニーズを深く理解して最適な技術アーキテクチャを設計します。'
                },
                q5: {
                    question: 'トレーニングは提供されますか？',
                    answer: 'はい、プロジェクト納品時に包括的なドキュメントとトレーニングを提供し、チームがスムーズに運用を引き継げるようにします。'
                },
                q6: {
                    question: 'どのように始めればよいですか？',
                    answer: '上記のフォームに記入するか、直接メールでご連絡ください。無料の初回相談を手配し、ニーズを理解して推奨事項を提供します。'
                }
            },
            process: {
                title: '協力プロセス',
                step1: {
                    title: '要件確認',
                    desc: 'ニーズと目標を理解'
                },
                step2: {
                    title: '計画立案',
                    desc: 'アーキテクチャと実装計画を設計'
                },
                step3: {
                    title: '開発実装',
                    desc: 'アジャイル開発で定期的に成果を納品'
                },
                step4: {
                    title: 'デプロイ稼働',
                    desc: '安定した運用を確保しサポートを提供'
                }
            }
        },

        privacy: {
            header: {
                title: 'プライバシーポリシー',
                subtitle: '最終更新：2025年10月6日'
            },
            section1: {
                title: '1. 情報収集',
                intro: '以下の種類の情報を収集します：',
                item1: '<strong>個人情報：</strong>お問い合わせフォームからご連絡いただく際に、お名前、メールアドレス、メッセージ内容を収集します。',
                item2: '<strong>使用情報：</strong>Google Analyticsを使用してウェブサイトの使用統計情報（ブラウザタイプ、訪問時間、ページ閲覧履歴など）を収集します。',
                item3: '<strong>Cookie：</strong>ユーザーエクスペリエンスとウェブサイト機能を改善するためにCookieを使用します。'
            },
            section2: {
                title: '2. Google AdSense広告',
                intro: '本ウェブサイトはGoogle AdSenseを使用して広告を表示します。Googleとそのパートナーは以下を行う可能性があります：',
                item1: '本ウェブサイトまたは他のウェブサイトへの過去の訪問に基づいて広告を表示するためにCookieを使用',
                item2: 'ユーザーが本ウェブサイトおよび/またはインターネット上の他のウェブサイトにアクセスした状況に基づいて広告を配信するために広告Cookieを使用',
                item3: 'パーソナライズド広告をオプトアウトするには、<a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">広告設定</a>にアクセスしてください'
            },
            section3: {
                title: '3. Cookie使用声明',
                intro: '本ウェブサイトは以下の種類のCookieを使用します：',
                item1: '<strong>必須Cookie：</strong>ウェブサイトの基本機能（言語選択など）に使用',
                item2: '<strong>分析Cookie：</strong>Google Analyticsでウェブサイトトラフィック分析に使用',
                item3: '<strong>広告Cookie：</strong>Google AdSenseで関連広告を表示するために使用',
                note: 'ブラウザ設定からCookieを管理または削除できます。Cookieを無効にするとウェブサイト機能に影響する可能性があります。'
            },
            section4: {
                title: '4. 情報の使用',
                intro: '収集した情報を以下の目的で使用します：',
                item1: 'お問い合わせへの回答とサービスの提供',
                item2: 'ウェブサイトコンテンツとユーザーエクスペリエンスの改善',
                item3: '製品更新とマーケティング情報の送信（同意を得た場合のみ）',
                item4: 'ウェブサイト使用傾向の分析'
            },
            section5: {
                title: '5. 第三者サービス',
                intro: '本ウェブサイトは以下の第三者サービスを使用します：',
                item1: '<strong>Google Analytics：</strong><a href="https://policies.google.com/privacy" target="_blank" rel="noopener">プライバシーポリシー</a>',
                item2: '<strong>Google AdSense：</strong><a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">広告ポリシー</a>'
            },
            section6: {
                title: '6. データセキュリティ',
                intro: '個人情報を保護するために合理的な技術的および組織的措置を講じています：',
                item1: 'HTTPS暗号化転送の使用',
                item2: 'データアクセス権限の制限',
                item3: '定期的なセキュリティレビュー'
            },
            section7: {
                title: '7. あなたの権利',
                intro: 'GDPRおよび関連規制に基づき、以下の権利があります：',
                item1: '個人データへのアクセス',
                item2: '不正確なデータの訂正',
                item3: 'データの削除要求',
                item4: 'データ処理への異議申し立て',
                item5: 'データポータビリティ',
                contact: 'これらの権利を行使するには、<a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>までご連絡ください'
            },
            section8: {
                title: '8. 子供のプライバシー',
                text: '本ウェブサイトは13歳未満の子供を対象としていません。子供の個人情報を故意に収集することはありません。'
            },
            section9: {
                title: '9. ポリシーの変更',
                text: 'このプライバシーポリシーを随時更新する場合があります。重大な変更がある場合は、ウェブサイトに通知を掲載します。'
            },
            section10: {
                title: '10. お問い合わせ',
                intro: 'このプライバシーポリシーに関してご質問がある場合は、以下までご連絡ください：',
                item1: '<strong>メール：</strong><a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>',
                item2: '<strong>一般お問い合わせ：</strong><a href="mailto:help@aiinpocket.com">help@aiinpocket.com</a>'
            }
        },

        footer: {
            tagline: '知能を手の届くところに',
            services: 'サービス',
            contactUs: 'お問い合わせ',
            privacy: 'プライバシーポリシー',
            email: 'メール',
            copyright: 'AiInPocket. All rights reserved.',
            poweredBy: '/// Powered by AI & Innovation ///'
        },

        easterEgg: {
            title: '[イースターエッグ発動！]',
            text: '隠された魔法の呪文を発見しました！',
            magic: 'AI is in your pocket now!',
            btnClose: '閉じる'
        },

        landing: {
            title: 'AI ウェブサイトジェネレーター',
            subtitle: '目的地を選択してください：コーポレートサイトにアクセスするか、AI駆動のウェブサイト生成を開始します。',
            startGenerator: 'ジェネレーターを開始',
            corporateWebsite: 'コーポレートサイト'
        },

        cookie: {
            title: '🍪 Cookie 使用について',
            description: '本ウェブサイトは、ユーザーエクスペリエンスを向上させ、Google AdSenseを通じて広告を表示するためにCookieを使用しています。閲覧を続けることで、Cookieの使用に同意したものとみなされます。',
            learnMore: '詳細を見る',
            accept: 'すべてのCookieを受け入れる',
            reject: '必要なCookieのみ'
        }
    }
};

// 當前語言（預設繁體中文）
let currentLanguage = localStorage.getItem('language') || 'zh-TW';

/**
 * 取得翻譯文字
 */
function t(key) {
    const keys = key.split('.');
    let value = translations[currentLanguage];

    for (const k of keys) {
        value = value?.[k];
    }

    return value || key;
}

/**
 * 切換語言
 */
function setLanguage(lang) {
    if (!translations[lang]) {
        console.error(`Language ${lang} not supported`);
        return;
    }

    currentLanguage = lang;
    localStorage.setItem('language', lang);
    updatePageContent();

    // 觸發語言變更事件
    document.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

/**
 * 取得當前語言
 */
function getCurrentLanguage() {
    return currentLanguage;
}

/**
 * 更新頁面內容
 */
function updatePageContent() {
    // 更新所有帶有 data-i18n 屬性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);

        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            element.placeholder = translation;
        } else if (element.tagName === 'SELECT') {
            // SELECT 元素不更新，由 OPTION 自己更新
            return;
        } else {
            // 使用 innerHTML 以保留 HTML 標籤（如 <strong>, <br> 等）
            element.innerHTML = translation;
        }
    });

    // 更新 data-text 屬性（用於 glitch 效果）
    document.querySelectorAll('[data-i18n-attr="data-text"]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);
        element.setAttribute('data-text', translation);
    });

    // 更新頁面語言屬性
    document.documentElement.lang = currentLanguage;
}

// 頁面載入時初始化
document.addEventListener('DOMContentLoaded', () => {
    updatePageContent();
});
