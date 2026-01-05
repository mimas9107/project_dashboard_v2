# 配置快速參考

## Claude Desktop vs Claude Code CLI - 配置差異

### Claude Desktop（圖形介面）

**配置檔案位置:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**配置格式:**
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}
```

---

### Claude Code CLI（命令列介面）🐧

**配置檔案位置:**
- Linux: `~/.config/claude-code/mcp.json`
- 或: `~/.claude-code/mcp.json`

**建立配置:**
```bash
mkdir -p ~/.config/claude-code
nano ~/.config/claude-code/mcp.json
```

**配置格式:**
```json
{
  "mcpServers": {
    "project-dashboard": {
      "command": "python3",
      "args": ["/absolute/path/to/mcp_server.py"],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**重啟 Claude Code:**
```bash
# 退出（Ctrl+D 或 exit）
# 重新啟動
claude
```

---

## 快速檢查清單

### 安裝前
- [ ] Python 3.8+ 已安裝
- [ ] Git 已安裝（建議）
- [ ] 確認 Claude Desktop 或 Claude Code CLI 已安裝

### 安裝
- [ ] 解壓專案到合適位置
- [ ] `pip install -r requirements.txt`
- [ ] `python3 test_standalone.py` 測試通過

### 配置
- [ ] 找到正確的配置檔案位置
- [ ] 使用**絕對路徑**
- [ ] JSON 格式正確（無語法錯誤）
- [ ] `dashboard_state.yaml` 存在並配置

### 測試
- [ ] 重啟應用程式（Desktop 或 CLI）
- [ ] 工具顯示在可用工具列表中
- [ ] 測試 `get_focused_projects`
- [ ] 測試 `scan_project`

---

## 常見路徑錯誤

❌ **錯誤寫法:**
```json
"args": ["./mcp_server.py"]           // 相對路徑
"args": ["~/project/mcp_server.py"]   // ~ 符號
"args": ["$HOME/project/mcp_server.py"] // 環境變數
```

✅ **正確寫法:**
```json
"args": ["/home/justin/project_dashboard_v2/mcp_server.py"]
```

---

## 快速驗證

### 驗證 Python 可用
```bash
which python3
python3 --version
```

### 驗證依賴已安裝
```bash
python3 -c "import mcp, yaml; print('OK')"
```

### 驗證 MCP Server 可執行
```bash
python3 /path/to/mcp_server.py
# 應該啟動並等待 stdin（Ctrl+C 退出）
```

### 驗證 JSON 格式
```bash
# Claude Desktop
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Claude Code CLI
cat ~/.config/claude-code/mcp.json | python3 -m json.tool
```

---

## 疑難排解速查

| 問題 | 可能原因 | 解決方案 |
|-----|---------|---------|
| 工具不顯示 | 路徑錯誤 | 使用絕對路徑 |
| JSON 解析錯誤 | 格式錯誤 | 驗證 JSON 格式 |
| ModuleNotFoundError | 依賴未安裝 | `pip install mcp pyyaml` |
| Permission denied | 權限不足 | `chmod +x mcp_server.py` |
| Git 資訊為空 | 非 Git 倉庫 | `git init` 初始化 |

---

## 完整文件連結

- **完整配置指南**: [CLAUDE_CODE_SETUP.md](CLAUDE_CODE_SETUP.md)
- **快速開始**: [QUICKSTART.md](QUICKSTART.md)
- **詳細說明**: [README.md](README.md)
- **專案總覽**: [OVERVIEW.md](OVERVIEW.md)

---

**記住**: Claude Desktop 和 Claude Code CLI 的配置檔案**位置不同**！
