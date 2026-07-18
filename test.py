# test.py
"""
简历分析测试脚本
不依赖 Web 服务，直接测试分析流程。
运行: python test.py
"""

from app.services.resume_analyzer import analyze_resume

# 模拟一份结构化简历数据
resume = {
    "name": "吉伟翔",
    "phone": "15102303275",
    "email": "2669520581@qq.com",
    "school": "重庆科技大学",
    "major": "智能科学与技术",
    "skills": ["Python", "PyTorch", "OpenCV"],
    "projects": ["家乡宣传网页", "数据可视化仪表盘"]
}

if __name__ == "__main__":
    try:
        result = analyze_resume(resume)
        print("✅ 分析完成！结果如下：\n")
        print(result)
    except Exception as e:
        print(f"❌ 分析失败: {e}")