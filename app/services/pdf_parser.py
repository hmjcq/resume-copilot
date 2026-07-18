"""
PDF 文本提取模块
提供 extract_text() 函数，用于从 PDF 文件中提取纯文本。
支持文件路径和二进制数据两种输入方式。
"""

import io
from pathlib import Path
from typing import Union

import pdfplumber


def extract_text(file_input: Union[str, Path, bytes]) -> str:
    """
    从 PDF 中提取全部文本内容。

    参数:
        file_input:
            - str / Path : PDF 文件路径
            - bytes       : PDF 文件的二进制数据（如 FastAPI UploadFile 读取的内容）

    返回:
        str: 提取出的所有页面文本，页与页之间用换行符分隔。

    异常:
        FileNotFoundError: 文件路径不存在时抛出。
        ValueError: 输入类型无效或 PDF 无法解析时抛出。
    """
    # 1. 统一处理输入类型
    if isinstance(file_input, (str, Path)):
        pdf_path = Path(file_input)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
        pdf_file = pdfplumber.open(str(pdf_path))
    elif isinstance(file_input, bytes):
        pdf_file = pdfplumber.open(io.BytesIO(file_input))
    else:
        raise ValueError("file_input 必须是文件路径(str/Path)或二进制数据(bytes)")

    # 2. 逐页提取文本
    all_text = []
    try:
        for page in pdf_file.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    except Exception as e:
        raise ValueError(f"PDF 解析失败: {e}")
    finally:
        pdf_file.close()

    return "\n".join(all_text)


# ========== 简单自测（直接运行此文件时生效） ==========
if __name__ == "__main__":
    import sys

    # 测试1：通过命令行参数传入 PDF 路径
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        try:
            text = extract_text(pdf_path)
            print("✅ 提取成功！文本内容：\n")
            print(text)
        except Exception as e:
            print(f"❌ 提取失败: {e}")
    else:
        # 测试2：如果没有参数，尝试在 uploads 文件夹里找 resume.pdf
        base_dir = Path(__file__).resolve().parent.parent.parent  # resume-copilot 根目录
        sample_pdf = base_dir / "uploads" / "resume.pdf"
        if sample_pdf.exists():
            try:
                text = extract_text(sample_pdf)
                print(f"✅ 已自动找到并提取 {sample_pdf}\n")
                print(text)
            except Exception as e:
                print(f"❌ 提取失败: {e}")
        else:
            print("ℹ️  使用方法：")
            print(f"   python {__file__} 路径/到/你的简历.pdf")
            print("   或者将 resume.pdf 放到 uploads/ 文件夹后直接运行本脚本")