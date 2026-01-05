#!/usr/bin/env python3
"""
Project Dashboard MCP Server v2
A Minimal MCP Server exposing project management tools for LLM usage.

Tools:
1. get_focused_projects() - Returns favorite projects with git info
2. scan_project(path, options) - Scans a project folder on-demand
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
import yaml
import json

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# ===== Configuration =====
DASHBOARD_STATE_FILE = "dashboard_state.yaml"
PROJECTS_DIR = "projects"


# ===== Helper Functions =====

def load_dashboard_state() -> Dict[str, Any]:
    """
    Load the dashboard state from YAML file.
    Returns favorites list and other metadata.
    """
    if not os.path.exists(DASHBOARD_STATE_FILE):
        return {"favorites": []}
    
    try:
        with open(DASHBOARD_STATE_FILE, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}
            return state
    except Exception as e:
        print(f"Error loading dashboard state: {e}")
        return {"favorites": []}


def get_git_info(project_path: str) -> Dict[str, Any]:
    """
    Get lightweight git information for a project.
    
    Returns:
        - has_git: bool (whether .git directory exists)
        - dirty: bool (whether there are uncommitted changes)
        - last_commit_days: int (days since last commit, -1 if no commits)
    """
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
        # Check if dirty (uncommitted changes)
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
            
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError) as e:
        print(f"Git info error for {project_path}: {e}")
    
    return git_info


def scan_directory(
    path: str, 
    depth: int = 2,
    include_extensions: Optional[List[str]] = None,
    current_depth: int = 0
) -> Dict[str, Any]:
    """
    Recursively scan a directory and return file/folder structure.
    
    Args:
        path: Directory path to scan
        depth: Maximum depth to scan (default: 2)
        include_extensions: List of file extensions to include (e.g., [".py", ".js"])
        current_depth: Current recursion depth (internal use)
    
    Returns:
        Dictionary containing:
        - files: List of file paths
        - folders: List of folder paths
        - extensions_present: Set of file extensions found
    """
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
        # Skip hidden files and common ignore patterns
        if entry.startswith('.') or entry in ['node_modules', '__pycache__', 'venv', '.venv']:
            continue
        
        full_path = os.path.join(path, entry)
        
        if os.path.isfile(full_path):
            ext = os.path.splitext(entry)[1]
            
            # Filter by extension if specified
            if include_extensions is None or ext in include_extensions:
                result["files"].append(full_path)
                if ext:
                    result["extensions_present"].add(ext)
        
        elif os.path.isdir(full_path):
            result["folders"].append(full_path)
            
            # Recursive scan
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


def get_project_basic_info(project_path: str) -> Dict[str, Any]:
    """
    Get basic project information (name, path).
    
    Args:
        project_path: Path to the project
    
    Returns:
        Dictionary with project name and path
    """
    return {
        "name": os.path.basename(project_path),
        "path": project_path
    }


# ===== MCP Server Setup =====

server = Server("project-dashboard-v2")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """
    List available MCP tools.
    """
    return [
        Tool(
            name="get_focused_projects",
            description=(
                "Returns projects explicitly marked as 'favorite' in dashboard_state.yaml. "
                "Includes declared metadata (favorite status) and derived metadata "
                "(git info: has_git, dirty, last_commit_days)."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="scan_project",
            description=(
                "Performs derived-on-demand recursive scanning of a project folder. "
                "Returns files, folders, extensions present, and git info. "
                "Options: depth (int), include_extensions (list of extensions like ['.py', '.js']). "
                "Does not modify declared metadata, only returns derived facts."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the project folder to scan"
                    },
                    "options": {
                        "type": "object",
                        "description": "Scan options",
                        "properties": {
                            "depth": {
                                "type": "integer",
                                "description": "Maximum depth to scan (default: 2)",
                                "default": 2
                            },
                            "include_extensions": {
                                "type": "array",
                                "description": "List of file extensions to include (e.g., ['.html', '.js'])",
                                "items": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["path"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle tool calls from the LLM.
    """
    if name == "get_focused_projects":
        return await handle_get_focused_projects()
    elif name == "scan_project":
        return await handle_scan_project(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_get_focused_projects() -> List[TextContent]:
    """
    Handle get_focused_projects tool call.
    
    Returns favorite projects with git-derived information.
    """
    state = load_dashboard_state()
    favorites = state.get("favorites", [])
    
    projects_info = []
    
    for fav_path in favorites:
        # Support both absolute and relative paths
        if not os.path.isabs(fav_path):
            full_path = os.path.join(PROJECTS_DIR, fav_path)
        else:
            full_path = fav_path
        
        if not os.path.isdir(full_path):
            continue
        
        # Get basic info
        project_info = get_project_basic_info(full_path)
        
        # Add declared metadata
        project_info["favorite"] = True
        
        # Add derived metadata (git info)
        project_info["git_info"] = get_git_info(full_path)
        
        projects_info.append(project_info)
    
    result = {
        "focused_projects": projects_info,
        "total_count": len(projects_info)
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def handle_scan_project(arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Handle scan_project tool call.
    
    Performs on-demand scanning of a project directory.
    """
    project_path = arguments.get("path")
    options = arguments.get("options", {})
    
    if not project_path:
        raise ValueError("Missing required argument: path")
    
    if not os.path.isdir(project_path):
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": f"Path does not exist or is not a directory: {project_path}"
            })
        )]
    
    # Extract options
    depth = options.get("depth", 2)
    include_extensions = options.get("include_extensions")
    
    # Perform directory scan
    scan_result = scan_directory(
        project_path,
        depth=depth,
        include_extensions=include_extensions
    )
    
    # Get git info
    git_info = get_git_info(project_path)
    
    # Prepare result
    result = {
        "path": project_path,
        "name": os.path.basename(project_path),
        "scan_options": {
            "depth": depth,
            "include_extensions": include_extensions
        },
        "files": scan_result["files"],
        "folders": scan_result["folders"],
        "extensions_present": sorted(list(scan_result["extensions_present"])),
        "file_count": len(scan_result["files"]),
        "folder_count": len(scan_result["folders"]),
        "git_info": git_info
    }
    
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


# ===== Main Entry Point =====

async def main():
    """
    Main entry point for the MCP server.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
