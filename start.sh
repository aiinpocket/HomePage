#!/bin/bash

# AiInPocket 快速啟動腳本

echo "================================"
echo "🚀 AiInPocket 啟動中..."
echo "================================"

# 檢查 .env 檔案
if [ ! -f "backend/.env" ]; then
    echo "⚠️  未找到 .env 檔案，正在創建..."
    cp backend/.env.example backend/.env
    echo "✅ 已創建 backend/.env，請編輯此檔案並設定你的 OPENAI_API_KEY"
    echo ""
    echo "你可以稍後編輯 backend/.env 來設定 API Key"
    echo ""
fi

# 建立並啟動 Docker 容器
echo "🐳 啟動 Docker 容器..."
docker-compose up --build -d

# 等待服務啟動
echo ""
echo "⏳ 等待服務啟動..."
sleep 5

# 檢查服務狀態
echo ""
echo "📊 檢查服務狀態..."
docker-compose ps

echo ""
echo "================================"
echo "✅ AiInPocket 已成功啟動！"
echo "================================"
echo ""
echo "🌐 前端網站: http://localhost:80"
echo "🔧 後端 API: http://localhost:8000"
echo "📚 API 文檔: http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "  - 如需停止: docker-compose down"
echo "  - 查看日誌: docker-compose logs -f"
echo "  - 記得在 backend/.env 設定你的 OPENAI_API_KEY"
echo ""
echo "🎉 享受 AiInPocket 吧！"
echo "================================"
