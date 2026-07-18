"""
简历分析服务
提供 analyze_resume() 函数，将结构化简历转换为评分与建议。
整合 Prompt 构建、AI 调用、JSON 解析全流程。
"""

import json
from ..prompts.resume_prompt import build_resume_prompt
from .ai_service import ask_ai
from ..schemas.resume import ResumeAnalysis


def analyze_resume(resume: dict) -> dict:
    """
    对一份结构化简历进行 AI 分析。

    参数:
        resume: 简历字典。

    返回:
        dict: 包含 score, strengths, weaknesses, suggestions 的分析结果。

    异常:
        ValueError: AI 返回内容无法解析为有效 JSON 或字段不符合预期时抛出。
        Exception: 其他调用错误直接向上抛出。
    """
    # 1. 构建 Prompt
    prompt = build_resume_prompt(resume)

    # 2. 调用 AI
    raw_response = ask_ai(prompt)

    # 3. 清洗并解析 JSON
    data = _extract_json(raw_response)

    # 4. 使用 Pydantic 进行数据校验和类型转换
    try:
        analysis = ResumeAnalysis.model_validate(data)
    except Exception as e:
        raise ValueError(f"AI 返回的数据不符合要求: {e}")

    # 5. 返回字典（方便 JSON 序列化）
    return analysis.model_dump()


def _extract_json(text: str) -> dict:
    """从 AI 返回的文本中提取 JSON 对象"""
    text = text.strip()
    # 去掉可能的 Markdown 代码块标记
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    # 找到第一个 { 和最后一个 }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("未在响应中找到 JSON 对象")

    json_str = text[start:end+1]
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}\n原始内容: {text}")