let allProjects = [];
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
}