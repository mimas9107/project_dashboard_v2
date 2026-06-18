---
name:          "MEMOIR.md"
description:   "專案回憶錄，記錄重要決策、架構演進與開發心得。"
created_date:  "2026/06/18 10:00:00"
modified_date: "2026/06/18 18:00:00"
project_version: "2.2.3"
document_version: "1.0.1"
agent_sign: ['human/name', 'gemini cli/current_agent']
---
# 專案回憶錄 (MEMOIR.md)

## 1. 核心決策
- **從 Flask 遷移至 FastAPI (2026-02-14)**:
    - 決策原因：FastAPI 提供原生異步支援與更強大的類型檢查，適合與 MCP Server 整合。
    - 結果：提升了 API 回應速度，簡化了程式碼結構。
- **引入 SQLite 資料庫**:
    - 決策原因：原本的 JSON 檔案儲存在專案數量增多時效能下降。
    - 結果：支援了標籤、備註與快取功能，大幅提升查詢效率。

## 2. 前端演進
- **離線支援 (v2.2.1)**:
    - 將 Bootstrap 等 CDN 資源本地化，確保在無網路環境下（如封閉式開發環境）依然能正常工作。
- **專案詳情分欄 (v2.2.2)**:
    - 為了讓使用者能同時查看 README 與檔案結構，改採左右分欄佈局。

## 3. 已知模式與慣例
- **Single Source of Truth**: `CHANGELOG.md` 作為版本號的唯一基準。
- **技術優先級**: 優先使用 Vanilla CSS 與 Vanilla JS，減少對重型框架的依賴，保持輕量。

## 4. 未來展望
- 支援多工作區切換。
- 增加更多的 Git 批次操作工具。
- 整合更深入的程式碼靜態分析工具。
