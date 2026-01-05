# Project Dashboard MCP Server v2 - 開發者文件

## 架構設計

### 核心概念

#### 1. 元數據分類 (Metadata Classification)

專案嚴格區分兩種類型的元數據：

**宣告式元數據 (Declared Metadata)**
- 定義：由使用者在配置檔案中明確設定的資料
- 儲存：持久化在 `dashboard_state.yaml` 檔案中
- 特性：穩定、使用者可控
- 範例：
  - `favorite` 狀態
  - 專案標籤
  - 優先級設定

**衍生式元數據 (Derived Metadata)**
- 定義：從檔案系統或 Git 倉庫即時計算的資料
- 儲存：不持久化，每次請求時重新計算
- 特性：動態、反映當前狀態
- 範例：
  - Git 狀態（dirty, last_commit_days）
  - 檔案數量統計
  - 副檔名列表

#### 2. 責任邊界 (Responsibility Boundaries)

**MCP Server 的職責：**
- ✅ 提供事實資訊（declared + derived metadata）
- ✅ 執行檔案系統掃描
- ✅ 查詢 Git 狀態
- ❌ **不**決定專案優先級
- ❌ **不**進行智能推薦
- ❌ **不**修改 declared metadata（由 LLM 指示使用者修改）

**LLM 的職責：**
- 解讀 MCP Server 提供的資訊
- 根據上下文進行推理
- 為使用者提供建議
- 決定行動優先順序

### 技術架構

