#!/usr/bin/env python3
"""
Project Dashboard v2 - Setup Script
自動建立所有必要的檔案
"""

import os
from pathlib import Path

# 獲取腳本所在目錄
BASE_DIR = Path(__file__).parent

# ===== 前端 HTML =====
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Dashboard v2</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>

    <div class="container py-5">
        <header class="d-flex justify-content-between align-items-center mb-5">
            <div>
                <h1 class="fw-bold"><i class="bi bi-grid-1x2-fill text-primary me-2"></i>Project Dashboard v2</h1>
                <p class="mt-3 text-muted">本地開發環境自動化管理工具</p>
            </div>
            <div>
                <button class="btn btn-outline-light" onclick="showStatistics()">
                    <i class="bi bi-bar-chart-fill me-2"></i>統計資訊
                </button>
            </div>
        </header>
        
        <!-- 搜尋與篩選 -->
        <div class="row mb-4">
            <div class="col-md-6">
                <input type="text" id="searchInput" class="form-control" placeholder="搜尋專案...">
            </div>
            <div class="col-md-3">
                <select id="languageFilter" class="form-select">
                    <option value="">所有語言</option>
                </select>
            </div>
            <div class="col-md-3">
                <select id="tagFilter" class="form-select">
                    <option value="">所有標籤</option>
                </select>
            </div>
        </div>
        
        <div id="projectGrid" class="row g-4">
            <div class="col-12 text-center py-5">
                <div class="spinner-border text-primary"></div>
                <p class="mt-3">正在掃描專案...</p>
            </div>
        </div>
    </div>

    <!-- 目錄結構 Modal -->
    <div class="modal fade" id="structureModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content border-0 shadow">
                <div class="modal-header bg-dark text-white">
                    <h5 class="modal-title"><i class="bi bi-folder2-open me-2"></i><span id="modalTitle"></span></h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-4">
                    <div id="treeContent"></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 統計資訊 Modal -->
    <div class="modal fade" id="statsModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
            <div class="modal-content border-0 shadow">
                <div class="modal-header bg-primary text-white">
                    <h5 class="modal-title"><i class="bi bi-bar-chart-fill me-2"></i>工作區統計</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-4">
                    <div id="statsContent"></div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>'''

# ===== 前端 CSS =====
CSS_CONTENT = ''':root {
    --bg-dark: #121212;
    --card-bg: #1e1e1e;
    --text-main: #e0e0e0;
    --text-muted: #999;
    --accent: #0d6efd;
    --fav-gold: #ffc107;
}

body {
    background-color: var(--bg-dark);
    color: var(--text-main);
    font-family: 'Segoe UI', system-ui, sans-serif;
}

.project-card {
    background-color: var(--card-bg);
    border: 1px solid #333;
    cursor: pointer;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
}

.project-card:hover {
    transform: translateY(-5px);
    border-color: var(--accent);
    box-shadow: 0 8px 16px rgba(13, 110, 253, 0.3);
}

.project-title { 
    color: #fff; 
    font-weight: bold; 
    font-size: 1.1rem;
}

.project-desc { 
    color: var(--text-muted); 
    font-size: 0.9rem; 
    margin-bottom: 1rem; 
    min-height: 40px;
}

/* 語言標籤 */
.lang-badge { 
    border: none; 
    font-size: 0.7rem; 
    padding: 4px 8px; 
    border-radius: 4px; 
    color: #fff;
    margin-right: 4px;
    margin-bottom: 4px;
}

