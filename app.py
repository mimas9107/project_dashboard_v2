"""
Project Dashboard v2 - FastAPI Web Application
前後端分離的 Web 介面
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

sys.path.insert(0, str(Path(__file__).parent))

from core.project_manager import ProjectManager
from core.database import DatabaseManager


def load_env(filepath=".env"):
    env_data = {
        "SCAN_DIR": "./",
        "HOST": "127.0.0.1",
        "PORT": 5001,
        "DB_PATH": "project_dashboard.db",
    }

    env_file = Path(filepath)
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_data[key] = value.strip('"').strip("'")

    return env_data


config = load_env()
SCAN_PATH = Path(config["SCAN_DIR"]).resolve()

project_manager = ProjectManager(str(SCAN_PATH))
db = DatabaseManager(config["DB_PATH"])

app = FastAPI(title="Project Dashboard v2")

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/projects")
async def get_projects():
    try:
        projects = project_manager.list_all_projects()
        favorites = set(db.get_favorites())

        enriched_projects = []
        for project in projects:
            info = project_manager.get_project_info(project["name"])

            git_status, git_detail = info["git_status"]

            enriched_projects.append(
                {
                    "name": info["name"],
                    "description": info["description"],
                    "languages": info["languages"],
                    "git_status": git_status,
                    "git_detail": git_detail,
                    "is_favorite": project["name"] in favorites,
                    "tags": db.get_project_tags(project["name"]),
                    "has_git": info["has_git"],
                }
            )

            db.cache_project(info)

        return JSONResponse(content=enriched_projects)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/project/{name}")
async def get_project_detail(name: str):
    try:
        info = project_manager.get_project_info(name)

        git_status, git_detail = info["git_status"]

        result = {
            **info,
            "git_status": git_status,
            "git_detail": git_detail,
            "is_favorite": db.is_favorite(name),
            "tags": db.get_project_tags(name),
            "cache_age": db.get_cache_age(name),
        }

        return JSONResponse(content=result)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/favorite")
async def toggle_favorite(data: dict = Body(...)):
    try:
        name = data.get("name")
        notes = data.get("notes")

        if not name:
            raise HTTPException(status_code=400, detail="缺少專案名稱")

        is_favorite = db.toggle_favorite(name)

        if is_favorite and notes:
            db.update_favorite_notes(name, notes)

        return JSONResponse(
            content={
                "status": "success",
                "is_favorite": is_favorite,
                "message": f"專案已{'加入' if is_favorite else '移除'}收藏",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/favorites")
async def get_favorites():
    try:
        favorites = db.get_favorites_detailed()
        return JSONResponse(content=favorites)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/structure/{name}")
async def get_structure(name: str, depth: int = Query(default=2)):
    try:
        tree = project_manager.get_directory_tree(name, depth)
        return JSONResponse(content=tree)

    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/open/{name}")
async def open_in_code(name: str, editor: str = Query(default="code")):
    try:
        success, message = project_manager.open_in_editor(name, editor)

        if success:
            return JSONResponse(content={"status": "success", "message": message})
        else:
            raise HTTPException(status_code=500, detail=message)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tags/{name}")
async def get_tags(name: str):
    try:
        tags = db.get_project_tags(name)
        return JSONResponse(content={"tags": tags})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tags/{name}")
async def add_tag(name: str, data: dict = Body(...)):
    try:
        tag = data.get("tag")
        if not tag:
            raise HTTPException(status_code=400, detail="缺少標籤名稱")

        success = db.add_tag(name, tag)
        return JSONResponse(
            content={
                "success": success,
                "message": f"已新增標籤 '{tag}'" if success else "標籤已存在",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/tags/{name}")
async def delete_tag(name: str, data: dict = Body(...)):
    try:
        tag = data.get("tag")
        if not tag:
            raise HTTPException(status_code=400, detail="缺少標籤名稱")

        success = db.remove_tag(name, tag)
        return JSONResponse(
            content={
                "success": success,
                "message": f"已移除標籤 '{tag}'" if success else "移除失敗",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tags")
async def get_all_tags():
    try:
        tags = db.get_all_tags()
        return JSONResponse(content=tags)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search/language/{language}")
async def search_by_language(language: str):
    try:
        results = project_manager.search_by_language(language)
        favorites = set(db.get_favorites())

        for project in results:
            project["is_favorite"] = project["name"] in favorites
            project["tags"] = db.get_project_tags(project["name"])

        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search/tag/{tag}")
async def search_by_tag(tag: str):
    try:
        projects = db.find_by_tag(tag)
        return JSONResponse(content={"projects": projects})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/git/modified")
async def get_modified_projects():
    try:
        modified = project_manager.get_modified_projects()
        return JSONResponse(content=modified)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/git/status")
async def batch_git_status():
    try:
        status_groups = project_manager.batch_git_status()
        return JSONResponse(content=status_groups)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/diagnostics/no-readme")
async def find_no_readme():
    try:
        folders = project_manager.find_projects_without_readme()
        return JSONResponse(content={"folders": folders})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
async def get_statistics():
    try:
        all_projects = project_manager.list_all_projects()

        language_counts = {}
        for project in all_projects:
            info = project_manager.get_project_info(project["name"])
            for lang in info["languages"].keys():
                language_counts[lang] = language_counts.get(lang, 0) + 1

        top_languages = sorted(
            language_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]

        git_summary = project_manager.batch_git_status()

        return JSONResponse(
            content={
                "total_projects": len(all_projects),
                "favorites_count": len(db.get_favorites()),
                "top_languages": [
                    {"language": lang, "count": count} for lang, count in top_languages
                ],
                "git_summary": {
                    "clean": len(git_summary["Clean"]),
                    "modified": len(git_summary["Modified"]),
                    "not_git": len(git_summary["Not a Git repo"]),
                    "errors": len(git_summary["Error"]),
                },
                "folders_without_readme": len(
                    project_manager.find_projects_without_readme()
                ),
                "database_stats": db.get_statistics(),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/cache/clear")
async def clear_cache(data: dict = Body(...)):
    try:
        max_age_days = data.get("max_age_days", 7)

        deleted = db.clear_old_cache(max_age_days)

        return JSONResponse(
            content={
                "status": "success",
                "deleted_count": deleted,
                "message": f"已清除 {deleted} 個快取記錄",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print(f"掃描路徑: {SCAN_PATH}")
    print(f"資料庫: {config['DB_PATH']}")

    uvicorn.run("app:app", host=config["HOST"], port=int(config["PORT"]), reload=True)
