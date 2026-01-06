"""
Project Dashboard v2 - Enhanced MCP Server
提供豐富的工具讓 AI 助理管理本地專案
"""
import os
import sys
from pathlib import Path
from typing import List, Dict

# 加入核心模組路徑
sys.path.insert(0, str(Path(__file__).parent))

from fastmcp import FastMCP
from core.project_manager import ProjectManager
from core.database import DatabaseManager


# ===== 環境設定 =====
def load_env(filepath='.env'):
    """載入環境變數"""
    env_data = {
        'SCAN_DIR': '..',  # 預設掃描上層目錄
        'DB_PATH': 'project_dashboard.db'
    }
    
    env_file = Path(filepath)
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_data[key] = value.strip('"').strip("'")
    
    return env_data


# 初始化
config = load_env()
SCAN_PATH = Path(__file__).parent / config['SCAN_DIR']
SCAN_PATH = SCAN_PATH.resolve()

project_manager = ProjectManager(str(SCAN_PATH))
db = DatabaseManager(config['DB_PATH'])

mcp = FastMCP("Project Dashboard v2")


# ===== 基礎專案管理工具 =====

@mcp.tool()
def list_projects() -> List[Dict]:
    """
    列出所有專案及其基本資訊
    
    Returns:
        專案列表，包含名稱、描述和收藏狀態
    """
    projects = project_manager.list_all_projects()
    favorites = set(db.get_favorites())
    
    # 加入收藏狀態
    for project in projects:
        project['is_favorite'] = project['name'] in favorites
        project['tags'] = db.get_project_tags(project['name'])
    
    return projects


@mcp.tool()
def get_project_info(name: str) -> Dict:
    """
    獲取指定專案的詳細資訊
    
    Args:
        name: 專案名稱
        
    Returns:
        包含語言分析、Git 狀態、依賴等完整資訊
    """
    try:
        info = project_manager.get_project_info(name)
        
        # 加入資料庫資訊
        info['is_favorite'] = db.is_favorite(name)
        info['tags'] = db.get_project_tags(name)
        
        # 快取資訊
        db.cache_project(info)
        
        return info
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool()
def get_project_files(name: str, depth: int = 2) -> Dict:
    """
    獲取專案的檔案目錄結構
    
    Args:
        name: 專案名稱
        depth: 遞迴深度（預設 2 層）
        
    Returns:
        樹狀結構字典
    """
    try:
        return project_manager.get_directory_tree(name, depth)
    except ValueError as e:
        return {"error": str(e)}


# ===== 搜尋與篩選工具 =====

@mcp.tool()
def search_projects_by_language(language: str) -> List[Dict]:
    """
    搜尋使用特定程式語言的專案
    
    Args:
        language: 語言名稱（例如: Python, JavaScript, Rust, Go）
        
    Returns:
        符合條件的專案列表，按語言佔比排序
        
    Examples:
        - search_projects_by_language("Python")
        - search_projects_by_language("TypeScript")
    """
    results = project_manager.search_by_language(language)
    
    # 加入收藏狀態
    favorites = set(db.get_favorites())
    for project in results:
        project['is_favorite'] = project['name'] in favorites
    
    return results


@mcp.tool()
def search_projects_by_tag(tag: str) -> List[str]:
    """
    搜尋具有特定標籤的專案
    
    Args:
        tag: 標籤名稱（例如: web, api, experimental）
        
    Returns:
        專案名稱列表
    """
    return db.find_by_tag(tag)


@mcp.tool()
def get_all_tags() -> List[Dict]:
    """
    獲取所有標籤及其使用次數
    
    Returns:
        標籤列表，包含每個標籤的使用次數
    """
    return db.get_all_tags()


# ===== Git 管理工具 =====

@mcp.tool()
def get_modified_projects() -> List[Dict]:
    """
    快速找出所有有 Git 變更的專案
    
    Returns:
        有未提交變更的專案列表
    """
    return project_manager.get_modified_projects()


@mcp.tool()
def batch_git_status() -> Dict[str, List[str]]:
    """
    批次取得所有專案的 Git 狀態摘要
    
    Returns:
        按狀態分組的專案字典
        - Clean: 無變更
        - Modified: 有未提交變更
        - Not a Git repo: 不是 Git 倉庫
        - Error: 檢查失敗
    """
    return project_manager.batch_git_status()


# ===== 專案診斷工具 =====

@mcp.tool()
def find_projects_without_readme() -> List[str]:
    """
    找出缺少 README.md 的資料夾
    
    這些資料夾可能是未完成的專案或需要整理的目錄
    
    Returns:
        資料夾名稱列表
    """
    return project_manager.find_projects_without_readme()


