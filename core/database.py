"""
Project Dashboard v2 - Database Manager
使用 SQLite 管理收藏、快取和專案元資料
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from contextlib import contextmanager


class DatabaseManager:
    """資料庫管理器"""
    
    def __init__(self, db_path: str = 'project_dashboard.db'):
        """
        初始化資料庫連接
        
        Args:
            db_path: 資料庫檔案路徑
        """
        self.db_path = Path(db_path)
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """資料庫連接上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 啟用字典式存取
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """初始化資料庫表結構"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 收藏表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    name TEXT PRIMARY KEY,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    order_index INTEGER DEFAULT 0,
                    notes TEXT
                )
            ''')
            
            # 專案快取表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_cache (
                    name TEXT PRIMARY KEY,
                    description TEXT,
                    languages JSON,
                    git_status TEXT,
                    git_detail TEXT,
                    has_git BOOLEAN,
                    last_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 專案標籤表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(project_name, tag)
                )
            ''')
            
            # 掃描歷史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    projects_found INTEGER,
                    scan_duration_ms INTEGER
                )
            ''')
            
            # 建立索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_order ON favorites(order_index)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cache_last_scan ON project_cache(last_scan)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags_project ON project_tags(project_name)')
    
    # ===== 收藏管理 =====
    
    def get_favorites(self) -> List[str]:
        """
        獲取所有收藏的專案名稱（按排序索引）
        
        Returns:
            專案名稱列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name FROM favorites 
                ORDER BY order_index ASC, added_at DESC
            ''')
            return [row['name'] for row in cursor.fetchall()]
    
    def get_favorites_detailed(self) -> List[Dict]:
        """
        獲取收藏的詳細資訊
        
        Returns:
            包含所有欄位的字典列表
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, added_at, order_index, notes 
                FROM favorites 
                ORDER BY order_index ASC, added_at DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def is_favorite(self, project_name: str) -> bool:
        """檢查專案是否為收藏"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM favorites WHERE name = ?', (project_name,))
            return cursor.fetchone() is not None
    
    def add_favorite(self, project_name: str, notes: str = None) -> bool:
        """
        新增收藏
        
        Args:
            project_name: 專案名稱
            notes: 備註（可選）
            
        Returns:
            是否成功新增
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # 取得當前最大排序索引
                cursor.execute('SELECT COALESCE(MAX(order_index), -1) + 1 FROM favorites')
                next_order = cursor.fetchone()[0]
                
                cursor.execute('''
                    INSERT INTO favorites (name, order_index, notes)
                    VALUES (?, ?, ?)
                ''', (project_name, next_order, notes))
                
                return True
        except sqlite3.IntegrityError:
            return False  # 已存在
    
    def remove_favorite(self, project_name: str) -> bool:
        """
        移除收藏
        
        Args:
            project_name: 專案名稱
            
        Returns:
            是否成功移除
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM favorites WHERE name = ?', (project_name,))
            return cursor.rowcount > 0
    
    def toggle_favorite(self, project_name: str) -> bool:
        """
        切換收藏狀態
        
        Args:
            project_name: 專案名稱
            
        Returns:
            切換後的狀態（True=已收藏, False=已取消）
        """
        if self.is_favorite(project_name):
            self.remove_favorite(project_name)
            return False
        else:
            self.add_favorite(project_name)
            return True
    
    def update_favorite_order(self, project_name: str, new_order: int) -> bool:
        """更新收藏的排序索引"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE favorites 
                SET order_index = ? 
                WHERE name = ?
            ''', (new_order, project_name))
            return cursor.rowcount > 0
    
    def update_favorite_notes(self, project_name: str, notes: str) -> bool:
        """更新收藏備註"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE favorites 
                SET notes = ? 
                WHERE name = ?
            ''', (notes, project_name))
            return cursor.rowcount > 0
    
    # ===== 快取管理 =====
    
    def cache_project(self, project_data: Dict):
        """
        快取專案資訊
        
        Args:
            project_data: 專案資料字典，必須包含 'name' 鍵
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO project_cache 
                (name, description, languages, git_status, git_detail, has_git, last_scan)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                project_data.get('name'),
                project_data.get('description'),
                json.dumps(project_data.get('languages', {})),
                project_data.get('git_status', ['Unknown', ''])[0],
                project_data.get('git_status', ['', ''])[1],
                project_data.get('has_git', False)
            ))
    
    def get_cached_project(self, project_name: str) -> Optional[Dict]:
        """
        從快取獲取專案資訊
        
        Args:
            project_name: 專案名稱
            
        Returns:
            專案資料字典或 None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT name, description, languages, git_status, git_detail, 
                       has_git, last_scan
                FROM project_cache 
                WHERE name = ?
            ''', (project_name,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'name': row['name'],
                    'description': row['description'],
                    'languages': json.loads(row['languages']) if row['languages'] else {},
                    'git_status': (row['git_status'], row['git_detail']),
                    'has_git': bool(row['has_git']),
                    'last_scan': row['last_scan']
                }
            return None
    
    def get_cache_age(self, project_name: str) -> Optional[float]:
        """
        獲取快取年齡（秒數）
        
        Returns:
            距離上次掃描的秒數，或 None（如果不存在）
        """
        cached = self.get_cached_project(project_name)
        if cached:
            last_scan = datetime.fromisoformat(cached['last_scan'])
            return (datetime.now() - last_scan).total_seconds()
        return None
    
    def clear_old_cache(self, max_age_days: int = 7):
        """清除過舊的快取"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM project_cache 
                WHERE last_scan < datetime('now', '-' || ? || ' days')
            ''', (max_age_days,))
            return cursor.rowcount
    
    # ===== 標籤管理 =====
    
    def add_tag(self, project_name: str, tag: str) -> bool:
        """為專案新增標籤"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO project_tags (project_name, tag)
                    VALUES (?, ?)
                ''', (project_name, tag.strip().lower()))
                return True
        except sqlite3.IntegrityError:
            return False  # 標籤已存在
    
    def remove_tag(self, project_name: str, tag: str) -> bool:
        """移除專案標籤"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM project_tags 
                WHERE project_name = ? AND tag = ?
            ''', (project_name, tag.strip().lower()))
            return cursor.rowcount > 0
    
    def get_project_tags(self, project_name: str) -> List[str]:
        """獲取專案的所有標籤"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT tag FROM project_tags 
                WHERE project_name = ?
                ORDER BY created_at DESC
            ''', (project_name,))
            return [row['tag'] for row in cursor.fetchall()]
    
    def find_by_tag(self, tag: str) -> List[str]:
        """搜尋具有特定標籤的專案"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT project_name 
                FROM project_tags 
                WHERE tag = ?
            ''', (tag.strip().lower(),))
            return [row['project_name'] for row in cursor.fetchall()]
    
    def get_all_tags(self) -> List[Dict[str, Any]]:
        """獲取所有標籤及其使用次數"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT tag, COUNT(*) as count
                FROM project_tags
                GROUP BY tag
                ORDER BY count DESC, tag ASC
            ''')
            return [{'tag': row['tag'], 'count': row['count']} for row in cursor.fetchall()]
    
    # ===== 統計與分析 =====
    
    def record_scan(self, projects_found: int, duration_ms: int):
        """記錄掃描歷史"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO scan_history (projects_found, scan_duration_ms)
                VALUES (?, ?)
            ''', (projects_found, duration_ms))
    
    def get_scan_history(self, limit: int = 10) -> List[Dict]:
        """獲取掃描歷史"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT scan_time, projects_found, scan_duration_ms
                FROM scan_history
                ORDER BY scan_time DESC
                LIMIT ?
            ''', (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict:
        """獲取統計資訊"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 收藏數量
            cursor.execute('SELECT COUNT(*) as count FROM favorites')
            favorites_count = cursor.fetchone()['count']
            
            # 快取數量
            cursor.execute('SELECT COUNT(*) as count FROM project_cache')
            cached_count = cursor.fetchone()['count']
            
            # 標籤數量
            cursor.execute('SELECT COUNT(DISTINCT tag) as count FROM project_tags')
            tags_count = cursor.fetchone()['count']
            
            # 最近掃描時間
            cursor.execute('SELECT MAX(scan_time) as last_scan FROM scan_history')
            last_scan = cursor.fetchone()['last_scan']
            
            return {
                'favorites_count': favorites_count,
                'cached_projects': cached_count,
                'total_tags': tags_count,
                'last_scan': last_scan
            }
    
    def export_data(self) -> Dict:
        """匯出所有資料（用於備份）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 匯出收藏
            cursor.execute('SELECT * FROM favorites')
            favorites = [dict(row) for row in cursor.fetchall()]
            
            # 匯出標籤
            cursor.execute('SELECT * FROM project_tags')
            tags = [dict(row) for row in cursor.fetchall()]
            
            return {
                'export_time': datetime.now().isoformat(),
                'favorites': favorites,
                'tags': tags
            }
    
    def import_data(self, data: Dict):
        """匯入資料（用於還原）"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 匯入收藏
            for fav in data.get('favorites', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO favorites (name, added_at, order_index, notes)
                    VALUES (?, ?, ?, ?)
                ''', (fav['name'], fav['added_at'], fav['order_index'], fav.get('notes')))
            
            # 匯入標籤
            for tag in data.get('tags', []):
                cursor.execute('''
                    INSERT OR IGNORE INTO project_tags (project_name, tag, created_at)
                    VALUES (?, ?, ?)
                ''', (tag['project_name'], tag['tag'], tag['created_at']))
