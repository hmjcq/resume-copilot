# app/config.py
import os
from dotenv import load_dotenv

# 加载项目根目录的 .env 文件
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")

if not OPENAI_API_KEY:
    raise ValueError("缺少 OPENAI_API_KEY，请在 .env 文件中配置")