# 變更日誌

所有重要的專案變更都會記錄在這個檔案中。

格式基於 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/)。

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
