# app/routers/analyze.py
from fastapi import APIRouter, HTTPException
from ..services.resume_analyzer import analyze_resume
from ..schemas.resume import ResumeAnalysis

router = APIRouter(prefix="/analyze", tags=["简历分析"])

@router.post("/", response_model=ResumeAnalysis)
async def analyze(resume: dict):
    """
    接收结构化简历 JSON，返回 AI 分析结果。
    请求体示例：
    {
        "name": "吉伟翔",
        "phone": "15102303275",
        "email": "2669520581@qq.com",
        "school": "重庆科技大学",
        "major": "智能科学与技术",
        "skills": ["Python", "PyTorch", "OpenCV"],
        "projects": ["家乡宣传网页", "数据可视化仪表盘"]
    }
    """
    try:
        result = analyze_resume(resume)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))