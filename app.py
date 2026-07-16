import os
import shutil
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Resume Copilot")

# 确保上传目录存在
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 首页：显示上传页面
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resume Copilot - 上传简历</title>
    </head>
    <body>
        <h2>上传 PDF 简历</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf" required>
            <button type="submit">上传</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 接收 PDF 并保存
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # 验证文件类型
    if file.content_type != "application/pdf":
        return JSONResponse(
            status_code=400,
            content={"message": "只允许上传 PDF 文件"}
        )
    
    # 保存文件到 uploads/
    file_path = UPLOAD_DIR / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": "上传成功，你的简历已保存", "filename": file.filename}

@app.get("/health")
def health():
    return {"status": "ok"}