"""
简历结构化解析模块
提供 parse_resume() 函数，将纯文本简历转换为结构化字典。
当前版本使用正则表达式 + 规则提取，后续可替换为 AI 模型。
"""

import re
from typing import List, Dict


def parse_resume(text: str) -> dict:
    """
    解析简历文本，返回结构化信息。

    参数:
        text: 从 PDF 提取的纯文本字符串。

    返回:
        dict: 包含姓名、电话、邮箱、学校、专业、技能、项目等字段。
    """
    result = {
        "name": _extract_name(text),
        "phone": _extract_phone(text),
        "email": _extract_email(text),
        "school": _extract_school(text),
        "major": _extract_major(text),
        "skills": _extract_skills(text),
        "projects": _extract_projects(text),
    }
    return result


# ==================== 内部提取函数 ====================

def _extract_name(text: str) -> str:
    """
    简单规则提取姓名：
    假设简历开头第一行非空行就是姓名。
    """
    lines = text.strip().splitlines()
    for line in lines:
        line = line.strip()
        if line:
            # 一般姓名不会太长，也不会包含大量英文或数字
            if len(line) <= 20 and not re.search(r'[a-zA-Z0-9@]', line):
                return line
    return ""


def _extract_phone(text: str) -> str:
    """提取中国大陆手机号（11位数字，1开头）"""
    pattern = r'1[3-9]\d{9}'
    match = re.search(pattern, text)
    return match.group() if match else ""


def _extract_email(text: str) -> str:
    """提取电子邮箱"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group() if match else ""


def _extract_school(text: str) -> str:
    """提取学校名称（常见关键词：大学/学院）"""
    pattern = r'[\u4e00-\u9fa5]+大学|[\u4e00-\u9fa5]+学院'
    match = re.search(pattern, text)
    return match.group() if match else ""


def _extract_major(text: str) -> str:
    # 匹配“xxx专业”“xxx方向”“xxx系”
    pattern = r'([\u4e00-\u9fa5]+)(?:专业|方向|系)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)  # 只返回专业名称本身

    # 备选：常见专业关键词
    major_keywords = ['计算机科学', '软件工程', '智能科学与技术', '数据科学', '人工智能', '网络工程']
    for kw in major_keywords:
        if kw in text:
            return kw
    return ""


def _extract_skills(text: str) -> List[str]:
    """
    提取技能关键词（常见编程语言/框架/工具）。
    此处为演示，后续可接入 AI 做更精准的 NER。
    """
    skill_candidates = [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust",
        "PyTorch", "TensorFlow", "Keras", "OpenCV", "Scikit-learn", "Pandas", "NumPy",
        "Vue", "React", "Angular", "Node.js", "Django", "Flask", "FastAPI",
        "MySQL", "PostgreSQL", "MongoDB", "Redis",
        "Docker", "Kubernetes", "Git", "Linux"
    ]
    found = []
    text_lower = text.lower()
    for skill in skill_candidates:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(set(found))  # 去重


def _extract_projects(text: str) -> List[str]:
    projects = []
    # 匹配：项目名称：xxx 或 项目：xxx 或 Project: xxx（不区分大小写）
    pattern = r'(?:项目名称|项目|Project)\s*[:：]\s*(.+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    for m in matches:
        projects.append(m.strip())
    return projects


# ==================== 自测代码 ====================
if __name__ == "__main__":
    sample_text = """
    吉伟翔
    电话：15102303275 | 邮箱：2669520581@qq.com
    重庆科技大学 智能科学与技术专业
    技能：Python, PyTorch, OpenCV, FastAPI
    项目：
    项目名称：家乡宣传网页
    项目名称：数据可视化仪表盘
    """
    result = parse_resume(sample_text)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))