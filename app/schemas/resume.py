# app/schemas/resume.py
from pydantic import BaseModel, Field

class Dimensions(BaseModel):
    technical_skills: int = Field(..., ge=0, le=100, description="技术能力评分")
    project_quality: int = Field(..., ge=0, le=100, description="项目质量评分")
    job_match: int = Field(..., ge=0, le=100, description="岗位匹配度评分")
    resume_completeness: int = Field(..., ge=0, le=100, description="简历完整度评分")

class ResumeAnalysis(BaseModel):
    dimensions: Dimensions
    score: int = Field(..., ge=0, le=100, description="综合得分")
    strengths: list[str] = Field(..., min_length=1)
    weaknesses: list[str] = Field(..., min_length=1)
    suggestions: list[str] = Field(..., min_length=1)