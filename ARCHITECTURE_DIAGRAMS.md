# Project Dashboard MCP Server v2 - 架構圖

## 系統架構圖

```mermaid
graph TB
    subgraph "Claude LLM Environment"
        A[Claude LLM]
    end
    
    subgraph "MCP Server"
        B[stdio_server]
        C[Server Instance]
        D[Tool: get_focused_projects]
        E[Tool: scan_project]
        
        F[load_dashboard_state]
        G[get_git_info]
        H[scan_directory]
        I[get_project_basic_info]
    end
    
    subgraph "Data Layer"
        J[(dashboard_state.yaml)]
        K[File System]
        L[Git Repositories]
    end
    
    A <-->|JSON-RPC over stdio| B
    B --> C
    C --> D
    C --> E
    
    D --> F
    D --> G
    D --> I
    
    E --> H
    E --> G
    
    F --> J
    G --> L
    H --> K
    I --> K
    
    style A fill:#e1f5ff
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style J fill:#fff9c4
    style K fill:#fff9c4
    style L fill:#fff9c4
```

## 資料流程圖

```mermaid
sequenceDiagram
    participant C as Claude LLM
    participant M as MCP Server
    participant Y as YAML Config
    participant F as File System
    participant G as Git

    Note over C,G: Tool Call: get_focused_projects()
    
    C->>M: Request get_focused_projects
    M->>Y: Load favorites list
    Y-->>M: Return favorites
    
    loop For each favorite project
        M->>F: Check if path exists
        F-->>M: Path info
        M->>G: Get git status
        G-->>M: Git info (dirty, last_commit)
    end
    
    M-->>C: Return projects with metadata
    
    Note over C,G: Tool Call: scan_project(path, options)
    
    C->>M: Request scan_project
    M->>F: Recursive directory scan
    F-->>M: Files and folders
    M->>G: Get git info
    G-->>M: Git status
    M-->>C: Return scan results
```

## 元數據分類架構

```mermaid
graph LR
    subgraph "Declared Metadata"
        A1[User Preferences]
        A2[favorite status]
        A3[project tags]
        A4[priority levels]
    end
    
    subgraph "Derived Metadata"
        B1[Git Info]
        B2[has_git]
        B3[dirty status]
        B4[last_commit_days]
        B5[File Stats]
        B6[file count]
        B7[extensions]
    end
    
    subgraph "Storage"
        C1[dashboard_state.yaml]
    end
    
    subgraph "Calculation"
        C2[Real-time computation]
    end
    
    A1 --> A2
    A1 --> A3
    A1 --> A4
    A2 --> C1
    A3 --> C1
    A4 --> C1
    
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B5 --> B6
    B5 --> B7
    
    B2 --> C2
    B3 --> C2
    B4 --> C2
    B6 --> C2
    B7 --> C2
    
    style C1 fill:#fff9c4
    style C2 fill:#c8e6c9
```

## 工具處理流程

```mermaid
flowchart TD
    Start([Tool Call Request]) --> Route{Which Tool?}
    
    Route -->|get_focused_projects| GFP[Get Focused Projects]
    Route -->|scan_project| SP[Scan Project]
    
    GFP --> LoadYAML[Load YAML Config]
    LoadYAML --> GetFav[Get Favorites List]
    GetFav --> LoopProj{For Each Project}
    
    LoopProj -->|Yes| CheckPath[Check Path Exists]
    CheckPath --> GetBasic[Get Basic Info]
    GetBasic --> GetGit1[Get Git Info]
    GetGit1 --> AddToList[Add to Results]
    AddToList --> LoopProj
    
    LoopProj -->|No| FormatResp1[Format JSON Response]
    FormatResp1 --> Return1([Return to LLM])
    
    SP --> ValidPath{Valid Path?}
    ValidPath -->|No| Error[Return Error]
    Error --> Return2([Return to LLM])
    
    ValidPath -->|Yes| ParseOpts[Parse Options]
    ParseOpts --> ScanDir[Recursive Scan]
    ScanDir --> GetGit2[Get Git Info]
    GetGit2 --> CalcStats[Calculate Stats]
    CalcStats --> FormatResp2[Format JSON Response]
    FormatResp2 --> Return3([Return to LLM])
    
    style GFP fill:#c8e6c9
    style SP fill:#c8e6c9
    style LoadYAML fill:#fff9c4
    style ScanDir fill:#e1f5ff
    style GetGit1 fill:#e1f5ff
    style GetGit2 fill:#e1f5ff
```

## 目錄掃描演算法

```mermaid
graph TD
    Start([scan_directory]) --> Init[Initialize Results]
    Init --> CheckDir{Is Directory?}
    
    CheckDir -->|No| ReturnEmpty[Return Empty Results]
    CheckDir -->|Yes| CheckDepth{Depth < Max?}
    
    CheckDepth -->|No| ReturnEmpty
    CheckDepth -->|Yes| ListEntries[List Directory Entries]
    
    ListEntries --> Loop{For Each Entry}
    
    Loop -->|More| Filter{Should Process?}
    Filter -->|Hidden/Ignored| Loop
    
    Filter -->|Process| IsFile{Is File?}
    
    IsFile -->|Yes| CheckExt{Extension Match?}
    CheckExt -->|Yes| AddFile[Add to Files List]
    CheckExt -->|No| Loop
    AddFile --> Loop
    
    IsFile -->|No| IsDir{Is Directory?}
    IsDir -->|Yes| AddFolder[Add to Folders List]
    AddFolder --> Recurse[Recursive Call]
    Recurse --> Merge[Merge Results]
    Merge --> Loop
    
    Loop -->|Done| Return[Return Results]
    Return --> End([End])
    
    style Start fill:#e1f5ff
    style Filter fill:#fff9c4
    style Recurse fill:#c8e6c9
    style Return fill:#e1f5ff
```