```
┌─────────────────────────────────────────────────────────┐
│                    LLM (Claude)                         │
│  - 接收工具輸出                                          │
│  - 進行推理和決策                                        │
│  - 生成建議給使用者                                      │
└────────────────────┬────────────────────────────────────┘
                     │ MCP Protocol
                     │ (JSON-RPC over stdio)
                     ↓
┌─────────────────────────────────────────────────────────┐
│              MCP Server (mcp_server.py)                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Tools Layer                                     │   │
│  │  - get_focused_projects()                       │   │
│  │  - scan_project(path, options)                  │   │
│  └────────────┬────────────────────────────────────┘   │
│               │                                         │
│  ┌────────────┴────────────────────────────────────┐   │
│  │ Logic Layer                                     │   │
│  │  - load_dashboard_state()                       │   │
│  │  - get_git_info()                               │   │
│  │  - scan_directory()                             │   │
│  │  - get_project_basic_info()                     │   │
│  └────────────┬────────────────────────────────────┘   │
│               │                                         │
│  ┌────────────┴────────────────────────────────────┐   │
│  │ Data Layer                                      │   │
│  │  - dashboard_state.yaml (declared metadata)     │   │
│  │  - File System (derived: file structure)       │   │
│  │  - Git Repository (derived: git status)        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 工具詳細說明

### 1. get_focused_projects()

**目的**: 返回使用者標記為「favorite」的專案列表

**輸入**: 無

**輸出結構**:
```json
{
  "focused_projects": [
    {
      "name": "project_name",
      "path": "/absolute/path/to/project",
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

**執行流程**:
1. 讀取 `dashboard_state.yaml`
2. 提取 `favorites` 列表
3. 對每個專案：
   - 解析路徑（支援相對/絕對路徑）
   - 獲取基本資訊
   - 計算 Git 資訊（衍生）
4. 組裝並返回 JSON 結果

**使用場景**:
- 使用者詢問「我的重點專案有哪些？」
- LLM 需要了解使用者關注的專案
- 提供專案狀態總覽

### 2. scan_project(path, options)

**目的**: 對指定專案進行深度掃描，返回詳細的檔案結構資訊

**輸入**:
```json
{
  "path": "/path/to/project",
  "options": {
    "depth": 3,
    "include_extensions": [".py", ".js", ".html"]
  }
}
```

**輸出結構**:
```json
{
  "path": "/path/to/project",
  "name": "project",
  "scan_options": {
    "depth": 3,
    "include_extensions": [".py", ".js", ".html"]
  },
  "files": ["/path/to/file1.py", "/path/to/file2.js"],
  "folders": ["/path/to/folder1", "/path/to/folder2"],
  "extensions_present": [".html", ".js", ".py"],
  "file_count": 42,
  "folder_count": 8,
  "git_info": {
    "has_git": true,
    "dirty": false,
    "last_commit_days": 1
  }
}
```

**參數說明**:
- `depth`: 掃描深度（預設: 2）
  - `1`: 只掃描根目錄
  - `2`: 掃描到子目錄
  - `3+`: 更深層掃描
- `include_extensions`: 副檔名過濾器
  - `null`: 包含所有檔案
  - `[".py"]`: 只包含 Python 檔案
  - `[".js", ".jsx", ".ts"]`: 包含多種副檔名

**執行流程**:
1. 驗證路徑是否存在
2. 遞迴掃描目錄：
   - 應用深度限制
   - 過濾副檔名（如果指定）
   - 跳過隱藏檔案和常見忽略目錄
3. 獲取 Git 資訊
4. 組裝統計資料
5. 返回完整結果

**自動忽略項目**:
- 以 `.` 開頭的檔案/目錄
- `node_modules`
- `__pycache__`
- `venv` / `.venv`

**使用場景**:
- 分析專案結構
- 統計程式碼規模
- 識別技術棧（根據副檔名）
- 檢查專案組織方式

## Git 資訊提取

### 實作細節

```python
def get_git_info(project_path: str) -> Dict[str, Any]:
    """
    獲取 Git 倉庫的輕量級資訊
    
    使用的 Git 命令:
    1. git status --porcelain  # 檢查未提交變更
    2. git log -1 --format=%ct  # 獲取最後提交時間戳
    """
```

### 返回欄位

- `has_git` (bool): `.git` 目錄是否存在
- `dirty` (bool): 是否有未提交的變更
- `last_commit_days` (int): 距離最後提交的天數
  - `-1`: 沒有提交記錄
  - `0`: 今天提交
  - `1+`: N 天前提交

### 錯誤處理

- **超時**: 5 秒超時限制，避免在大型倉庫上阻塞
- **異常**: 捕獲所有 Git 錯誤，返回安全預設值
- **權限**: 處理無權限訪問的情況

### 性能考量

- 使用 `--porcelain` 格式提高解析速度
- 只獲取最後一次提交（`-1`）
- 不獲取完整提交歷史
- 不執行網路操作（不檢查遠端）

## 目錄掃描演算法

### 遞迴掃描邏輯

```python
def scan_directory(path, depth, include_extensions, current_depth):
    """
    深度優先搜尋 (DFS) 實作
    
    終止條件:
    1. 達到最大深度
    2. 遇到權限錯誤
    3. 路徑不存在
    """
```

### 複雜度分析

- **時間複雜度**: O(N)，其中 N 為符合條件的檔案/目錄總數
- **空間複雜度**: O(D)，其中 D 為目錄深度（遞迴堆疊）

### 過濾機制

1. **名稱過濾**:
   ```python
   if entry.startswith('.'):  # 隱藏檔案
       continue
   if entry in ['node_modules', '__pycache__', 'venv']:
       continue
   ```

2. **副檔名過濾**:
   ```python
   if include_extensions is None or ext in include_extensions:
       # 包含此檔案
   ```

### 效能優化建議

- 對於大型專案（>10,000 檔案），建議使用 `depth=1` 或 `depth=2`
- 使用 `include_extensions` 過濾可大幅減少處理時間
- 避免掃描 `node_modules` 等大型目錄（已自動忽略）

## 配置檔案格式

### dashboard_state.yaml

```yaml
# 基本格式
favorites:
  - "project1"
  - "project2"
  - "/absolute/path/to/project3"

# 擴展格式（未來支援）
favorites:
  - "project1"

project_tags:
  project1:
    - python
    - web
    - flask

project_priority:
  project1: high
  project2: medium
```

### 路徑解析規則

1. **相對路徑**: 相對於 `projects/` 目錄
   - `"my_project"` → `projects/my_project`

2. **絕對路徑**: 直接使用
   - `"/home/user/work/project"` → `/home/user/work/project`

3. **驗證**: 檢查路徑是否為目錄

## MCP Protocol 整合

### 通訊方式

- **協議**: JSON-RPC 2.0
- **傳輸**: stdio (標準輸入/輸出)
- **格式**: JSON

### 訊息流程

```
┌─────────┐                      ┌─────────────┐
│  Claude │                      │ MCP Server  │
└────┬────┘                      └──────┬──────┘
     │                                  │
     │ 1. list_tools request            │
     │─────────────────────────────────>│
     │                                  │
     │ 2. tools list response           │
     │<─────────────────────────────────│
     │                                  │
     │ 3. call_tool request             │
     │    (get_focused_projects)        │
     │─────────────────────────────────>│
     │                                  │
     │                    4. Execute tool
     │                       - Load YAML
     │                       - Get git info
     │                       - Format result
     │                                  │
     │ 5. tool result response          │
     │<─────────────────────────────────│
     │                                  │
```

### 工具定義結構

```python
Tool(
    name="tool_name",
    description="詳細說明...",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "參數說明"
            }
        },
        "required": ["param1"]
    }
)
```

## 錯誤處理策略

### 1. 檔案系統錯誤

```python
try:
    entries = os.listdir(path)
except PermissionError:
    return {"files": [], "folders": []}  # 返回空結果
```

### 2. Git 錯誤

```python
try:
    result = subprocess.run(..., timeout=5)
except subprocess.TimeoutExpired:
    # 超時，返回預設值
except subprocess.CalledProcessError:
    # Git 命令失敗，返回預設值
```

### 3. YAML 解析錯誤

```python
try:
    state = yaml.safe_load(f)
except Exception as e:
    print(f"Error: {e}")
    return {"favorites": []}  # 返回安全預設值
```

### 錯誤響應格式

```json
{
  "error": "描述性錯誤訊息",
  "path": "/path/that/failed",
  "details": "額外的錯誤詳情"
}
```

## 測試策略

### 單元測試

測試每個輔助函數：
- `load_dashboard_state()`
- `get_git_info()`
- `scan_directory()`
- `get_project_basic_info()`

### 整合測試

模擬完整的工具調用流程：
1. 載入配置
2. 處理請求
3. 返回結果

### 測試腳本

使用 `test_mcp_server.py`:
```bash
python3 test_mcp_server.py
```

## 擴展指南

### 添加新工具

1. **定義工具** (`list_tools()`):
```python
Tool(
    name="new_tool",
    description="工具描述",
    inputSchema={...}
)
```

2. **實作處理器** (`call_tool()`):
```python
elif name == "new_tool":
    return await handle_new_tool(arguments)
```

3. **實作邏輯**:
```python
async def handle_new_tool(arguments):
    # 你的邏輯
    return [TextContent(type="text", text=json.dumps(result))]
```

### 添加新的元數據欄位

**宣告式元數據** (在 YAML 中):
```yaml
favorites: [...]

new_metadata:
  project1:
    field1: value1
    field2: value2
```

**衍生式元數據** (在程式碼中):
```python
def get_new_derived_info(path):
    # 計算衍生資訊
    return {"new_field": "computed_value"}
```

## 最佳實踐

### 1. 保持輕量

- Git 操作有超時限制
- 目錄掃描有深度限制
- 返回資料簡潔明瞭

### 2. 清晰的職責分離

- MCP Server: 提供資料
- LLM: 解讀和推理
- 使用者: 做出決策

### 3. 錯誤優雅處理

- 總是返回有效的 JSON
- 提供有意義的錯誤訊息
- 不要讓錯誤中斷整個流程

### 4. 可擴展設計

- 模組化函數
- 清晰的介面
- 易於添加新功能

## 效能考量

### 建議的配置

**小型專案集合** (< 10 projects):
- `depth`: 3-5
- 全副檔名掃描

**中型專案集合** (10-50 projects):
- `depth`: 2-3
- 使用副檔名過濾

**大型專案集合** (> 50 projects):
- `depth`: 1-2
- 嚴格的副檔名過濾
- 考慮實作快取

### 瓶頸識別

1. **Git 操作**: 最耗時，已設置超時
2. **目錄掃描**: 使用深度限制控制
3. **YAML 解析**: 通常很快

## 安全考量

### 1. 路徑驗證

```python
if not os.path.isdir(path):
    return error_response("Invalid path")
```

### 2. 命令注入防護

- 使用 `subprocess.run()` 而非 `os.system()`
- Git 命令參數經過驗證
- 不執行使用者提供的命令

### 3. 權限檢查

- 妥善處理 `PermissionError`
- 不嘗試訪問受保護的目錄

## 版本管理

### v2 變更

- ✅ 完整的 MCP Protocol 實作
- ✅ 兩個核心工具
- ✅ 清晰的元數據分類
- ✅ 完整的錯誤處理
- ✅ 測試腳本

### 未來規劃 (v3)

- [ ] 快取機制
- [ ] 更多衍生元數據（LOC, 複雜度）
- [ ] WebSocket 支援
- [ ] 專案健康度評分

## 參考資源

- [MCP Protocol 規範](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Git 命令參考](https://git-scm.com/docs)
