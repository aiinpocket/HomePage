#!/usr/bin/env python3
"""移除專案中所有 emoji 的腳本"""
import re
import os
from pathlib import Path

# emoji 替換對照表
EMOJI_REPLACEMENTS = {
    # 通用 emoji
    '🚀': '',
    '🎉': '',
    '💬': '',
    '📊': '',
    '🔒': '',
    '🌐': '',
    '📧': '',
    '💎': '',
    '✨': '',
    '🎯': '',
    '🤖': 'AI助手',
    '👤': '用戶',
    '✅': '[成功]',
    '❌': '[失敗]',
    '📁': '',
    '💻': '',
    '👥': '',
    '⏰': '',
    '🧠': 'AI',
    '☁️': 'Cloud',
    '⚡': 'DevOps',
    '🔐': '',
    '📈': '',
    '📝': '',
    '🛡️': '',
    '🔧': '',
    '🦊': '',
    '⚙️': '',
    '🔴': '',
    '🍃': '',
    '🔄': '',
    '🐍': '',
    '🔥': '',
    '🔍': '',
    '🎨': '',
    '⎈': '',
    '🐳': '',
    '🏗️': '',
    '🟢': '',
    '⚛️': '',
    '🗄️': '',
    '🔵': '',
    '👨‍💻': '',
    '👋': '',
    '🎮': '',
}

def remove_emojis_from_file(file_path):
    """從檔案中移除 emoji"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 替換所有 emoji
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)

        # 如果內容有變化，寫回檔案
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """主函數"""
    project_root = Path(__file__).parent
    modified_files = []

    # 要處理的檔案類型
    file_patterns = ['**/*.html', '**/*.js', '**/*.py', '**/*.md']

    # 排除的目錄
    exclude_dirs = {'.git', 'node_modules', '__pycache__', '.idea', 'dist'}

    for pattern in file_patterns:
        for file_path in project_root.glob(pattern):
            # 跳過排除的目錄
            if any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs):
                continue

            if remove_emojis_from_file(file_path):
                modified_files.append(file_path)
                print(f"Modified: {file_path.relative_to(project_root)}")

    print(f"\n處理完成！共修改 {len(modified_files)} 個檔案")

if __name__ == '__main__':
    main()
