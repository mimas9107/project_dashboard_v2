# Claude Code CLI - MCP Server 設定指南

本指南說明如何在 Linux 環境下使用 Claude Code CLI 搭配 Project Dashboard MCP Server。

## 📋 前置需求

- Linux 作業系統
- Claude Code CLI 已安裝
- Python 3.8+
- Git（建議）

## 🚀 快速設定

### 步驟 1: 確認 Claude Code CLI 已安裝

```bash
claude --version
```

如果尚未安裝，請參考：https://docs.anthropic.com/claude/docs/claude-code

### 步驟 2: 找到 Claude Code 配置檔案

Claude Code CLI 的 MCP Server 配置檔案通常位於：

```bash
~/.config/claude-code/mcp.json
```

或

```bash
~/.claude-code/mcp.json
```

檢查檔案是否存在：
```bash
ls -la ~/.config/claude-code/mcp.json
# 或
ls -la ~/.claude-code/mcp.json
```

如果不存在，建立目錄和檔案：
```bash
mkdir -p ~/.config/claude-code
touch ~/.config/claude-code/mcp.json
```

### 步驟 3: 配置 MCP Server

編輯 `~/.config/claude-code/mcp.json`：

```bash
nano ~/.config/claude-code/mcp.json
# 或使用你喜歡的編輯器
vim ~/.config/claude-code/mcp.json
```

加入以下配置：

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/home/你的使用者名稱/path/to/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**重要**: 將路徑替換為你的實際路徑。使用絕對路徑！

### 步驟 4: 驗證配置

檢查配置檔案格式是否正確：

```bash
cat ~/.config/claude-code/mcp.json | python3 -m json.tool
```

如果沒有錯誤訊息，表示 JSON 格式正確。

### 步驟 5: 測試 MCP Server

先確認 MCP Server 可以獨立運行：

```bash
cd /path/to/project_dashboard_v2
python3 test_standalone.py
```

### 步驟 6: 啟動 Claude Code 並測試

```bash
# 啟動 Claude Code
claude

# 或在特定專案目錄啟動
cd /your/project
claude
```

在 Claude Code 中測試：

```
顯示我的所有重點專案
```

如果成功，你應該會看到專案列表！

## 📝 完整配置範例

### 基本配置

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/home/justin/projects/project_dashboard_v2/mcp_server.py"
      ]
    }
  }
}
```

### 使用虛擬環境

如果你使用 Python 虛擬環境：

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "/home/justin/projects/project_dashboard_v2/venv/bin/python",
      "args": [
        "/home/justin/projects/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 多個 MCP Server

如果你有多個 MCP Server：

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/home/justin/projects/project_dashboard_v2/mcp_server.py"
      ]
    },
    "another-server": {
      "command": "node",
      "args": [
        "/home/justin/projects/another-mcp/server.js"
      ]
    }
  }
}
```

## 🔧 進階配置

### 使用 Shell 腳本啟動

建立啟動腳本 `start_mcp.sh`：

```bash
#!/bin/bash
cd /home/justin/projects/project_dashboard_v2
source venv/bin/activate  # 如果使用虛擬環境
exec python3 mcp_server.py
```

賦予執行權限：
```bash
chmod +x start_mcp.sh
```

配置檔案：
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "/home/justin/projects/project_dashboard_v2/start_mcp.sh",
      "args": []
    }
  }
}
```

### 設定環境變數

如果需要特定環境變數：

```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": [
        "/home/justin/projects/project_dashboard_v2/mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "/home/justin/projects/project_dashboard_v2",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🐛 疑難排解

### 問題 1: MCP Server 無法啟動

**症狀**: Claude Code 啟動後沒有顯示工具

**解決方案**:

1. 檢查 Python 路徑：
```bash
which python3
# 使用輸出的完整路徑
```

2. 測試 MCP Server 是否可以運行：
```bash
python3 /path/to/mcp_server.py
# 不應該有錯誤
```

3. 檢查依賴是否安裝：
```bash
python3 -c "import mcp, yaml"
# 如果報錯，安裝依賴
pip install mcp pyyaml
```

### 問題 2: 找不到配置檔案路徑

**解決方案**:

嘗試以下位置：
```bash
# 方案 1
~/.config/claude-code/mcp.json

# 方案 2
~/.claude-code/mcp.json

# 方案 3
~/.config/claude/mcp.json
```

