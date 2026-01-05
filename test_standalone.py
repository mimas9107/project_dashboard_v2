#!/usr/bin/env python3
"""
Standalone Test Script for Project Dashboard MCP Server v2
Tests the helper functions without importing the MCP module.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
import json
import yaml


# ===== Copy of Helper Functions from mcp_server.py =====

DASHBOARD_STATE_FILE = "dashboard_state.yaml"
PROJECTS_DIR = "projects"


def load_dashboard_state():
    """Load the dashboard state from YAML file."""
    if not os.path.exists(DASHBOARD_STATE_FILE):
        return {"favorites": []}
    
    try:
        with open(DASHBOARD_STATE_FILE, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}
            return state
    except Exception as e:
        print(f"Error loading dashboard state: {e}")
        return {"favorites": []}


def get_git_info(project_path):
    """Get lightweight git information for a project."""
    git_info = {
        "has_git": False,
        "dirty": False,
        "last_commit_days": -1
    }
    
    git_dir = os.path.join(project_path, ".git")
    if not os.path.isdir(git_dir):
        return git_info
    
    git_info["has_git"] = True
    
    try:
        # Check if dirty
        result = subprocess.run(
            ["git", "-C", project_path, "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        git_info["dirty"] = bool(result.stdout.strip())
        
        # Get last commit date
        result = subprocess.run(
            ["git", "-C", project_path, "log", "-1", "--format=%ct"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.strip():
            last_commit_timestamp = int(result.stdout.strip())
            last_commit_date = datetime.fromtimestamp(last_commit_timestamp)
            days_diff = (datetime.now() - last_commit_date).days
            git_info["last_commit_days"] = days_diff
            
    except Exception as e:
        print(f"Git info error for {project_path}: {e}")
    
    return git_info


def scan_directory(path, depth=2, include_extensions=None, current_depth=0):
    """Recursively scan a directory."""
    result = {
        "files": [],
        "folders": [],
        "extensions_present": set()
    }
    
    if not os.path.isdir(path):
        return result
    
    if current_depth >= depth:
        return result
    
    try:
        entries = os.listdir(path)
    except PermissionError:
        return result
    
    for entry in entries:
        if entry.startswith('.') or entry in ['node_modules', '__pycache__', 'venv', '.venv']:
            continue
        
        full_path = os.path.join(path, entry)
        
        if os.path.isfile(full_path):
            ext = os.path.splitext(entry)[1]
            
            if include_extensions is None or ext in include_extensions:
                result["files"].append(full_path)
                if ext:
                    result["extensions_present"].add(ext)
        
        elif os.path.isdir(full_path):
            result["folders"].append(full_path)
            
            sub_result = scan_directory(
                full_path, 
                depth, 
                include_extensions,
                current_depth + 1
            )
            result["files"].extend(sub_result["files"])
            result["folders"].extend(sub_result["folders"])
            result["extensions_present"].update(sub_result["extensions_present"])
    
    return result


def get_project_basic_info(project_path):
    """Get basic project information."""
    return {
        "name": os.path.basename(project_path),
        "path": project_path
    }


# ===== Test Functions =====

def test_load_dashboard_state():
    """Test loading dashboard state"""
    print("=" * 60)
    print("測試: load_dashboard_state()")
    print("=" * 60)
    
    state = load_dashboard_state()
    print(f"Dashboard State: {json.dumps(state, indent=2, ensure_ascii=False)}")
    print()
    return state


def test_git_info():
    """Test git info extraction"""
    print("=" * 60)
    print("測試: get_git_info()")
    print("=" * 60)
    
    # Test current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    git_info = get_git_info(current_dir)
    print(f"當前目錄的 Git 資訊:")
    print(json.dumps(git_info, indent=2, ensure_ascii=False))
    print()
    return git_info


def test_scan_directory():
    """Test directory scanning"""
    print("=" * 60)
    print("測試: scan_directory()")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Test 1: Basic scan
    print("測試 1: 基本掃描 (depth=2)")
    result = scan_directory(current_dir, depth=2)
    print(f"找到檔案: {len(result['files'])} 個")
    print(f"找到資料夾: {len(result['folders'])} 個")
    print(f"副檔名: {sorted(list(result['extensions_present']))}")
    if result['files']:
        print(f"前 5 個檔案: {[os.path.basename(f) for f in result['files'][:5]]}")
    print()
    
    # Test 2: With extension filter
    print("測試 2: 過濾掃描 (.py, .yaml, .md)")
    result = scan_directory(
        current_dir, 
        depth=2, 
        include_extensions=[".py", ".yaml", ".yml", ".md"]
    )
    print(f"找到檔案: {len(result['files'])} 個")
    print(f"副檔名: {sorted(list(result['extensions_present']))}")
    if result['files']:
        print(f"檔案列表: {[os.path.basename(f) for f in result['files']]}")
    print()
    return result


def test_project_info():
    """Test project basic info"""
    print("=" * 60)
    print("測試: get_project_basic_info()")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    info = get_project_basic_info(current_dir)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    print()
    return info


def test_integrated_workflow():
    """Test integrated workflow simulating MCP tools"""
    print("=" * 60)
    print("測試: 整合工作流程模擬")
    print("=" * 60)
    
    # Simulate get_focused_projects
    print("\n1️⃣  模擬 get_focused_projects:")
    print("-" * 60)
    state = load_dashboard_state()
    favorites = state.get("favorites", [])
    
    projects_info = []
    for fav_path in favorites:
        if not os.path.isabs(fav_path):
            full_path = os.path.join("projects", fav_path)
        else:
            full_path = fav_path
        
        # Create dummy project folders for testing
        os.makedirs(full_path, exist_ok=True)
        
        project_info = get_project_basic_info(full_path)
        project_info["favorite"] = True
        project_info["git_info"] = get_git_info(full_path)
        projects_info.append(project_info)
    
    result = {
        "focused_projects": projects_info,
        "total_count": len(projects_info)
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Simulate scan_project
    print("\n2️⃣  模擬 scan_project:")
    print("-" * 60)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scan_result = scan_directory(current_dir, depth=2)
    git_info = get_git_info(current_dir)
    
    result = {
        "path": current_dir,
        "name": os.path.basename(current_dir),
        "scan_options": {
            "depth": 2,
            "include_extensions": None
        },
        "files_sample": [os.path.basename(f) for f in scan_result["files"][:5]],
        "file_count": len(scan_result["files"]),
        "folder_count": len(scan_result["folders"]),
        "extensions_present": sorted(list(scan_result["extensions_present"])),
        "git_info": git_info
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def create_test_projects():
    """Create some test projects for demonstration"""
    print("=" * 60)
    print("建立測試專案...")
    print("=" * 60)
    
    test_projects = [
        "my_web_app",
        "data_analysis_project",
        "automation_scripts"
    ]
    
    for proj_name in test_projects:
        proj_path = os.path.join("projects", proj_name)
        os.makedirs(proj_path, exist_ok=True)
        
        # Create some dummy files
        readme_path = os.path.join(proj_path, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as f:
                f.write(f"# {proj_name}\n\nThis is a test project.\n")
        
        # Initialize git if not exists
        git_dir = os.path.join(proj_path, ".git")
        if not os.path.isdir(git_dir):
            try:
                subprocess.run(
                    ["git", "init"],
                    cwd=proj_path,
                    capture_output=True,
                    timeout=5
                )
                subprocess.run(
                    ["git", "add", "."],
                    cwd=proj_path,
                    capture_output=True,
                    timeout=5
                )
                subprocess.run(
                    ["git", "commit", "-m", "Initial commit"],
                    cwd=proj_path,
                    capture_output=True,
                    timeout=5
                )
                print(f"✅ 建立專案: {proj_name}")
            except Exception as e:
                print(f"⚠️  建立專案 {proj_name} 時發生錯誤: {e}")
    
    print()


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 8 + "Project Dashboard MCP Server v2 測試" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Create test projects first
    create_test_projects()
    
    # Run tests
    test_load_dashboard_state()
    test_git_info()
    test_scan_directory()
    test_project_info()
    test_integrated_workflow()
    
    print("=" * 60)
    print("✅ 所有測試完成！")
    print("=" * 60)
    print()
    print("📝 下一步:")
    print("   1. 檢查 dashboard_state.yaml 確認 favorites 列表")
    print("   2. 安裝 mcp 套件: pip install mcp")
    print("   3. 配置 Claude Desktop 使用這個 MCP Server")
    print("   4. 在 Claude 中使用工具測試功能")
    print()


if __name__ == "__main__":
    main()
