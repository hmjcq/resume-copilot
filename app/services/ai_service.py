"""
AI 服务模块
提供 ask_ai() 函数，发送 prompt 字符串并返回模型回复。
"""

from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

# 全局客户端，整个项目复用
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def ask_ai(prompt: str) -> str:
    """
    向 AI 发送 prompt 字符串，返回模型的文本回复。

    参数:
        prompt: 完整的提示词字符串（已包含角色设定、格式要求等）。

    返回:
        str: 模型生成的回复文本。
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()


# ================== 自测代码 ==================
if __name__ == "__main__":
    test_prompt = "请用一句话介绍你自己。"
    try:
        reply = ask_ai(test_prompt)
        print("✅ AI 回复：", reply)
    except Exception as e:
        print(f"❌ 调用失败: {e}")