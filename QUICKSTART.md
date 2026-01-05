# Quick Start Guide - Project Dashboard MCP Server v2

快速上手指南，5 分鐘內啟動並運行！

## 🚀 30 秒快速安裝

```bash
# 1. 進入專案目錄
cd project_dashboard_v2

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 建立測試專案
mkdir -p projects/test_project
cd projects/test_project
git init
echo "# Test Project" > README.md
git add . && git commit -m "Initial commit"
cd ../..

# 4. 測試運行
python3 test_mcp_server.py
```

## 📝 基本使用

### 1. 設定你的專案

編輯 `dashboard_state.yaml`:

```yaml
favorites:
  - "test_project"
  - "my_important_app"
```

### 2. 在 Claude Desktop 中配置

**macOS**: 編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: 編輯 `%APPDATA%\Claude\claude_desktop_config.json`

**Linux**: 編輯 `~/.config/Claude/claude_desktop_config.json`

加入以下配置（記得修改路徑）:

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/完整/路徑/到/project_dashboard_v2/mcp_server.py"
      ]
    }
  }
}
```

### 3. 重啟 Claude Desktop

配置完成後重啟 Claude Desktop，你應該會看到新的工具可用！

## 💬 實際使用範例

### 範例 1: 查看重點專案

```
你: 幫我看看我的重點專案狀態如何？

Claude: [使用 get_focused_projects 工具]
你有 3 個重點專案：

1. **test_project** 
   - 路徑: /path/to/projects/test_project
   - Git 狀態: ✅ 乾淨
   - 最後提交: 2 天前

2. **my_important_app**
   - 路徑: /path/to/projects/my_important_app  
   - Git 狀態: ⚠️ 有未提交的變更
   - 最後提交: 5 天前

3. **automation_scripts**
   - 路徑: /path/to/projects/automation_scripts
   - Git 狀態: ✅ 乾淨
   - 最後提交: 1 天前
```

### 範例 2: 分析專案結構

```
你: 幫我分析一下 test_project 的結構

Claude: [使用 scan_project 工具]
專案 test_project 的結構分析：

📁 專案資訊:
- 檔案總數: 23 個
- 資料夾總數: 5 個

📄 檔案類型:
- .py: 15 個（Python 程式碼）
- .md: 3 個（文件）
- .yaml: 2 個（配置檔案）
- .txt: 3 個（文字檔案）

🔧 Git 狀態:
- 倉庫: 是
- 未提交變更: 否
- 最後提交: 2 天前

這看起來是一個結構良好的 Python 專案！
```

### 範例 3: 深度掃描特定檔案類型

```
你: 我想看看這個專案裡有哪些 Python 和 JavaScript 檔案

Claude: [使用 scan_project 工具，設定 include_extensions: [".py", ".js"]]
找到的檔案：

Python 檔案 (15):
- main.py
- config.py
- utils.py
...

JavaScript 檔案 (8):
- app.js
- router.js
- components/Header.js
...
```

## 🎯 常見使用場景

### 場景 1: 每日站會前快速檢查

```
「幫我看看哪些專案有未提交的變更，我需要在站會前整理一下」
```

### 場景 2: 專案健康度檢查

```
「哪些專案超過一週沒有更新了？我可能需要重新關注它們」
```

### 場景 3: 技術棧分析

```
「掃描我的專案，告訴我主要使用了哪些技術棧」
```

### 場景 4: 程式碼審查準備

```
「幫我看看 my_app 專案裡有多少 Python 檔案，我需要準備 code review」
```

## 🔧 進階技巧

### 技巧 1: 使用絕對路徑

如果專案不在 `projects/` 目錄下：

```yaml
favorites:
  - "/Users/justin/Documents/important_project"
  - "local_project_in_projects_folder"
```

### 技巧 2: 控制掃描深度

```
「請只掃描專案的根目錄，不要進入子目錄（depth=1）」
```

### 技巧 3: 過濾特定檔案類型

```
「只顯示專案中的 HTML、CSS 和 JavaScript 檔案」
```

## ⚠️ 常見問題

### Q1: 工具沒有出現在 Claude Desktop 中？

**解決方案:**
1. 檢查配置檔案路徑是否正確
2. 確認使用的是**絕對路徑**
3. 重啟 Claude Desktop
4. 檢查 Python 是否正確安裝

### Q2: 如何在 Linux 下使用 Claude Code CLI？

**答案:** Claude Code CLI 使用不同的配置檔案！

**快速設定步驟:**

1. 找到配置檔案位置：
```bash
~/.config/claude-code/mcp.json
# 或
~/.claude-code/mcp.json
```

2. 建立/編輯配置檔案：
```bash
mkdir -p ~/.config/claude-code
nano ~/.config/claude-code/mcp.json
```

3. 加入以下配置（記得修改路徑）：
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/完整/路徑/到/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

4. 重啟 Claude Code：
```bash
# 退出後重新啟動
claude
```

5. 測試工具：
```
顯示我的所有重點專案
```

**詳細說明**: 請參考 [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) 獲取完整的配置指南、疑難排解和進階設定。

**重要提醒:**
- Claude Desktop 和 Claude Code CLI 使用**不同的配置檔案**
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- Claude Code CLI: `~/.config/claude-code/mcp.json` (Linux)

### Q3: Git 資訊顯示不正確？

**解決方案:**
1. 確認專案目錄包含 `.git` 資料夾
2. 確保 git 命令在 PATH 中可用
3. 檢查是否有權限訪問 Git 倉庫

### Q4: 掃描速度很慢？

**解決方案:**
1. 減少掃描深度（使用 `depth=1` 或 `depth=2`）
2. 使用 `include_extensions` 過濾
3. 確認沒有掃描到 `node_modules` 等大型目錄

### Q5: 路徑找不到？

**解決方案:**
1. 使用絕對路徑
2. 確認路徑存在且為目錄
3. 檢查拼寫和大小寫（特別是 Linux/macOS）

### Q6: Claude Code CLI 中工具無法啟動？

**解決方案:**
1. 檢查 Python 路徑：
```bash
which python3
```

2. 測試 MCP Server：
```bash
python3 /path/to/mcp_server.py
```

3. 檢查依賴：
```bash
pip install mcp pyyaml
```

4. 驗證 JSON 格式：
```bash
cat ~/.config/claude-code/mcp.json | python3 -m json.tool
```

詳細疑難排解請參考 [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md)

## 📊 效能參考

| 專案規模 | 檔案數量 | 建議深度 | 預期時間 |
|---------|---------|---------|---------|
| 小型    | < 100   | 3-5     | < 1秒   |
| 中型    | 100-1K  | 2-3     | 1-3秒   |
| 大型    | 1K-10K  | 1-2     | 3-10秒  |
| 超大型  | > 10K   | 1       | 10-30秒 |

## 🎓 學習路徑

1. ✅ **基礎**: 安裝並運行測試
2. ✅ **初級**: 配置自己的專案並使用基本工具
3. ⬜ **中級**: 自訂掃描參數和過濾器
4. ⬜ **高級**: 閱讀 DEVELOPMENT.md 並擴展新功能

## 🔗 相關資源

- [完整 README](README.md) - 詳細功能說明
- [開發者文件](DEVELOPMENT.md) - 架構和 API 設計
- [測試腳本](test_mcp_server.py) - 功能測試

## 🎉 下一步

現在你已經準備好了！試試這些命令：

```
「顯示我的所有重點專案」
「掃描 [專案名稱] 並告訴我它的結構」
「哪些專案需要我的注意？」
```

享受使用 Project Dashboard MCP Server v2！ 🚀
