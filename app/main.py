# app/main.py
import os
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader

# 导入各服务模块
from .services.pdf_parser import extract_text
from .services.resume_parser import parse_resume
from .services.resume_analyzer import analyze_resume

# 导入新的分析路由
from .routers import analyze

# ================== 路径配置 ==================
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"

# ================== 初始化应用 ==================
app = FastAPI(title="Resume Copilot")

# 模板引擎
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

# 挂载静态文件
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 注册分析路由
app.include_router(analyze.router)

# 确保上传目录存在
UPLOAD_DIR.mkdir(exist_ok=True)


# ================== 页面路由 ==================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """首页：上传 PDF 简历"""
    template = env.get_template("index.html")
    rendered = template.render(request=request)
    return HTMLResponse(content=rendered)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"message": "只允许上传 PDF 文件"})

    original_ext = os.path.splitext(file.filename)[1].lower()
    if original_ext != ".pdf":
        return JSONResponse(status_code=400, content={"message": "只允许上传 PDF 文件"})

    new_filename = f"{uuid.uuid4().hex}{original_ext}"
    file_path = UPLOAD_DIR / new_filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 默认错误，避免 analysis 为 None
    analysis = {"error": "分析未执行"}
    resume_info = {}
    try:
        resume_text = extract_text(file_path)
        resume_info = parse_resume(resume_text)
        analysis = analyze_resume(resume_info)
    except Exception as e:
        analysis = {"error": f"处理失败: {e}"}

    return {
        "message": "上传成功",
        "original_filename": file.filename,
        "saved_as": new_filename,
        "resume_info": resume_info,
        "analysis": analysis
    }


@app.get("/health")
def health():
    return {"status": "ok"}