或查看 Claude Code 的文件：
```bash
claude --help
```

### 問題 3: 權限問題

**症狀**: Permission denied

**解決方案**:

1. 確認檔案有執行權限：
```bash
chmod +x /path/to/mcp_server.py
```

2. 確認 Python 可以訪問：
```bash
python3 /path/to/mcp_server.py
```

### 問題 4: 模組找不到

**症狀**: ModuleNotFoundError: No module named 'mcp'

**解決方案**:

安裝依賴：
```bash
pip install --user mcp pyyaml
# 或
pip3 install --user mcp pyyaml
```

如果使用虛擬環境：
```bash
cd /path/to/project_dashboard_v2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

然後在配置中使用虛擬環境的 Python：
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "/path/to/project_dashboard_v2/venv/bin/python",
      "args": ["/path/to/project_dashboard_v2/mcp_server.py"]
    }
  }
}
```

### 問題 5: JSON 格式錯誤

**症狀**: Error parsing config file

**解決方案**:

驗證 JSON 格式：
```bash
cat ~/.config/claude-code/mcp.json | python3 -m json.tool
```

常見錯誤：
- 缺少逗號
- 多餘的逗號（最後一個元素後）
- 路徑中的反斜線未轉義（Windows）
- 引號不匹配

### 問題 6: 工具顯示但無法使用

**解決方案**:

1. 檢查 dashboard_state.yaml 是否存在：
```bash
ls -la /path/to/project_dashboard_v2/dashboard_state.yaml
```

2. 檢查專案路徑是否正確：
```bash
cat /path/to/project_dashboard_v2/dashboard_state.yaml
```

3. 運行測試腳本：
```bash
cd /path/to/project_dashboard_v2
python3 test_standalone.py
```

## 📖 使用範例

配置完成後，在 Claude Code 中可以這樣使用：

### 範例 1: 查看重點專案

```
你: 幫我看看我的重點專案狀態

Claude: [自動使用 get_focused_projects 工具]
你有 3 個重點專案：
- my_web_app: 乾淨，2天前提交
- data_analysis_project: 有未提交變更
- automation_scripts: 乾淨，1天前提交
```

### 範例 2: 分析專案結構

```
你: 分析 my_web_app 專案的結構

Claude: [使用 scan_project 工具]
專案包含：
- 15 個 Python 檔案
- 3 個 Markdown 文件
- 主要目錄：src/, tests/, docs/
```

### 範例 3: 檢查 Git 狀態

```
你: 哪些專案需要提交？

Claude: [使用 get_focused_projects 獲取狀態]
以下專案有未提交的變更：
- data_analysis_project
```

## 🔄 更新配置

如果修改了配置檔案，需要重啟 Claude Code：

```bash
# 退出 Claude Code
exit 或 Ctrl+D

# 重新啟動
claude
```

## 📋 配置檢查清單

在配置前確認：

- [ ] Python 3.8+ 已安裝
- [ ] `mcp` 和 `pyyaml` 已安裝
- [ ] `mcp_server.py` 有執行權限
- [ ] 使用絕對路徑
- [ ] JSON 格式正確
- [ ] `dashboard_state.yaml` 存在並配置正確
- [ ] 測試腳本運行成功

## 🎯 最佳實踐

1. **使用絕對路徑**: 避免相對路徑問題
2. **虛擬環境**: 隔離 Python 依賴
3. **測試先行**: 配置前先測試 MCP Server
4. **版本控制**: 備份配置檔案
5. **日誌記錄**: 必要時添加日誌

## 📚 相關資源

- [Claude Code 官方文件](https://docs.anthropic.com/claude/docs/claude-code)
- [MCP Protocol 文件](https://modelcontextprotocol.io/)
- [專案 README](README.md)
- [開發者文件](DEVELOPMENT.md)

## 💡 提示

- Claude Code CLI 和 Claude Desktop 使用不同的配置檔案
- Linux 下通常使用 `~/.config/claude-code/mcp.json`
- 配置修改後需要重啟 Claude Code
- 使用 `claude --help` 查看更多選項

---

**注意**: Claude Code CLI 的配置可能隨版本更新而變化，請參考最新的官方文件。