## Git 資訊提取流程

```mermaid
flowchart TD
    Start([get_git_info]) --> InitVars[Initialize Variables]
    InitVars --> CheckGit{.git exists?}
    
    CheckGit -->|No| SetNoGit[has_git = False]
    SetNoGit --> Return1[Return Default Values]
    
    CheckGit -->|Yes| SetHasGit[has_git = True]
    SetHasGit --> TryStatus[Try: git status --porcelain]
    
    TryStatus --> Success1{Success?}
    Success1 -->|No| Timeout1[Handle Timeout/Error]
    Timeout1 --> Return2[Return Partial Info]
    
    Success1 -->|Yes| CheckOutput{Output Empty?}
    CheckOutput -->|No| SetDirty[dirty = True]
    CheckOutput -->|Yes| SetClean[dirty = False]
    
    SetDirty --> TryLog[Try: git log -1]
    SetClean --> TryLog
    
    TryLog --> Success2{Success?}
    Success2 -->|No| Timeout2[Handle Timeout/Error]
    Timeout2 --> Return3[Return Partial Info]
    
    Success2 -->|Yes| ParseTime[Parse Timestamp]
    ParseTime --> CalcDays[Calculate Days Diff]
    CalcDays --> SetDays[Set last_commit_days]
    SetDays --> Return4[Return Full Info]
    
    style CheckGit fill:#fff9c4
    style TryStatus fill:#e1f5ff
    style TryLog fill:#e1f5ff
    style Timeout1 fill:#ffccbc
    style Timeout2 fill:#ffccbc
```

## 錯誤處理架構

```mermaid
graph TD
    Start([Function Call]) --> Try[Try Block]
    
    Try --> FileOp{File Operation}
    Try --> GitOp{Git Operation}
    Try --> YAMLOp{YAML Operation}
    
    FileOp -->|Success| Continue1[Continue]
    FileOp -->|PermissionError| HandlePerm[Return Empty/Safe Default]
    FileOp -->|FileNotFoundError| HandleNotFound[Return Error Message]
    
    GitOp -->|Success| Continue2[Continue]
    GitOp -->|TimeoutExpired| HandleTimeout[Return Partial Info]
    GitOp -->|CalledProcessError| HandleGitError[Return Safe Default]
    
    YAMLOp -->|Success| Continue3[Continue]
    YAMLOp -->|YAMLError| HandleYAML[Return Empty Config]
    
    HandlePerm --> LogError[Log Error]
    HandleNotFound --> LogError
    HandleTimeout --> LogError
    HandleGitError --> LogError
    HandleYAML --> LogError
    
    Continue1 --> Success[Return Success]
    Continue2 --> Success
    Continue3 --> Success
    
    LogError --> Graceful[Graceful Degradation]
    Graceful --> End([End])
    Success --> End
    
    style HandlePerm fill:#ffccbc
    style HandleNotFound fill:#ffccbc
    style HandleTimeout fill:#ffccbc
    style HandleGitError fill:#ffccbc
    style HandleYAML fill:#ffccbc
    style Graceful fill:#fff9c4
```

## 擴展點架構

```mermaid
graph LR
    subgraph "Current Tools"
        T1[get_focused_projects]
        T2[scan_project]
    end
    
    subgraph "Future Tools"
        T3[analyze_project_health]
        T4[compare_projects]
        T5[generate_report]
    end
    
    subgraph "Helper Functions"
        H1[load_dashboard_state]
        H2[get_git_info]
        H3[scan_directory]
    end
    
    subgraph "New Helper Functions"
        H4[calculate_loc]
        H5[analyze_dependencies]
        H6[check_security]
    end
    
    T1 --> H1
    T1 --> H2
    T2 --> H2
    T2 --> H3
    
    T3 -.-> H2
    T3 -.-> H4
    T3 -.-> H5
    
    T4 -.-> H1
    T4 -.-> H3
    
    T5 -.-> H1
    T5 -.-> H6
    
    style T1 fill:#c8e6c9
    style T2 fill:#c8e6c9
    style T3 fill:#e3f2fd
    style T4 fill:#e3f2fd
    style T5 fill:#e3f2fd
```

---

這些圖表展示了 Project Dashboard MCP Server v2 的完整架構設計，包括：

1. **系統架構**: 整體組件關係
2. **資料流程**: Tool 調用的完整流程
3. **元數據分類**: Declared vs Derived 的架構
4. **工具處理**: 詳細的處理邏輯
5. **掃描演算法**: 遞迴目錄掃描的實作
6. **Git 資訊**: 資訊提取的完整流程
7. **錯誤處理**: 完善的錯誤處理機制
8. **擴展點**: 未來可擴展的方向

你可以使用支援 Mermaid 的工具（如 GitHub, VS Code, Typora）來渲染這些圖表。
