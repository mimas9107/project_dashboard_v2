---
name:          "SPEC.md"
description:   "專案技術規格書，定義系統架構、技術棧與 API 規範。"
created_date:  "2026/06/18 10:00:00"
modified_date: "2026/06/18 18:00:00"
project_version: "2.2.3"
document_version: "1.0.1"
agent_sign: ['human/name', 'gemini cli/current_agent']
---
# 技術規格書 (SPEC.md)

## 1. 系統概述
Project Dashboard v2 是一個本地專案管理系統，整合了核心邏輯層、SQLite 資料庫、FastAPI Web 伺服器與 MCP (Model Context Protocol) 伺服器。

## 2. 技術棧
- **後端框架**: FastAPI (Python)
- **資料庫**: SQLite
- **AI 整合**: MCP (Model Context Protocol) 透過 `fastmcp` 實作
- **前端**: HTML5, Vanilla CSS (Bootstrap 5.3.0), JavaScript (Vanilla)
- **環境管理**: `uv` (建議使用)
- **程式碼品質**: `ruff`

## 3. 系統架構
專案採用分層架構：
- **核心邏輯層 (`core/`)**: 處理專案掃描、Git 狀態檢查與資料庫交互。
- **Web 介面層 (`app.py`)**: 提供 RESTful API 與靜態網頁服務。
- **AI 工具層 (`mcp_server.py`)**: 暴露專案管理工具給 AI Agent 使用。

## 4. 資料庫架構
主要資料表：
- `favorites`: 收藏專案清單。
- `project_cache`: 專案詳細資訊快取。
- `project_tags`: 專案自定義標籤。
- `scan_history`: 歷史掃描記錄。

## 5. API 規範
詳見 `README.md` 中的 API 端點列表。

## 6. 安全性規範
- 路徑驗證：防止 Directory Traversal。
- 輸入過濾：所有 API 參數均經過驗證。
