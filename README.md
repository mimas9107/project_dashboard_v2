# Project Dashboard MCP Server v2

一個輕量級的 MCP (Model Context Protocol) Server，專為 LLM 使用而設計，用於管理和監控本地專案。

## 📋 功能特色

這個 MCP Server 提供兩個核心工具：

### 1. `get_focused_projects()`
返回在 `dashboard_state.yaml` 中明確標記為「favorite」的專案。

**包含資訊：**
- **宣告式元數據 (Declared Metadata)**: `favorite` 狀態（由使用者設定）
- **衍生式元數據 (Derived Metadata)**: Git 資訊（即時計算）
  - `has_git`: 是否為 Git 倉庫
  - `dirty`: 是否有未提交的變更
  - `last_commit_days`: 距離上次提交的天數

### 2. `scan_project(path, options=None)`
對專案資料夾執行按需遞迴掃描。

**參數：**
- `path` (必填): 專案資料夾路徑
- `options` (選填):
  - `depth`: 掃描深度（預設: 2）
  - `include_extensions`: 要包含的副檔名列表（例如: `[".html", ".js"]`）

**返回資訊：**
- `files`: 檔案列表
- `folders`: 資料夾列表
- `extensions_present`: 發現的副檔名
- `file_count` / `folder_count`: 檔案/資料夾數量
- `git_info`: Git 資訊（同上）

## 🏗️ 專案結構

```
project_dashboard_v2/
├── projects/                    # 存放所有專案的目錄
│   ├── my_web_app/
│   ├── data_analysis_project/
│   └── automation_scripts/
├── dashboard_state.yaml         # 宣告式元數據（使用者偏好設定）
├── mcp_server.py               # MCP Server 主程式
├── requirements.txt            # Python 依賴套件
└── README.md                   # 本檔案
```

## 🚀 安裝與使用

### 步驟 1: 安裝依賴套件

```bash
cd project_dashboard_v2
pip install -r requirements.txt
```

### 步驟 2: 設定專案清單

編輯 `dashboard_state.yaml` 檔案，添加你想要追蹤的專案：

```yaml
favorites:
  - "my_web_app"
  - "data_analysis_project"
  - "automation_scripts"
```

### 步驟 3: 建立專案資料夾

在 `projects/` 目錄下建立對應的專案資料夾，或者在 YAML 中使用絕對路徑。

### 步驟 4: 啟動 MCP Server

```bash
python3 mcp_server.py
```

或者使其可執行：

```bash
chmod +x mcp_server.py
./mcp_server.py
```

### 步驟 5: 在 Claude Desktop 中配置

在 Claude Desktop 的設定檔中添加這個 MCP Server：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/absolute/path/to/project_dashboard_v2/mcp_server.py"
      ]
    }
  }
}
```

重啟 Claude Desktop 後，你就可以使用這些工具了！

### 🐧 在 Linux 使用 Claude Code CLI？

如果你在 Linux 環境下使用 **Claude Code CLI**，配置檔案位置不同：

**配置檔案位置**: `~/.config/claude-code/mcp.json`

```bash
# 建立配置目錄
mkdir -p ~/.config/claude-code

# 編輯配置檔案
nano ~/.config/claude-code/mcp.json
```

**配置內容**（格式相同，但路徑不同）：
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/absolute/path/to/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

重啟 Claude Code CLI：
```bash
# 退出後重新執行
claude
```

**📖 詳細的 Claude Code CLI 設定指南**: 請參考 [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md) 獲取完整的配置說明、疑難排解和進階設定。

## 📝 使用範例

### 獲取重點專案

```
請使用 get_focused_projects 工具顯示我的重點專案。
```

**LLM 會收到：**
```json
{
  "focused_projects": [
    {
      "name": "my_web_app",
      "path": "/path/to/projects/my_web_app",
      "favorite": true,
      "git_info": {
        "has_git": true,
        "dirty": false,
        "last_commit_days": 3
      }
    }
  ],
  "total_count": 1
}
```

### 掃描專案

```
請掃描 /path/to/my_project 資料夾，深度設為 3，只包含 Python 和 JavaScript 檔案。
```

**LLM 會使用：**
```json
{
  "path": "/path/to/my_project",
  "options": {
    "depth": 3,
    "include_extensions": [".py", ".js"]
  }
}
```

## 🎯 設計原則

### 宣告式 vs 衍生式元數據

這個專案嚴格區分兩種類型的元數據：

1. **宣告式元數據 (Declared Metadata)**
   - 由使用者在 `dashboard_state.yaml` 中明確設定
   - 持久化儲存
   - 例如：`favorite` 狀態、專案標籤

2. **衍生式元數據 (Derived Metadata)**
   - 按需即時計算
   - 不持久化儲存
   - 例如：Git 狀態、檔案統計

**重要**: MCP Server **不決定**優先級或緊急度，它只提供事實資訊。LLM 會使用這些輸出進行推理和決策。

## 🔧 進階配置

### 支援絕對路徑

在 `dashboard_state.yaml` 中，你可以使用絕對路徑：

```yaml
favorites:
  - "/Users/username/Documents/important_project"
  - "relative_project_in_projects_folder"
```

### Git 資訊超時

Git 命令有 5 秒的超時限制，避免在大型倉庫上阻塞。

### 忽略模式

掃描時會自動忽略：
- 隱藏檔案（以 `.` 開頭）
- `node_modules`
- `__pycache__`
- `venv` / `.venv`

## 🛠️ 開發與擴展

### 添加新工具

在 `mcp_server.py` 中：

1. 在 `list_tools()` 中註冊新工具
2. 在 `call_tool()` 中添加處理邏輯
3. 實作對應的處理函數

### 添加新的宣告式元數據

在 `dashboard_state.yaml` 中添加新欄位：

```yaml
favorites:
  - "my_project"

project_tags:
  my_project:
    - web
    - flask
    
project_priority:
  my_project: high
```

然後在 `mcp_server.py` 中讀取並返回這些資料。

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📚 相關資源

- [Model Context Protocol 文件](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [原始 Project Dashboard](https://github.com/mimas9107/project_dashboard)
