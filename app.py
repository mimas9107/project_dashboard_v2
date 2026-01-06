"""
Project Dashboard v2 - Flask Web Application
前後端分離的 Web 介面
"""
import os
import sys
from pathlib import Path
from flask import Flask, jsonify, render_template, request, abort

# 加入核心模組路徑
sys.path.insert(0, str(Path(__file__).parent))

from core.project_manager import ProjectManager
from core.database import DatabaseManager


# ===== 環境設定 =====
def load_env(filepath='.env'):
    """載入環境變數"""
    env_data = {
        'SCAN_DIR': './',
        'HOST': '127.0.0.1',
        'PORT': 5001,
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
SCAN_PATH = Path(config['SCAN_DIR']).resolve()

project_manager = ProjectManager(str(SCAN_PATH))
db = DatabaseManager(config['DB_PATH'])

app = Flask(__name__)


# ===== 路由 =====

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')


@app.route('/api/projects')
def get_projects():
    """獲取所有專案列表"""
    try:
        projects = project_manager.list_all_projects()
        favorites = set(db.get_favorites())
        
        # 豐富專案資訊
        enriched_projects = []
        for project in projects:
            info = project_manager.get_project_info(project['name'])
            
            # 格式化 Git 狀態
            git_status, git_detail = info['git_status']
            
            enriched_projects.append({
                'name': info['name'],
                'description': info['description'],
                'languages': info['languages'],
                'git_status': git_status,
                'git_detail': git_detail,
                'is_favorite': project['name'] in favorites,
                'tags': db.get_project_tags(project['name']),
                'has_git': info['has_git']
            })
            
            # 快取資訊
            db.cache_project(info)
        
        return jsonify(enriched_projects)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/project/<name>')
def get_project_detail(name):
    """獲取單一專案的詳細資訊"""
    try:
        info = project_manager.get_project_info(name)
        
        # 格式化 Git 狀態
        git_status, git_detail = info['git_status']
        
        result = {
            **info,
            'git_status': git_status,
            'git_detail': git_detail,
            'is_favorite': db.is_favorite(name),
            'tags': db.get_project_tags(name),
            'cache_age': db.get_cache_age(name)
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorite', methods=['POST'])
def toggle_favorite():
    """切換專案收藏狀態"""
    try:
        data = request.json
        name = data.get('name')
        notes = data.get('notes')
        
        if not name:
            return jsonify({'error': '缺少專案名稱'}), 400
        
        is_favorite = db.toggle_favorite(name)
        
        # 如果提供了備註，更新備註
        if is_favorite and notes:
            db.update_favorite_notes(name, notes)
        
        return jsonify({
            'status': 'success',
            'is_favorite': is_favorite,
            'message': f"專案已{'加入' if is_favorite else '移除'}收藏"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/favorites')
def get_favorites():
    """獲取所有收藏專案"""
    try:
        favorites = db.get_favorites_detailed()
        return jsonify(favorites)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/structure/<name>')
def get_structure(name):
    """獲取專案目錄結構"""
    try:
        depth = int(request.args.get('depth', 2))
        tree = project_manager.get_directory_tree(name, depth)
        return jsonify(tree)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/open/<name>')
def open_in_code(name):
    """在編輯器中開啟專案"""
    try:
        editor = request.args.get('editor', 'code')
        success, message = project_manager.open_in_editor(name, editor)
        
        if success:
            return jsonify({'status': 'success', 'message': message})
        else:
            return jsonify({'status': 'failed', 'message': message}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tags/<name>', methods=['GET', 'POST', 'DELETE'])
def manage_tags(name):
    """管理專案標籤"""
    try:
        if request.method == 'GET':
            tags = db.get_project_tags(name)
            return jsonify({'tags': tags})
        
        elif request.method == 'POST':
            data = request.json
            tag = data.get('tag')
            if not tag:
                return jsonify({'error': '缺少標籤名稱'}), 400
            
            success = db.add_tag(name, tag)
            return jsonify({
                'success': success,
                'message': f"已新增標籤 '{tag}'" if success else '標籤已存在'
            })
        
        elif request.method == 'DELETE':
            data = request.json
            tag = data.get('tag')
            if not tag:
                return jsonify({'error': '缺少標籤名稱'}), 400
            
            success = db.remove_tag(name, tag)
            return jsonify({
                'success': success,
                'message': f"已移除標籤 '{tag}'" if success else '移除失敗'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tags')
def get_all_tags():
    """獲取所有標籤及使用次數"""
    try:
        tags = db.get_all_tags()
        return jsonify(tags)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/language/<language>')
def search_by_language(language):
    """按語言搜尋專案"""
    try:
        results = project_manager.search_by_language(language)
        favorites = set(db.get_favorites())
        
        for project in results:
            project['is_favorite'] = project['name'] in favorites
            project['tags'] = db.get_project_tags(project['name'])
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/search/tag/<tag>')
def search_by_tag(tag):
    """按標籤搜尋專案"""
    try:
        projects = db.find_by_tag(tag)
        return jsonify({'projects': projects})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/git/modified')
def get_modified_projects():
    """獲取所有有變更的專案"""
    try:
        modified = project_manager.get_modified_projects()
        return jsonify(modified)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/git/status')
def batch_git_status():
    """批次獲取所有專案的 Git 狀態摘要"""
    try:
        status_groups = project_manager.batch_git_status()
        return jsonify(status_groups)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/diagnostics/no-readme')
def find_no_readme():
    """找出缺少 README 的資料夾"""
    try:
        folders = project_manager.find_projects_without_readme()
        return jsonify({'folders': folders})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def get_statistics():
    """獲取工作區統計資訊"""
    try:
        all_projects = project_manager.list_all_projects()
        
        # 統計語言分布
        language_counts = {}
        for project in all_projects:
            info = project_manager.get_project_info(project['name'])
            for lang in info['languages'].keys():
                language_counts[lang] = language_counts.get(lang, 0) + 1
        
        top_languages = sorted(
            language_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        git_summary = project_manager.batch_git_status()
        
        return jsonify({
            'total_projects': len(all_projects),
            'favorites_count': len(db.get_favorites()),
            'top_languages': [
                {'language': lang, 'count': count}
                for lang, count in top_languages
            ],
            'git_summary': {
                'clean': len(git_summary['Clean']),
                'modified': len(git_summary['Modified']),
                'not_git': len(git_summary['Not a Git repo']),
                'errors': len(git_summary['Error'])
            },
            'folders_without_readme': len(project_manager.find_projects_without_readme()),
            'database_stats': db.get_statistics()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """清除過舊的快取"""
    try:
        data = request.json or {}
        max_age_days = data.get('max_age_days', 7)
        
        deleted = db.clear_old_cache(max_age_days)
        
        return jsonify({
            'status': 'success',
            'deleted_count': deleted,
            'message': f'已清除 {deleted} 個快取記錄'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    print(f"掃描路徑: {SCAN_PATH}")
    print(f"資料庫: {config['DB_PATH']}")
    
    app.run(
        debug=True,
        host=config['HOST'],
        port=int(config['PORT'])
    )
