# Project Dashboard v2.2

> 統一核心邏輯 + SQLite 資料庫 + FastAPI Web Server + MCP Server 的本地專案管理系統

## 🎯 v2 新功能亮點

### 0. **離線支援** (v2.2.1)
- ✅ 所有前端依賴（Bootstrap、Bootstrap Icons）已本地化
- ✅ 無需外部網路連線即可正常顯示樣式
- ✅ 字型檔案內建於 `static/fonts/` 目錄

### 0.1. **專案詳情分欄** (v2.2.2)
- ✅ 點擊專案卡片彈出左右分欄 Modal
- ✅ 左側顯示完整 README.md（Markdown 渲染）
- ✅ 右側顯示檔案結構樹
- ✅ 兩側獨立滾動瀏覽（高度 90vh，貼近瀏覽器檢視畫面）

### 1. **統一核心邏輯層**
- ✅ 所有專案管理邏輯集中在 `core/project_manager.py`
- ✅ FastAPI 和 MCP Server 共用相同程式碼，避免雙重維護
- ✅ 更容易進行單元測試和功能擴展

### 2. **SQLite 資料庫**
- ✅ 持久化收藏、標籤、快取資料
- ✅ 支援收藏排序和備註功能
- ✅ 自動快取掃描結果，提升載入速度
- ✅ 完整的資料匯出/匯入功能

### 3. **增強的 MCP 工具集**
全新 AI 工具共 **20+ 個**，包括：

#### 基礎管理
- `list_projects()` - 列出所有專案
- `get_project_info(name)` - 獲取詳細資訊
- `get_project_files(name, depth)` - 查看目錄結構

#### 智能搜尋
- `search_projects_by_language(language)` - 按語言搜尋（如 "Python"）
- `search_projects_by_tag(tag)` - 按標籤搜尋
- `get_all_tags()` - 查看所有可用標籤

#### Git 管理
- `get_modified_projects()` - 找出有變更的專案
- `batch_git_status()` - 批次檢查所有專案狀態

#### 專案診斷
- `find_projects_without_readme()` - 找出缺少 README 的資料夾
- `analyze_workspace_summary()` - 工作區完整統計分析

#### 收藏與標籤
- `toggle_project_favorite(name)` - 切換收藏
- `add_project_tag(name, tag)` - 新增標籤
- `remove_project_tag(name, tag)` - 移除標籤
- `update_favorite_notes(name, notes)` - 更新收藏備註

#### 編輯器整合
- `open_in_vscode(name)` - VS Code 開啟
- `open_in_editor(name, editor)` - 支援多種編輯器

#### 智能建議
- `suggest_next_actions()` - AI 主動建議下一步操作

---

## 📦 專案結構

```
project_dashboard_v2/
├── core/                          # 核心邏輯層
│   ├── __init__.py
│   ├── project_manager.py         # 專案管理核心類別
│   └── database.py                # SQLite 資料庫管理
├── static/
│   ├── css/
│   │   ├── bootstrap.min.css      # Bootstrap 5.3.0 (本地)
│   │   ├── bootstrap-icons.css    # Bootstrap Icons 1.10.0 (本地)
│   │   └── style.css              # 深色主題樣式
│   ├── js/
│   │   ├── bootstrap.bundle.min.js # Bootstrap 5.3.0 JS (本地)
│   │   ├── marked.min.js          # Markdown 渲染引擎 (本地)
│   │   └── script.js              # 前端互動邏輯
│   └── fonts/
│       ├── bootstrap-icons.woff2  # Bootstrap Icons 字型
│       └── bootstrap-icons.woff   # Bootstrap Icons 字型 (相容)
├── templates/
│   └── index.html                 # 網頁模板
├── tests/                         # 單元測試目錄
├── app.py                         # FastAPI Web 應用
├── mcp_server.py                  # MCP Server（供 AI 使用）
├── requirements.txt               # Python 依賴
├── .env                           # 環境配置
├── start_web.sh                   # Linux/macOS 啟動腳本（Web）
├── start_mcp.sh                   # Linux/macOS 啟動腳本（MCP）
├── README.md                      # FastAPI 版本文件
├── README_v2.md                   # 原始 v2 文件
├── CHANGELOG.md                   # 版本變更記錄
└── .gitignore                     # Git 忽略設定
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 配置環境

編輯 `.env` 檔案：

```ini
SCAN_DIR="../"                      # 專案掃描路徑
HOST="127.0.0.1"
PORT=5001
DB_PATH="project_dashboard.db"      # 資料庫檔案位置
```

### 3. 啟動 Web 介面（FastAPI）

```bash
python app.py
```

然後開啟瀏覽器訪問：`http://127.0.0.1:5001`

