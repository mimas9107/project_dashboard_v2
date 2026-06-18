---
name:          "CHANGELOG.md"
description:   "專案變更日誌，記錄所有版本的改進與修復。"
created_date:  "2026/02/14 00:00:00"
modified_date: "2026/06/18 18:00:00"
project_version: "2.2.3"
document_version: "1.0.1"
agent_sign: ['human/name', 'gemini cli/current_agent']
---
# 變更日誌

所有重要的專案變更都會記錄在這個檔案中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

## [2.2.3] - 2026-06-18

### 🐛 錯誤修復
- **前端 `url_for` 不存在於 FastAPI Jinja2 環境**: `templates/index.html` 中的 `{{ url_for(...) }}` 改為直接路徑
- **Symlink 專案誤判為不安全路徑**: `core/project_manager.py` 的 `validate_project_path` 改用 unresolved path 做路徑檢查，允許掃描目錄內的 symbolic link
- **單一專案掃描錯誤導致整支 API 掛掉**: `app.py` 的 `/api/projects` 加入 `try/except` 跳過問題專案，避免回傳非陣列格式使前端 `.filter()` 報錯

### 🔧 技術改進
- `pyproject.toml` 依賴優化（保留 FastAPI 為主，移除不相關依賴）

---

## [2.2.2] - 2026-04-07

### ✨ 新功能
- **專案詳情分欄 Modal**: 點擊專案卡片後，彈窗改為左右分欄布局
  - 左半部：顯示完整 README.md 內容（使用 marked.js 渲染 Markdown）
  - 右半部：保持原有檔案結構樹
  - 兩側各自獨立滾動，方便同時瀏覽說明與檔案結構
- **新增 API**: `GET /api/readme/{name}` 回傳專案完整 README.md 內容
- **本地化 marked.js**: 下載 Markdown 渲染引擎至 `static/js/marked.min.js`，支援離線使用

### 🔧 技術改進
- `project_manager.py` 新增 `get_readme_content()` 方法
- Modal 從 `modal-lg` 升級為 `modal-xl modal-dialog-scrollable`
- 使用順序載入（先 README 再結構）確保穩定性
- 新增 URL 編碼處理與錯誤處理，避免特殊字元問題
- 新增完整 Markdown 深色主題樣式（標題、程式碼、表格、引用等）
- **Modal 尺寸優化**: 高度改為 `90vh`，貼近瀏覽器檢視畫面，兩側內容各自獨立滾動

---

## [2.2.1] - 2026-04-07

### 🔧 離線支援
- **CDN 本地化**: 將所有外部 CDN 資源下載至 `static/` 目錄，支援離線環境使用
  - Bootstrap 5.3.0 CSS → `static/css/bootstrap.min.css`
  - Bootstrap 5.3.0 JS → `static/js/bootstrap.bundle.min.js`
  - Bootstrap Icons 1.10.0 CSS → `static/css/bootstrap-icons.css`
  - Bootstrap Icons 字型 → `static/fonts/bootstrap-icons.woff2`, `bootstrap-icons.woff`
- **路徑修正**: Bootstrap Icons CSS 字型路徑從 `./fonts/` 改為 `../fonts/`
- **模板更新**: `templates/index.html` 和 `setup.py` 中的 CDN 引用全部替換為本地路徑

---

## [2.2.0] - 2026-03-05

### ✨ UI/UX 改善
- **深色模式優化**: 彈窗 (Modal) 改為層次感更強的暗色調，提升在深色背景下的對比度。
- **統計資訊可讀性**: 
  - 為 Markdown、C++、C#、Vue 等 10+ 種語言新增配色。
  - 增加語言標籤的預設背景色，防止未知語言出現「白底白字」。
  - 統計數值與單位文字（如 `x 39 個專案`）改為純白並加粗，確保在暗色背景下清晰可見。
- **標題強化**: 頁面副標題從黯淡的灰色調亮，提升視覺辨識度。
- **互動效果**: 統計卡片新增懸停 (Hover) 位移效果與更清晰的邊框。

### 🔧 技術改進
- 在 CSS 中實作了背景層次階梯：頁面 (`#121212`) -> 彈窗 (`#1e1e1e`) -> 卡片 (`#2a2a2a`)。
- 解決了 JS 快取可能導致的標籤樣式回退問題。

---

## [2.1.0] - 2026-02-14

### ✨ 新功能
- 將 Flask 改為 FastAPI 作為 Web 框架
- 使用 `uvicorn` 作為 ASGI 伺服器
- 更新 API 端點使用 FastAPI 的強大功能

### 🔄 改善
- API 驗證改用 FastAPI 的 `Body()` 和 `Query()` 參數
- 使用 `JSONResponse` 替代 Flask 的 `jsonify()`
- 使用 `HTTPException` 替代 Flask 的 `abort()` 和自定義錯誤處理
- 靜態檔案路徑改為直接使用 `/static/` 路徑（不再依賴 `url_for`）
- `requirements.txt` 更新為 FastAPI 生態系統套件

### 📦 依賴更新
**新增依賴:**
- `fastapi==0.115.0`
- `uvicorn==0.32.0`
- `jinja2==3.1.4`
- `python-multipart==0.0.12`

**移除依賴:**
- `Flask==3.0.0`

**保留依賴:**
- `fastmcp==0.1.0` (無變更)

### 📝 文件
- 新增 `README.md` 記錄 FastAPI 版本說明
- 新增 `CHANGELOG.md` 及其首個版本記錄
- 更新專案文件以反映 FastAPI 版本變更

### 🔧 技術重點
- **統一核心邏輯**: `core/project_manager.py` 和 `core/database.py` 無需修改
- **MCP Server 保留**: `mcp_server.py` 繼續使用 FastMCP
- **前端模板** `templates/index.html`: 使用 `/static/` 路徑而非 `url_for()`
- **啟動指令**: 使用 `uvicorn.run()` 替代 Flask 的 `app.run()`

---

## [2.0.0] - 2026-01-06

### ✨ 新功能
- 統一核心邏輯層 (`core/project_manager.py`)
- SQLite 資料庫整合
- 20+ 個增強 MCP 工具
- 標籤系統
- 收藏備註功能
- 智能建議系統
- 快取機制
- 完整的 API 文檔

---

## [1.0.0] - 2025-12-27

### ✨ 新功能
- 基礎 Flask Web 介面
- 簡單的 MCP Server
- JSON 檔案儲存
