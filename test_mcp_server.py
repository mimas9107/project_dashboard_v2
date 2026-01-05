#!/usr/bin/env python3
"""
Test script for Project Dashboard MCP Server v2
Tests the helper functions without running the full MCP server.
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import helper functions
from mcp_server import (
    load_dashboard_state,
    get_git_info,
    scan_directory,
    get_project_basic_info
)


def test_load_dashboard_state():
    """Test loading dashboard state"""
    print("=" * 60)
    print("Testing: load_dashboard_state()")
    print("=" * 60)
    
    state = load_dashboard_state()
    print(f"Dashboard State: {json.dumps(state, indent=2)}")
    print()


def test_git_info():
    """Test git info extraction"""
    print("=" * 60)
    print("Testing: get_git_info()")
    print("=" * 60)
    
    # Test current directory (should have git)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    git_info = get_git_info(current_dir)
    print(f"Git info for current directory:")
    print(json.dumps(git_info, indent=2))
    print()


def test_scan_directory():
    """Test directory scanning"""
    print("=" * 60)
    print("Testing: scan_directory()")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Test 1: Basic scan
    print("Test 1: Basic scan (depth=2)")
    result = scan_directory(current_dir, depth=2)
    print(f"Files found: {len(result['files'])}")
    print(f"Folders found: {len(result['folders'])}")
    print(f"Extensions: {sorted(list(result['extensions_present']))}")
    print()
    
    # Test 2: With extension filter
    print("Test 2: Scan with extension filter (.py, .yaml)")
    result = scan_directory(
        current_dir, 
        depth=2, 
        include_extensions=[".py", ".yaml", ".yml"]
    )
    print(f"Files found: {len(result['files'])}")
    print(f"Extensions: {sorted(list(result['extensions_present']))}")
    print(f"Files: {[os.path.basename(f) for f in result['files'][:5]]}")
    print()


def test_project_info():
    """Test project basic info"""
    print("=" * 60)
    print("Testing: get_project_basic_info()")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    info = get_project_basic_info(current_dir)
    print(json.dumps(info, indent=2))
    print()


def test_integrated_workflow():
    """Test integrated workflow simulating MCP tools"""
    print("=" * 60)
    print("Testing: Integrated Workflow")
    print("=" * 60)
    
    # Simulate get_focused_projects
    print("\n1. Simulating get_focused_projects:")
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
    print(json.dumps(result, indent=2))
    
    # Simulate scan_project
    print("\n2. Simulating scan_project:")
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
        "files": scan_result["files"][:5],  # Show first 5 files
        "file_count": len(scan_result["files"]),
        "folder_count": len(scan_result["folders"]),
        "extensions_present": sorted(list(scan_result["extensions_present"])),
        "git_info": git_info
    }
    print(json.dumps(result, indent=2))


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "Project Dashboard MCP Server v2 Tests" + " " * 11 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    test_load_dashboard_state()
    test_git_info()
    test_scan_directory()
    test_project_info()
    test_integrated_workflow()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
