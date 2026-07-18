# Resume Copilot

> 基于 FastAPI + DeepSeek 的 AI 简历分析助手

## 项目简介

Resume Copilot 是基于 AI 驱动的简历分析系统。

用户上传 PDF 简历后，系统自动完成：

- PDF 文本提取
- 简历结构化解析
- AI 综合评分
- 四维能力分析
- 优势、不足与改进建议生成

整个流程无需人工参与，实现完整的 AI 简历分析。

---

## 功能展示

PDF 上传

PDF 文本解析（PyMuPDF）

简历信息结构化

DeepSeek AI 分析

四维评分

- 技术能力
- 项目质量
- 岗位匹配度
- 简历完整度

AI 改进建议

---

## 技术栈

### 后端

- Python 3.11
- FastAPI
- Jinja2
- Pydantic

### AI

- DeepSeek API
- Prompt Engineering

### PDF

- PyMuPDF

### 前端

- HTML
- CSS
- JavaScript

---

## 项目结构

```text
resume-copilot/
│
├── app/
│   ├── routers/
│   ├── services/
│   ├── prompts/
│   ├── schemas/
│   └── main.py
│
├── templates/
├── static/
├── uploads/
│
├── requirements.txt
└── README.md
```

---

## 快速开始

### 克隆项目

```bash
git clone https://github.com/hmjcq/resume-copilot.git
```

### 创建虚拟环境

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

Linux：

```bash
source .venv/bin/activate
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env`

```text
OPENAI_API_KEY=你的API_KEY
OPENAI_BASE_URL=https://api.deepseek.com/v1
```

### 启动

```bash
uvicorn app.main:app --reload
```

浏览器访问：

```
http://127.0.0.1:8000
```

---

## 项目截图

（这里后面放截图）

---

## 后续规划

- [ ] JD 岗位匹配
- [ ] ATS 自动评分
- [ ] AI 简历优化
- [ ] 模拟技术面试
- [ ] Docker 部署

---

## License

MIT