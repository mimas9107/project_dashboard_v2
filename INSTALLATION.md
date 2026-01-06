# Project Dashboard v2 - 安裝指南

## 📦 檔案清單

本專案應包含以下檔案：

```
project_dashboard_v2/
├── core/
│   ├── __init__.py                 ✅ 已建立
│   ├── project_manager.py          ⚠️  需要從對話記錄複製
│   └── database.py                 ⚠️  需要從對話記錄複製
├── static/
│   ├── css/
│   │   └── style.css               ✅ 已建立
│   └── js/
│       └── script.js               ✅ 已建立
├── templates/
│   └── index.html                  ✅ 已建立
├── tests/
│   └── __init__.py                 ✅ 已建立
├── app.py                          ⚠️  需要從對話記錄複製
├── mcp_server.py                   ⚠️  需要從對話記錄複製
├── setup.py                        ✅ 已建立
├── requirements.txt                ⚠️  需要建立
├── .env                            ⚠️  需要建立
├── start_web.bat                   ✅ 已建立
├── start_mcp.bat                   ✅ 已建立
└── README_v2.md                    ✅ 已建立
```

## 🔧 缺少的核心檔案

以下三個核心 Python 檔案在對話中已經完整建立，但由於 Claude 的檔案系統限制，需要您手動複製：

### 1. `core/project_manager.py`
- **位置**: 在本對話中搜尋 "Project Dashboard v2 - Core Project Manager"
- **行數**: 約 400+ 行
- **功能**: 統一的專案管理核心邏輯
- **包含**: ProjectManager 類別及所有專案掃描、分析功能

### 2. `core/database.py`
- **位置**: 在本對話中搜尋 "Project Dashboard v2 - Database Manager"
- **行數**: 約 350+ 行
- **功能**: SQLite 資料庫管理
- **包含**: DatabaseManager 類別及所有資料庫操作

### 3. `app.py`
- **位置**: 在本對話中搜尋 "Project Dashboard v2 - Flask Web Application"
- **行數**: 約 300+ 行
- **功能**: Flask Web 伺服器
- **包含**: 所有 API 路由定義

### 4. `mcp_server.py`
- **位置**: 在本對話中搜尋 "Project Dashboard v2 - Enhanced MCP Server"
- **行數**: 約 450+ 行
- **功能**: MCP Server（供 AI 助理使用）
- **包含**: 20+ 個 MCP 工具定義

## 📝 需要手動建立的設定檔

### `requirements.txt`
```
Flask==3.0.0
fastmcp==0.1.0
```

### `.env`
```ini
SCAN_DIR="../"
HOST="127.0.0.1"
PORT=5001
DB_PATH="project_dashboard.db"
```

## 🚀 完成步驟

1. **複製核心檔案**
   - 從對話記錄中複製上述 4 個 Python 檔案的完整內容
   - 確保檔案編碼為 UTF-8

2. **建立設定檔**
   - 建立 `requirements.txt`
   - 建立 `.env` 並根據您的環境調整路徑

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **啟動測試**
   ```bash
   # Web 介面
   python app.py
   
   # MCP Server
   python mcp_server.py
   ```

5. **驗證功能**
   - 開啟 http://127.0.0.1:5001
   - 檢查是否能看到專案列表
   - 測試收藏、標籤等功能

## ⚡ 快速自動化方案

如果您想要自動化這個過程，可以：

1. **使用我準備的完整打包檔**（如果 Claude 成功複製到輸出目錄）
2. **或者讓 Claude 重新建立一次核心檔案**到正確位置
3. **或者使用 Git** 從遠端倉庫 clone（如果已上傳）

## 🐛 常見問題

### Q: 缺少 core/project_manager.py
**A**: 回到本對話，找到標題為 "建立統一的專案管理核心邏輯" 的檔案內容，完整複製到該位置

### Q: 缺少 core/database.py
**A**: 回到本對話，找到標題為 "建立 SQLite 資料庫管理模組" 的檔案內容，完整複製

### Q: 模組導入錯誤
**A**: 確保 core/__init__.py 存在且包含正確的匯出語句

### Q: 資料庫錯誤
**A**: 檢查 .env 中的 DB_PATH 設定，確保有寫入權限

## 📞 需要幫助？

如果您在設定過程中遇到問題：

1. 檢查本 README 的故障排除章節
2. 查看 README_v2.md 中的完整文檔
3. 回到對話記錄查找完整的檔案內容
4. 或者請 Claude 重新生成特定檔案

---

**重要提示**: 本專案的核心邏輯檔案（約 1500+ 行程式碼）已在對話中完整建立，只需要從對話記錄複製到正確位置即可。
