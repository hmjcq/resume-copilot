"""
简历分析 Prompt 模块（企业级）
仅负责根据结构化简历拼装完整的 Prompt 字符串。
"""

import json


def build_resume_prompt(resume: dict) -> str:
    """
    生成面向资深技术负责人的专业分析 Prompt，要求 AI 返回包含四维评分和综合得分的 JSON。
    """
    resume_json_str = json.dumps(resume, ensure_ascii=False, indent=2)

    prompt = f"""你是一名拥有 10 年以上招聘经验的 Python 后端技术负责人。
你的任务是对候选人的简历进行严格、客观的分析，完全按照企业招聘标准评判，不允许任何鼓励或客套话。

请从以下四个维度进行评分（每个维度 0-100 分）：
1. 技术能力：编程语言、框架、工具链的掌握深度与广度
2. 项目质量：项目复杂度、技术挑战、实际成果与影响力
3. 岗位匹配度：与典型 Python 后端/算法岗位要求的契合程度
4. 简历完整度：教育背景、技能、项目、实习/工作经历的完整性与清晰度

并给出综合得分（综合得分不是平均，而是体现你对岗位匹配度的权衡）。

评分参考：
- 90+ 分：技术领先，有高难度项目或开源贡献，可直接胜任高级工程师
- 80-89 分：基础扎实，有独立负责模块的能力，适合中级岗位
- 70-79 分：能满足基本工作要求，但部分领域需指导
- 60-69 分：具备一定知识，但项目经验或技能广度不足
- 60 分以下：尚未达到初级工程师的最低要求

另外，请列出：
- strengths：3 条优势
- weaknesses：3 条不足
- suggestions：3 条具体改进建议

**必须严格按以下 JSON 格式返回，不要包含任何 Markdown 标记或解释文字：**
{{
  "dimensions": {{
    "technical_skills": 75,
    "project_quality": 60,
    "job_match": 70,
    "resume_completeness": 65
  }},
  "score": 68,
  "strengths": ["...", "...", "..."],
  "weaknesses": ["...", "...", "..."],
  "suggestions": ["...", "...", "..."]
}}

简历 JSON：
{resume_json_str}
"""
    return prompt.strip()