# 🐧 Claude Code CLI 支援更新摘要

## 更新日期
2026-01-05

## 更新內容

為 Project Dashboard MCP Server v2 添加了完整的 **Claude Code CLI** 支援文件。

## 新增文件

### 1. CLAUDE_CODE_SETUP.md ⭐ 主要文件
完整的 Claude Code CLI 設定指南，包含：

**內容:**
- ✅ 前置需求檢查
- ✅ 快速設定步驟（6 步驟）
- ✅ 完整配置範例（基本/虛擬環境/多 Server）
- ✅ 進階配置（Shell 腳本/環境變數）
- ✅ 6+ 常見問題詳細疑難排解
- ✅ 使用範例和最佳實踐
- ✅ 配置檢查清單

**行數:** ~380 行  
**適合:** Linux 使用者、Claude Code CLI 使用者

### 2. CONFIG_REFERENCE.md 📋 快速參考
配置快速參考卡片，包含：

**內容:**
- ✅ Claude Desktop vs Claude Code CLI 配置差異對照
- ✅ 快速檢查清單
- ✅ 常見路徑錯誤示範
- ✅ 快速驗證命令
- ✅ 疑難排解速查表

**行數:** ~120 行  
**適合:** 需要快速查找配置的使用者

## 更新的現有文件

### QUICKSTART.md
- ✅ 添加 Q2: 如何在 Linux 下使用 Claude Code CLI？
- ✅ 快速設定步驟
- ✅ 詳細文件連結
- ✅ 重要提醒（配置檔案位置不同）

### OVERVIEW.md
- ✅ 步驟 4 新增「選項 B: Claude Code CLI」
- ✅ 配置檔案位置說明
- ✅ 重啟指令說明

### README.md
- ✅ 步驟 5 新增「🐧 在 Linux 使用 Claude Code CLI？」章節
- ✅ 配置檔案位置和格式
- ✅ 重啟命令
- ✅ 詳細指南連結

### PROJECT_STRUCTURE.md
- ✅ 文件結構圖更新（添加 CLAUDE_CODE_SETUP.md）
- ✅ 文件說明新增 CLAUDE_CODE_SETUP.md 描述

### CHANGELOG.md
- ✅ v2.0.0 文件清單更新
- ✅ 新增 CLAUDE_CODE_SETUP.md
- ✅ 新增 CONFIG_REFERENCE.md

## 關鍵差異說明

### Claude Desktop vs Claude Code CLI

| 項目 | Claude Desktop | Claude Code CLI |
|-----|---------------|----------------|
| **配置檔案** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) | `~/.config/claude-code/mcp.json` (Linux) |
| **平台** | macOS, Windows, Linux | 主要是 Linux |
| **介面** | 圖形介面 | 命令列介面 |
| **重啟方式** | 重啟應用程式 | `exit` 後重新執行 `claude` |

## 配置範例

### Claude Code CLI 基本配置
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/home/justin/projects/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 配置檔案位置
```bash
# 方案 1（推薦）
~/.config/claude-code/mcp.json

# 方案 2
~/.claude-code/mcp.json
```

## 快速測試流程

```bash
# 1. 建立配置目錄
mkdir -p ~/.config/claude-code

# 2. 編輯配置
nano ~/.config/claude-code/mcp.json

# 3. 驗證 JSON 格式
cat ~/.config/claude-code/mcp.json | python3 -m json.tool

# 4. 測試 MCP Server
python3 /path/to/mcp_server.py

# 5. 啟動 Claude Code
claude

# 6. 測試工具
# 在 Claude Code 中輸入:
# "顯示我的所有重點專案"
```

## 疑難排解重點

### 最常見問題

1. **工具不顯示** → 檢查配置檔案位置和路徑
2. **ModuleNotFoundError** → 安裝依賴: `pip install mcp pyyaml`
3. **Permission denied** → `chmod +x mcp_server.py`
4. **JSON 格式錯誤** → 驗證格式: `python3 -m json.tool < config.json`

### 完整疑難排解
詳見 [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) 的「疑難排解」章節。

## 文件完整度更新

| 類別 | 檔案數 | 狀態 |
|-----|-------|------|
| 核心程式 | 1 | ✅ 完成 |
| 配置檔案 | 3 | ✅ 完成 |
| 測試腳本 | 2 | ✅ 完成 |
| 說明文件 | **10** | ✅ 完成（新增 2 份） |
| 範例專案 | 3 | ✅ 完成 |

## 推薦閱讀順序（Linux 使用者）

1. **總覽** → `OVERVIEW.md`
2. **快速參考** → `CONFIG_REFERENCE.md` 📋
3. **詳細設定** → `CLAUDE_CODE_SETUP.md` 🐧
4. **完整功能** → `README.md`
5. **架構理解** → `DEVELOPMENT.md`

## 使用建議

### 對於 Claude Desktop 使用者
- 參考原有文件即可
- 配置檔案位置不變
- 功能完全相同

### 對於 Claude Code CLI 使用者 🐧
- **必讀**: CLAUDE_CODE_SETUP.md
- **快速參考**: CONFIG_REFERENCE.md
- **注意**: 配置檔案位置不同
- **提示**: 使用絕對路徑

## 特別說明

### 為什麼需要獨立文件？

1. **配置位置不同**: 
   - Desktop: `~/Library/Application Support/Claude/`
   - CLI: `~/.config/claude-code/`

2. **使用方式不同**:
   - Desktop: 圖形介面操作
   - CLI: 命令列操作

3. **疑難排解不同**:
   - CLI 特有的問題（Python 路徑、虛擬環境等）
   - 需要命令列驗證方法

4. **文件完整性**:
   - 提供針對性的指導
   - 減少混淆
   - 提升使用體驗

## 測試狀態

### Claude Code CLI 配置測試
- ✅ 配置檔案格式驗證
- ✅ Python 路徑正確性
- ✅ 依賴套件安裝
- ✅ MCP Server 可執行性
- ⏳ 實際 Claude Code CLI 環境測試（待使用者驗證）

## 後續支援

如果遇到 Claude Code CLI 相關問題：

1. 查看 [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) 疑難排解章節
2. 查看 [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) 快速參考
3. 檢查 [QUICKSTART.md](QUICKSTART.md) 的 Q&A
4. 提交 Issue 到 GitHub

## 貢獻

歡迎回報 Claude Code CLI 使用經驗和改進建議！

---

**更新完成！** 現在 Project Dashboard MCP Server v2 完整支援：
- ✅ Claude Desktop（圖形介面）
- ✅ Claude Code CLI（命令列介面）🐧

享受使用！🚀