.lang-Python { background-color: #3572A5; }
.lang-JavaScript { background-color: #f1e05a; color: #000; }
.lang-TypeScript { background-color: #2b7489; }
.lang-React { background-color: #61dafb; color: #000; }
.lang-Rust { background-color: #dea584; }
.lang-Go { background-color: #00ADD8; }
.lang-HTML { background-color: #e34c26; }
.lang-CSS { background-color: #563d7c; }
.lang-Java { background-color: #b07219; }

/* 標籤 */
.tag-badge {
    font-size: 0.7rem;
    padding: 3px 7px;
    border-radius: 3px;
    background-color: #444;
    color: #ddd;
    margin-right: 4px;
}

/* 星號按鈕 */
.btn-fav { 
    background: none; 
    border: none; 
    font-size: 1.3rem; 
    color: #555; 
    transition: color 0.2s, transform 0.2s; 
}

.btn-fav:hover {
    transform: scale(1.1);
}

.btn-fav.active { 
    color: var(--fav-gold); 
    animation: star-pulse 0.3s ease-out;
}

@keyframes star-pulse {
    50% { transform: scale(1.3); }
}

/* 分隔線 */
.section-divider {
    border-top: 1px solid #333;
    margin: 3rem 0;
    position: relative;
    text-align: center;
}

.section-divider span {
    position: absolute; 
    top: -12px; 
    left: 50%; 
    transform: translateX(-50%);
    background: var(--bg-dark); 
    padding: 0 15px; 
    color: var(--text-muted); 
    font-size: 0.9rem;
    font-weight: 500;
}

/* 目錄樹 */
#treeContent { 
    background: #252525; 
    padding: 15px; 
    border-radius: 8px; 
    color: #ccc; 
    max-height: 500px;
    overflow-y: auto;
}

.tree-list { 
    list-style: none; 
    padding-left: 1.5rem; 
}

.tree-list li {
    margin: 5px 0;
    line-height: 1.8;
}

/* 搜尋框 */
#searchInput, .form-select {
    background-color: var(--card-bg);
    border-color: #333;
    color: var(--text-main);
}

#searchInput:focus, .form-select:focus {
    background-color: var(--card-bg);
    border-color: var(--accent);
    color: var(--text-main);
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

/* 統計卡片 */
.stat-card {
    background: var(--card-bg);
    border: 1px solid #333;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
}

.stat-value {
    font-size: 2.5rem;
    font-weight: bold;
    color: var(--accent);
}

.stat-label {
    color: var(--text-muted);
    font-size: 0.9rem;
}'''

# ===== 前端 JS =====
JS_CONTENT = '''let allProjects = [];
let allLanguages = new Set();
let allTags = new Set();

window.onload = () => {
    fetchProjects();
    loadFilters();
};

async function fetchProjects() {
    const grid = document.getElementById('projectGrid');
    try {
        const res = await fetch('/api/projects');
        allProjects = await res.json();
        
        renderProjects(allProjects);
        updateFilters();
    } catch (error) {
        grid.innerHTML = '<div class="col-12 text-center text-danger">載入失敗: ' + error.message + '</div>';
    }
}

function renderProjects(projects) {
    const grid = document.getElementById('projectGrid');
    
    const favs = projects.filter(p => p.is_favorite);
    const others = projects.filter(p => !p.is_favorite);

    let html = '';
    
    if (favs.length > 0) {
        html += favs.map(p => createCard(p)).join('');
        if (others.length > 0) {
            html += '<div class="col-12"><div class="section-divider"><span>其他專案</span></div></div>';
        }
    }
    
    html += others.map(p => createCard(p)).join('');
    
    grid.innerHTML = html || '<div class="col-12 text-center text-muted py-5">目前沒有專案</div>';
}

function createCard(p) {
    const langHtml = Object.entries(p.languages || {})
        .map(([l, pct]) => `<span class="badge lang-badge lang-${l}">${l} ${pct}%</span>`)
        .join(' ');
    
    const tagsHtml = (p.tags || [])
        .map(tag => `<span class="badge tag-badge">${tag}</span>`)
        .join(' ');

    const gitBadgeClass = p.git_status === 'Modified' ? 'bg-warning text-dark' : 
                         p.git_status === 'Clean' ? 'bg-success' : 'bg-secondary';

    return `
        <div class="col-md-4 mb-4">
            <div class="card h-100 project-card shadow-sm" onclick="showStructure('${p.name}')">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="project-title">${p.name}</h5>
                        <button class="btn-fav ${p.is_favorite ? 'active' : ''}" 
                                onclick="event.stopPropagation(); toggleFav('${p.name}')">
                            <i class="bi ${p.is_favorite ? 'bi-star-fill' : 'bi-star'}"></i>
                        </button>
                    </div>
                    <p class="project-desc">${p.description}</p>
                    <div class="mb-2">${langHtml}</div>
                    ${tagsHtml ? '<div class="mb-3">' + tagsHtml + '</div>' : ''}
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge ${gitBadgeClass}">
                            <i class="bi bi-git"></i> ${p.git_status || 'Unknown'}
                        </span>
                        <button class="btn btn-sm btn-outline-primary" 
                                onclick="event.stopPropagation(); openVSCode('${p.name}')">
                            <i class="bi bi-code-square"></i> VS Code
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function toggleFav(name) {
    await fetch('/api/favorite', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name})
    });
    fetchProjects();
}

async function showStructure(name) {
    document.getElementById('modalTitle').innerText = name;
    new bootstrap.Modal(document.getElementById('structureModal')).show();
    
    const res = await fetch(`/api/structure/${name}`);
    const data = await res.json();
    document.getElementById('treeContent').innerHTML = `<ul class="tree-list">${renderTree(data)}</ul>`;
}

function renderTree(node) {
    const icon = node.type === 'folder' ? 'bi-folder-fill text-warning' : 'bi-file-earmark-code text-info';
    let html = `<li><i class="bi ${icon}"></i> ${node.name}`;
    if (node.children && node.children.length > 0) {
        html += `<ul class="tree-list">${node.children.map(c => renderTree(c)).join('')}</ul>`;
    }
    return html + '</li>';
}

async function openVSCode(name) {
    await fetch(`/api/open/${name}`);
}

function updateFilters() {
    allProjects.forEach(p => {
        Object.keys(p.languages || {}).forEach(lang => allLanguages.add(lang));
        (p.tags || []).forEach(tag => allTags.add(tag));
    });
    
    const langFilter = document.getElementById('languageFilter');
    langFilter.innerHTML = '<option value="">所有語言</option>' + 
        [...allLanguages].sort().map(lang => `<option value="${lang}">${lang}</option>`).join('');
    
    const tagFilter = document.getElementById('tagFilter');
    tagFilter.innerHTML = '<option value="">所有標籤</option>' + 
        [...allTags].sort().map(tag => `<option value="${tag}">${tag}</option>`).join('');
}

function loadFilters() {
    document.getElementById('searchInput').addEventListener('input', filterProjects);
    document.getElementById('languageFilter').addEventListener('change', filterProjects);
    document.getElementById('tagFilter').addEventListener('change', filterProjects);
}

function filterProjects() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const selectedLang = document.getElementById('languageFilter').value;
    const selectedTag = document.getElementById('tagFilter').value;
    
    const filtered = allProjects.filter(p => {
        const matchesSearch = !searchTerm || 
            p.name.toLowerCase().includes(searchTerm) || 
            p.description.toLowerCase().includes(searchTerm);
        
        const matchesLang = !selectedLang || (p.languages && p.languages[selectedLang]);
        const matchesTag = !selectedTag || (p.tags && p.tags.includes(selectedTag));
        
        return matchesSearch && matchesLang && matchesTag;
    });
    
    renderProjects(filtered);
}

async function showStatistics() {
    const modal = new bootstrap.Modal(document.getElementById('statsModal'));
    modal.show();
    
    const res = await fetch('/api/statistics');
    const stats = await res.json();
    
    const content = document.getElementById('statsContent');
    content.innerHTML = `
        <div class="row">
            <div class="col-md-3 mb-3">
                <div class="stat-card">
                    <div class="stat-value">${stats.total_projects}</div>
                    <div class="stat-label">總專案數</div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="stat-card">
                    <div class="stat-value">${stats.favorites_count}</div>
                    <div class="stat-label">收藏專案</div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="stat-card">
                    <div class="stat-value">${stats.git_summary.modified}</div>
                    <div class="stat-label">有變更</div>
                </div>
            </div>
            <div class="col-md-3 mb-3">
                <div class="stat-card">
                    <div class="stat-value">${stats.git_summary.clean}</div>
                    <div class="stat-label">狀態乾淨</div>
                </div>
            </div>
        </div>
        <hr style="border-color: #333;">
        <h6 class="mb-3">Top 10 語言</h6>
        <div class="row">
            ${stats.top_languages.map(lang => `
                <div class="col-md-6 mb-2">
                    <span class="badge lang-badge lang-${lang.language}">${lang.language}</span>
                    <span class="text-muted">x ${lang.count} 個專案</span>
                </div>
            `).join('')}
        </div>
    `;
}'''

# ===== 啟動腳本 =====
BAT_WEB = '''@echo off
python app.py
pause'''

BAT_MCP = '''@echo off
python mcp_server.py
pause'''

# ===== 建立檔案 =====
def create_files():
    print("正在建立 Project Dashboard v2 檔案...")
    
    files = {
        'templates/index.html': HTML_CONTENT,
        'static/css/style.css': CSS_CONTENT,
        'static/js/script.js': JS_CONTENT,
        'start_web.bat': BAT_WEB,
        'start_mcp.bat': BAT_MCP,
        'core/__init__.py': '''"""
Project Dashboard v2 - Core Module
"""
from .project_manager import ProjectManager
from .database import DatabaseManager

__all__ = ['ProjectManager', 'DatabaseManager']
''',
        'tests/__init__.py': '# Tests module',
    }
    
    for filepath, content in files.items():
        full_path = BASE_DIR / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 已建立: {filepath}")
    
    print("\n✅ 所有檔案建立完成！")
    print("\n快速開始：")
    print("1. pip install -r requirements.txt")
    print("2. python app.py")
    print("3. 開啟瀏覽器: http://127.0.0.1:5001")

if __name__ == "__main__":
    create_files()