### 4. 啟動 MCP Server（供 AI 使用）

```bash
# 直接執行
python mcp_server.py

# 或使用腳本
./start_mcp.sh
```

---

## 🔧 Claude Desktop 整合

編輯 Claude Desktop 設定檔：

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "project-dashboard-v2": {
      "command": "python",
      "args": [
        "/path/to/project_dashboard_v2/mcp_server.py"
      ]
    }
  }
}
```

---

## 💡 使用範例

### 在 Claude Desktop 中使用

```
你: 幫我列出所有 Python 專案
Claude: [調用 search_projects_by_language("Python")]
      找到 5 個 Python 專案：
      1. project_dashboard_v2 (Python 85%)
      2. data_analysis_tool (Python 70%)
      ...

你: 哪些專案有未提交的變更？
Claude: [調用 get_modified_projects()]
      有 2 個專案需要注意：
      - web_scraper: 3 個檔案已修改
      - api_service: 1 個檔案已修改

你: 給我一些建議
Claude: [調用 suggest_next_actions()]
      ⚠️ 有 2 個專案有未提交的變更
      📝 有 3 個資料夾缺少 README.md
      ✅ 建議為常用專案加上標籤分類
```

### 在 Web 介面中使用

- **查看專案**：自動顯示所有專案卡片
- **收藏管理**：點擊星號圖示加入/移除收藏
- **目錄瀏覽**：點擊卡片查看檔案結構
- **快速開啟**：點擊 "VS Code" 按鈕直接開啟編輯器
- **標籤分類**：為專案新增自訂標籤

---

## 📊 API 端點列表

### 專案管理
- `GET /api/projects` - 獲取所有專案
- `GET /api/project/<name>` - 獲取單一專案詳情
- `GET /api/structure/<name>` - 獲取目錄結構

### 收藏管理
- `POST /api/favorite` - 切換收藏狀態
- `GET /api/favorites` - 獲取所有收藏

### 標籤管理
- `GET /api/tags/<name>` - 獲取專案標籤
- `POST /api/tags/<name>` - 新增標籤
- `DELETE /api/tags/<name>` - 刪除標籤
- `GET /api/tags` - 獲取所有標籤

### 搜尋功能
- `GET /api/search/language/<language>` - 按語言搜尋
- `GET /api/search/tag/<tag>` - 按標籤搜尋

### Git 工具
- `GET /api/git/modified` - 獲取有變更的專案
- `GET /api/git/status` - 批次 Git 狀態

### 診斷工具
- `GET /api/diagnostics/no-readme` - 缺少 README 的資料夾
- `GET /api/statistics` - 完整統計資訊

### 編輯器整合
- `GET /api/open/<name>?editor=code` - 開啟編輯器

### 快取管理
- `POST /api/cache/clear` - 清除過舊快取

---

## 🗄️ 資料庫結構

### 主要資料表

**favorites** - 收藏專案
```sql
name TEXT PRIMARY KEY,
added_at TIMESTAMP,
order_index INTEGER,
notes TEXT
```

**project_cache** - 專案快取
```sql
name TEXT PRIMARY KEY,
description TEXT,
languages JSON,
git_status TEXT,
git_detail TEXT,
has_git BOOLEAN,
last_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