@mcp.tool()
def analyze_workspace_summary() -> Dict:
    """
    分析整個工作區的統計摘要
    
    Returns:
        包含專案總數、語言分布、Git 狀態等統計資訊
    """
    all_projects = project_manager.list_all_projects()
    
    # 統計語言分布
    language_totals = {}
    git_status_summary = project_manager.batch_git_status()
    
    for project in all_projects:
        info = project_manager.get_project_info(project['name'])
        for lang, percentage in info['languages'].items():
            language_totals[lang] = language_totals.get(lang, 0) + 1
    
    # 排序語言
    top_languages = sorted(
        language_totals.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return {
        "total_projects": len(all_projects),
        "favorites_count": len(db.get_favorites()),
        "top_languages": [{"language": lang, "project_count": count} for lang, count in top_languages],
        "git_status": {
            "clean": len(git_status_summary['Clean']),
            "modified": len(git_status_summary['Modified']),
            "not_git": len(git_status_summary['Not a Git repo']),
            "errors": len(git_status_summary['Error'])
        },
        "folders_without_readme": len(project_manager.find_projects_without_readme()),
        "database_stats": db.get_statistics()
    }


# ===== 收藏管理工具 =====

@mcp.tool()
def toggle_project_favorite(name: str) -> Dict:
    """
    切換專案的收藏狀態
    
    Args:
        name: 專案名稱
        
    Returns:
        操作結果和新狀態
    """
    is_favorite = db.toggle_favorite(name)
    
    return {
        "project": name,
        "is_favorite": is_favorite,
        "message": f"專案 '{name}' 已{'加入' if is_favorite else '移除'}收藏"
    }


@mcp.tool()
def list_favorites() -> List[Dict]:
    """
    列出所有收藏的專案（含詳細資訊）
    
    Returns:
        收藏專案列表，包含加入時間和備註
    """
    return db.get_favorites_detailed()


@mcp.tool()
def update_favorite_notes(name: str, notes: str) -> Dict:
    """
    更新收藏專案的備註
    
    Args:
        name: 專案名稱
        notes: 備註內容
        
    Returns:
        操作結果
    """
    success = db.update_favorite_notes(name, notes)
    
    return {
        "success": success,
        "message": f"已更新 '{name}' 的備註" if success else "更新失敗"
    }


# ===== 標籤管理工具 =====

@mcp.tool()
def add_project_tag(name: str, tag: str) -> Dict:
    """
    為專案新增標籤
    
    Args:
        name: 專案名稱
        tag: 標籤名稱（例如: web, api, deprecated）
        
    Returns:
        操作結果
    """
    success = db.add_tag(name, tag)
    
    return {
        "success": success,
        "message": f"已為 '{name}' 新增標籤 '{tag}'" if success else "標籤已存在或新增失敗"
    }


@mcp.tool()
def remove_project_tag(name: str, tag: str) -> Dict:
    """
    移除專案標籤
    
    Args:
        name: 專案名稱
        tag: 要移除的標籤
        
    Returns:
        操作結果
    """
    success = db.remove_tag(name, tag)
    
    return {
        "success": success,
        "message": f"已從 '{name}' 移除標籤 '{tag}'" if success else "移除失敗"
    }


@mcp.tool()
def get_project_tags(name: str) -> List[str]:
    """
    獲取專案的所有標籤
    
    Args:
        name: 專案名稱
        
    Returns:
        標籤列表
    """
    return db.get_project_tags(name)


# ===== 編輯器整合工具 =====

@mcp.tool()
def open_in_vscode(name: str) -> Dict:
    """
    在 VS Code 中開啟專案
    
    Args:
        name: 專案名稱
        
    Returns:
        操作結果
    """
    success, message = project_manager.open_in_editor(name, 'code')
    
    return {
        "success": success,
        "message": message
    }


@mcp.tool()
def open_in_editor(name: str, editor: str = 'code') -> Dict:
    """
    在指定編輯器中開啟專案
    
    Args:
        name: 專案名稱
        editor: 編輯器指令（code, cursor, pycharm, subl 等）
        
    Returns:
        操作結果
    """
    success, message = project_manager.open_in_editor(name, editor)
    
    return {
        "success": success,
        "editor": editor,
        "message": message
    }


# ===== 資料管理工具 =====

@mcp.tool()
def clear_old_cache(max_age_days: int = 7) -> Dict:
    """
    清除過舊的專案快取
    
    Args:
        max_age_days: 保留最近幾天的快取（預設 7 天）
        
    Returns:
        清除結果
    """
    deleted_count = db.clear_old_cache(max_age_days)
    
    return {
        "deleted_count": deleted_count,
        "message": f"已清除 {deleted_count} 個過舊的快取記錄"
    }


@mcp.tool()
def export_favorites_and_tags() -> Dict:
    """
    匯出收藏和標籤資料（用於備份）
    
    Returns:
        包含所有收藏和標籤的 JSON 資料
    """
    return db.export_data()


@mcp.tool()
def get_dashboard_statistics() -> Dict:
    """
    獲取儀表板的統計資訊
    
    Returns:
        包含收藏數、快取數、標籤數等統計資料
    """
    return db.get_statistics()


# ===== 智能建議工具 =====

@mcp.tool()
def suggest_next_actions() -> List[str]:
    """
    AI 主動建議下一步動作
    
    基於當前專案狀態，提供智能建議：
    - 有未提交變更需要處理
    - 收藏數量過多需要整理
    - 發現缺少 README 的專案
    
    Returns:
        建議列表
    """
    suggestions = []
    
    # 檢查 Git 變更
    modified = project_manager.get_modified_projects()
    if modified:
        suggestions.append(f"⚠️ 有 {len(modified)} 個專案有未提交的變更")
        suggestions.extend([f"  - {p['name']}: {p['git_detail']}" for p in modified[:3]])
    
    # 檢查收藏數量
    favorites = db.get_favorites()
    if len(favorites) > 10:
        suggestions.append(f"📌 您有 {len(favorites)} 個收藏專案，考慮使用標籤分類管理")
    
    # 檢查缺少 README 的專案
    no_readme = project_manager.find_projects_without_readme()
    if no_readme:
        suggestions.append(f"📝 有 {len(no_readme)} 個資料夾缺少 README.md")
        suggestions.extend([f"  - {folder}" for folder in no_readme[:3]])
    
    # 檢查快取
    stats = db.get_statistics()
    if stats['cached_projects'] > 50:
        suggestions.append("🧹 建議清理過舊的快取以節省空間")
    
    if not suggestions:
        suggestions.append("✅ 所有專案狀態良好！")
    
    return suggestions


if __name__ == "__main__":
    # 啟動 MCP Server
    mcp.run()
