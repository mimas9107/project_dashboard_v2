"""
Project Dashboard v2 - Core Project Manager
統一的專案管理核心邏輯，供 Flask 和 MCP Server 共用
"""
import os
import subprocess
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ProjectManager:
    """專案管理核心類別"""
    
    # 支援的語言對應表
    LANGUAGE_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript', 
        '.ts': 'TypeScript',
        '.jsx': 'React',
        '.tsx': 'React',
        '.rs': 'Rust',
        '.go': 'Go',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.cs': 'C#',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.vue': 'Vue',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.json': 'JSON',
        '.xml': 'XML',
        '.md': 'Markdown'
    }
    
    # 忽略的目錄
    IGNORE_DIRS = {
        '.git', 'node_modules', '__pycache__', 'venv', '.venv',
        'env', 'dist', 'build', 'target', '.next', '.nuxt',
        'vendor', 'bin', 'obj', '.idea', '.vscode'
    }
    
    def __init__(self, scan_path: str):
        """
        初始化專案管理器
        
        Args:
            scan_path: 要掃描的根目錄路徑
        """
        self.scan_path = Path(scan_path).resolve()
        if not self.scan_path.exists():
            raise ValueError(f"掃描路徑不存在: {scan_path}")
    
    def validate_project_path(self, project_name: str) -> Path:
        """
        驗證專案路徑安全性（防止目錄遍歷攻擊）
        
        Args:
            project_name: 專案名稱
            
        Returns:
            驗證後的專案路徑
            
        Raises:
            ValueError: 路徑不安全或不存在
        """
        target = (self.scan_path / project_name).resolve()
        
        # 檢查是否在掃描路徑內
        try:
            target.relative_to(self.scan_path)
        except ValueError:
            raise ValueError(f"不安全的專案路徑: {project_name}")
        
        if not target.exists():
            raise ValueError(f"專案不存在: {project_name}")
        
        return target
    
    def list_all_projects(self) -> List[Dict]:
        """
        列出所有有效專案（包含 README.md 的資料夾）
        
        Returns:
            專案列表，每個專案包含基本資訊
        """
        projects = []
        
        try:
            for entry in self.scan_path.iterdir():
                if not entry.is_dir():
                    continue
                
                readme_path = entry / 'README.md'
                if readme_path.exists():
                    projects.append({
                        'name': entry.name,
                        'path': str(entry),
                        'description': self._get_project_description(entry)
                    })
        except Exception as e:
            print(f"掃描專案時發生錯誤: {e}")
        
        return sorted(projects, key=lambda x: x['name'].lower())
    
    def get_project_info(self, project_name: str) -> Dict:
        """
        獲取指定專案的詳細資訊
        
        Args:
            project_name: 專案名稱
            
        Returns:
            包含語言分析、Git 狀態等資訊的字典
        """
        project_path = self.validate_project_path(project_name)
        
        return {
            'name': project_name,
            'path': str(project_path),
            'description': self._get_project_description(project_path),
            'languages': self.analyze_languages(project_path),
            'git_status': self.get_git_status(project_path),
            'has_git': self._has_git(project_path),
            'dependencies': self._get_dependencies(project_path)
        }
    
    def analyze_languages(self, project_path: Path) -> Dict[str, int]:
        """
        分析專案中各種程式語言的檔案佔比
        
        Args:
            project_path: 專案路徑
            
        Returns:
            語言佔比字典 {'Python': 45, 'JavaScript': 30, ...}
        """
        file_counts = Counter()
        
        try:
            for root, dirs, files in os.walk(project_path):
                # 過濾忽略目錄
                dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS and not d.startswith('.')]
                
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext in self.LANGUAGE_MAP:
                        file_counts[self.LANGUAGE_MAP[ext]] += 1
        except Exception as e:
            print(f"分析語言時發生錯誤: {e}")
            return {}
        
        total = sum(file_counts.values())
        if total == 0:
            return {}
        
        # 計算百分比並排序
        language_percentages = {
            lang: round((count / total) * 100)
            for lang, count in file_counts.most_common()
        }
        
        return language_percentages
    
    def get_git_status(self, project_path: Path) -> Tuple[str, str]:
        """
        獲取專案的 Git 狀態
        
        Args:
            project_path: 專案路徑
            
        Returns:
            (狀態, 詳細訊息) 元組
            狀態可能值: 'Clean', 'Modified', 'Not a Git repo', 'Error'
        """
        if not self._has_git(project_path):
            return ('Not a Git repo', 'This project is not a Git repository')
        
        try:
            # 檢查工作目錄狀態
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if status_result.returncode != 0:
                return ('Error', 'Failed to get Git status')
            
            if status_result.stdout.strip():
                # 計算修改檔案數量
                modified_files = len(status_result.stdout.strip().split('\n'))
                return ('Modified', f'{modified_files} file(s) changed')
            else:
                return ('Clean', 'No changes')
                
        except subprocess.TimeoutExpired:
            return ('Error', 'Git command timeout')
        except Exception as e:
            return ('Error', f'Git error: {str(e)}')
    
    def get_directory_tree(self, project_name: str, depth: int = 2) -> Dict:
        """
        獲取專案的目錄樹結構
        
        Args:
            project_name: 專案名稱
            depth: 遞迴深度限制
            
        Returns:
            樹狀結構字典
        """
        project_path = self.validate_project_path(project_name)
        return self._build_tree(project_path, depth)
    
    def _build_tree(self, path: Path, depth: int) -> Optional[Dict]:
        """遞迴建立目錄樹"""
        if depth < 0:
            return None
        
        tree = {
            'name': path.name,
            'type': 'folder' if path.is_dir() else 'file',
            'children': []
        }
        
        if not path.is_dir():
            return tree
        
        try:
            entries = []
            for entry in path.iterdir():
                # 忽略隱藏檔案和特定目錄
                if entry.name.startswith('.') or entry.name in self.IGNORE_DIRS:
                    continue
                
                if entry.is_dir():
                    child = self._build_tree(entry, depth - 1)
                    if child:
                        entries.append(child)
                else:
                    entries.append({
                        'name': entry.name,
                        'type': 'file'
                    })
            
            # 排序：資料夾在前，然後按名稱排序
            tree['children'] = sorted(
                entries,
                key=lambda x: (x['type'] != 'folder', x['name'].lower())
            )
        except PermissionError:
            pass
        
        return tree
    
    def _get_project_description(self, project_path: Path) -> str:
        """從 README.md 提取第一個標題作為描述"""
        readme_path = project_path / 'README.md'
        
        if not readme_path.exists():
            return "No description available"
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                for line in f:
                    content = line.strip()
                    if content.startswith('#'):
                        # 移除 # 符號並截斷過長內容
                        return content.lstrip('#').strip()[:100]
        except Exception:
            pass
        
        return "No description available"
    
    def _has_git(self, project_path: Path) -> bool:
        """檢查專案是否為 Git 倉庫"""
        return (project_path / '.git').is_dir()
    
    def _get_dependencies(self, project_path: Path) -> Dict[str, List[str]]:
        """
        獲取專案依賴（從 requirements.txt、package.json 等）
        
        Returns:
            {'python': [...], 'node': [...], ...}
        """
        dependencies = {}
        
        # Python dependencies
        req_file = project_path / 'requirements.txt'
        if req_file.exists():
            try:
                with open(req_file, 'r', encoding='utf-8') as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                    dependencies['python'] = deps[:10]  # 限制前 10 個
            except Exception:
                pass
        
        # Node.js dependencies
        package_json = project_path / 'package.json'
        if package_json.exists():
            try:
                import json
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    deps = list(data.get('dependencies', {}).keys())
                    dependencies['node'] = deps[:10]
            except Exception:
                pass
        
        return dependencies
    
    def search_by_language(self, language: str) -> List[Dict]:
        """
        搜尋使用特定語言的專案
        
        Args:
            language: 語言名稱（如 'Python', 'JavaScript'）
            
        Returns:
            符合條件的專案列表
        """
        matching_projects = []
        
        for project in self.list_all_projects():
            project_path = Path(project['path'])
            languages = self.analyze_languages(project_path)
            
            if language in languages:
                matching_projects.append({
                    **project,
                    'language_percentage': languages[language]
                })
        
        # 按語言佔比排序
        return sorted(
            matching_projects,
            key=lambda x: x['language_percentage'],
            reverse=True
        )
    
    def get_modified_projects(self) -> List[Dict]:
        """
        獲取所有有 Git 變更的專案
        
        Returns:
            有變更的專案列表
        """
        modified = []
        
        for project in self.list_all_projects():
            project_path = Path(project['path'])
            status, detail = self.get_git_status(project_path)
            
            if status == 'Modified':
                modified.append({
                    **project,
                    'git_detail': detail
                })
        
        return modified
    
    def find_projects_without_readme(self) -> List[str]:
        """
        找出缺少 README.md 的資料夾
        
        Returns:
            資料夾名稱列表
        """
        folders_without_readme = []
        
        try:
            for entry in self.scan_path.iterdir():
                if entry.is_dir() and not (entry / 'README.md').exists():
                    # 排除常見的非專案資料夾
                    if entry.name not in self.IGNORE_DIRS:
                        folders_without_readme.append(entry.name)
        except Exception as e:
            print(f"掃描資料夾時發生錯誤: {e}")
        
        return sorted(folders_without_readme)
    
    def batch_git_status(self) -> Dict[str, List[str]]:
        """
        批次取得所有專案的 Git 狀態摘要
        
        Returns:
            按狀態分組的專案字典
        """
        status_groups = {
            'Clean': [],
            'Modified': [],
            'Not a Git repo': [],
            'Error': []
        }
        
        for project in self.list_all_projects():
            project_path = Path(project['path'])
            status, _ = self.get_git_status(project_path)
            status_groups[status].append(project['name'])
        
        return status_groups
    
    def open_in_editor(self, project_name: str, editor: str = 'code') -> Tuple[bool, str]:
        """
        在編輯器中開啟專案
        
        Args:
            project_name: 專案名稱
            editor: 編輯器指令 ('code', 'cursor', 'pycharm', etc.)
            
        Returns:
            (成功與否, 訊息) 元組
        """
        try:
            project_path = self.validate_project_path(project_name)
            
            result = subprocess.run(
                [editor, str(project_path)],
                shell=(os.name == 'nt'),
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return (True, f"Successfully opened {project_name} in {editor}")
            else:
                return (False, f"Failed to open {editor}: {result.stderr.decode()}")
                
        except subprocess.TimeoutExpired:
            return (False, "Editor command timeout")
        except FileNotFoundError:
            return (False, f"Editor '{editor}' not found in PATH")
        except Exception as e:
            return (False, f"Error: {str(e)}")