**project_tags** - 專案標籤
```sql
project_name TEXT,
tag TEXT,
created_at TIMESTAMP
```

**scan_history** - 掃描歷史
```sql
scan_time TIMESTAMP,
projects_found INTEGER,
scan_duration_ms INTEGER
```

---

## 🔒 安全性特性

1. **路徑驗證**：防止目錄遍历攻擊
2. **參數驗證**：檢查所有 API 輸入
3. **錯誤處理**：完善的異常捕獲機制
4. **權限控制**：僅掃描指定目錄

---

## 🧪 測試

```bash
# 執行單元測試
python -m pytest tests/

# 測試核心功能
python -c "from core.project_manager import ProjectManager; pm = ProjectManager('./'); print(pm.list_all_projects())"

# 測試資料庫
python -c "from core.database import DatabaseManager; db = DatabaseManager(); print(db.get_statistics())"
```

---

## 📈 效能優化

- **快取機制**：掃描結果自動快取 7 天
- **深度限制**：目錄樹預設限制 2 層
- **忽略目錄**：自動跳過 node_modules、.git 等
- **批次操作**：減少重複掃描

---

## 🛠️ 開發指南

### 新增自訂語言支援

編輯 `core/project_manager.py`：

```python
LANGUAGE_MAP = {
    '.py': 'Python',
    '.your_ext': 'YourLanguage',  # 新增這行
    ...
}
```

### 新增 MCP 工具

在 `mcp_server.py` 中：

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    """工具說明"""
    # 實作邏輯
    return result
```

### 新增 API 端點

在 `app.py` 中：

```python
@app.get("/api/your-endpoint")
async def your_endpoint():
    # 實作邏輯
    return JSONResponse(content=result)
```

---

## 🎁 從 v1 遷移

如果您有舊版的 `favorites.json`：

```python
# 匯入舊收藏到資料庫
import json
from core.database import DatabaseManager

db = DatabaseManager()
with open('favorites.json') as f:
    old_favs = json.load(f)
    for name in old_favs:
        db.add_favorite(name)
```

---

## 🐛 故障排除

### 資料庫鎖定錯誤
```bash
# 關閉所有使用資料庫的程式
# 或刪除 project_dashboard.db.lock 檔案
```

### Git 指令逾時
```python
# 在 .env 增加
GIT_TIMEOUT=10  # 秒數
```

### 編輯器開啟失敗
```bash
# 確認編輯器在 PATH 中
where code     # Windows
which code     # Linux/Mac
```

### 靜態檔案載入失敗
```bash
# 確認 static 目錄存在且包含 css/ 和 js/ 子目錄
# 檢查 templates/index.html 中的靜態路徑是否正確
```

---

## 📝 更新日誌

### v2.1.0 (2026-02-14) - FastAPI 版本
- ✨ 從 Flask 重構為 FastAPI
- ✨ 使用 `app.mount()` 替代 Flask 的 `static_folder`
- ✨ API 端點改用 FastAPI 的 `JSONResponse` 和 `HTTPException`
- ✨ 使用 `uvicorn` 作為 ASGI 伺服器
- ✨ 更新 `requirements.txt` 為 FastAPI 相關套件
- 📝 更新 API 驗證為 FastAPI 的 `Body()` 和 `Query()`

### v2.0.0 (2026-01-06)
- ✨ 統一核心邏輯層
- ✨ SQLite 資料庫整合
- ✨ 20+ 個增強 MCP 工具
- ✨ 標籤系統
- ✨ 收藏備註功能
- ✨ 智能建議系統
- ✨ 快取機制
- ✨ 完整的 API 文檔

### v1.0.0 (2025-12-27)
- 基礎 Flask Web 介面
- 簡單的 MCP Server
- JSON 檔案儲存

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

## 📄 授權

MIT License

---

## 👥 維護者

- Claude AI + Human Developer
- 最後更新：2026-02-14

---

## 🔗 相關資源

- [FastMCP 文檔](https://github.com/jlowin/fastmcp)
- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Enjoy managing your projects! 🚀**
