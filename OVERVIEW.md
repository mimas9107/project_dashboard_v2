# Project Dashboard MCP Server v2 - 專案總覽

## 🎯 專案目標

這是一個完整實作的 **MCP (Model Context Protocol) Server**，專為 LLM 使用而設計，用於管理和監控本地專案。

## ✨ 核心功能

### 1. get_focused_projects() 
返回你標記為「favorite」的專案，包含：
- 專案名稱和路徑
- Git 狀態（是否有未提交變更）
- 最後提交時間（天數）

### 2. scan_project(path, options)
深度掃描專案目錄，返回：
- 檔案和資料夾列表
- 副檔名統計
- Git 資訊
- 可自訂掃描深度和過濾規則

## 🚀 5 分鐘快速開始

### 步驟 1: 解壓並進入專案
```bash
cd project_dashboard_v2
```

### 步驟 2: 安裝依賴
```bash
pip install -r requirements.txt
# 或使用 pip install mcp pyyaml
```

### 步驟 3: 測試運行
```bash
python3 test_standalone.py
```

你應該會看到測試通過，並自動建立 3 個範例專案！

### 步驟 4: 配置 Claude Desktop 或 Claude Code CLI

**選項 A: Claude Desktop（圖形介面）**

編輯配置檔案（根據你的作業系統）：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

加入以下內容（記得修改路徑）：
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/你的/完整/路徑/project_dashboard_v2/mcp_server.py"
      ]
    }
  }
}
```

**選項 B: Claude Code CLI（命令列介面）**

如果你使用的是 Linux 下的 Claude Code CLI：

1. 配置檔案位置不同：
```bash
~/.config/claude-code/mcp.json
# 或
~/.claude-code/mcp.json
```

2. 建立/編輯配置：
```bash
mkdir -p ~/.config/claude-code
nano ~/.config/claude-code/mcp.json
```

3. 加入配置（與 Claude Desktop 格式相同）：
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

**📖 詳細的 Claude Code CLI 設定請參考**: [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md)

### 步驟 5: 重啟應用程式

- **Claude Desktop**: 重啟應用程式
- **Claude Code CLI**: 退出後重新執行 `claude` 命令

配置完成後，工具就可以使用了！

## 📝 快速使用範例

在 Claude 中試試這些指令：

```
「顯示我的所有重點專案」
→ 使用 get_focused_projects 工具

「掃描 my_web_app 專案並告訴我它的結構」
→ 使用 scan_project 工具

「哪些專案有未提交的變更？」
→ 分析 Git 狀態資訊
```

## 📂 專案結構一覽

```
project_dashboard_v2/
├── mcp_server.py              # 主程式 ⭐
├── dashboard_state.yaml       # 配置檔 ⭐
├── requirements.txt           # 依賴清單
├── test_standalone.py         # 測試腳本 ✅
├── README.md                  # 完整說明
├── QUICKSTART.md              # 快速開始
├── CLAUDE_CODE_SETUP.md       # Claude Code CLI 設定 🐧
├── DEVELOPMENT.md             # 開發者文件
├── PROJECT_STRUCTURE.md       # 結構說明
├── CHANGELOG.md               # 版本記錄
├── LICENSE                    # 授權條款
└── projects/                  # 專案目錄
    ├── my_web_app/
    ├── data_analysis_project/
    └── automation_scripts/
```

## 📚 文件導覽

| 文件 | 適合對象 | 內容 |
|-----|---------|------|
| **README.md** | 所有人 | 功能介紹、安裝指南、使用範例 |
| **QUICKSTART.md** | 新手 | 5分鐘快速上手、常見問題 |
| **DEVELOPMENT.md** | 開發者 | 架構設計、API 文件、擴展指南 |
| **PROJECT_STRUCTURE.md** | 維護者 | 完整的專案結構說明 |

## 🎯 核心設計原則

### 元數據分類
- **宣告式元數據**: 使用者在 YAML 中設定（如 favorite 狀態）
- **衍生式元數據**: 即時從檔案系統計算（如 Git 狀態）

### 職責邊界
- **MCP Server**: 提供事實資訊
- **LLM (Claude)**: 解讀資訊、進行推理、給出建議
- **使用者**: 做出最終決策

## 🔧 自訂你的專案

### 1. 編輯專案清單
編輯 `dashboard_state.yaml`:
```yaml
favorites:
  - "your_project_1"
  - "/absolute/path/to/project_2"
```

### 2. 建立專案資料夾
```bash
mkdir -p projects/your_project_1
cd projects/your_project_1
git init
# 添加你的檔案...
```

### 3. 測試
```bash
python3 test_standalone.py
```

## ⚡ 效能參考

| 專案規模 | 檔案數 | 建議深度 | 預期時間 |
|---------|-------|---------|---------|
| 小型 | < 100 | 3-5 | < 1秒 |
| 中型 | 100-1K | 2-3 | 1-3秒 |
| 大型 | > 1K | 1-2 | 3-10秒 |

## ❓ 常見問題

### Q: 工具沒出現在 Claude Desktop？
A: 
1. 確認配置檔案路徑正確
2. 使用**絕對路徑**
3. 重啟 Claude Desktop
4. 檢查 Python 和依賴已安裝

### Q: Git 資訊不正確？
A:
1. 確認專案有 `.git` 資料夾
2. 檢查 git 命令可用
3. 確認有權限訪問

### Q: 掃描很慢？
A:
1. 減少深度（depth=1 或 2）
2. 使用副檔名過濾
3. 確認沒掃到大型目錄

## 🎓 學習路徑

1. ✅ **入門**: 執行 `test_standalone.py`，理解基本概念
2. ✅ **初級**: 配置自己的專案，在 Claude 中使用工具
3. ⬜ **中級**: 閱讀 DEVELOPMENT.md，理解架構
4. ⬜ **高級**: 擴展新功能、添加新工具

## 🌟 主要特色

✅ 完整的 MCP Protocol 實作  
✅ 兩個強大的專案管理工具  
✅ 清晰的元數據分類  
✅ 靈活的目錄掃描  
✅ Git 整合  
✅ 完善的錯誤處理  
✅ 詳盡的文件  
✅ 測試腳本  

## 📦 套件資訊

**版本**: v2.0.0  
**Python**: >= 3.8  
**依賴**: mcp>=1.1.0, pyyaml>=6.0.0  
**授權**: MIT  

## 🤝 貢獻

歡迎貢獻！請：
1. Fork 專案
2. 建立功能分支
3. 提交 Pull Request

## 📞 支援

- 查看文件: README.md, QUICKSTART.md
- 提交 Issue: GitHub Issues
- 參考原始專案: https://github.com/mimas9107/project_dashboard

## 🎉 開始使用

```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 測試運行
python3 test_standalone.py

# 3. 配置 Claude Desktop
# (編輯配置檔案)

# 4. 重啟 Claude Desktop

# 5. 開始使用！
```

---

**享受使用 Project Dashboard MCP Server v2！** 🚀

有任何問題，請查看 QUICKSTART.md 或 README.md 獲取更多資訊。
