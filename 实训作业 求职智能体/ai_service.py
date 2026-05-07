from openai import OpenAI
from config import API_KEY, CHAT_MODEL

class AIAgent:
    def __init__(self, api_key, model):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = model
        self.default_resume = ""

    def set_default_resume(self, resume_text):
        self.default_resume = resume_text

    def get_default_resume(self):
        return self.default_resume

    def reset(self):
        pass

    def cancel_task(self):
        pass

    # 简历抽取（纯净文本，无格式无符号）
    def extract_resume(self, resume_text):
        prompt = f"""
从以下简历中完整提取所有信息，只输出纯文本内容，不要任何格式，不要符号，不要markdown。
必须包含：基本信息、教育背景、专业技能、实习经历、项目经历、荣誉奖项、证书资质、自我评价。

简历原文：
{resume_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.05,
            max_tokens=8192,
            stream=False
        )
        return response.choices[0].message.content

    # 简历润色（纯净文本）
    def polish_resume(self, resume_text):
        prompt = f"""
优化润色以下简历，只输出纯净文本，不要任何格式，不要符号，不要markdown。

{resume_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=8192,
            stream=False
        )
        return response.choices[0].message.content

    # 岗位匹配（纯净文本）
    def match_job(self, jd_text, resume_text=""):
        if not resume_text:
            resume_text = self.default_resume
        prompt = f"""
分析简历与岗位的匹配度，只输出纯净文本，不要任何格式，不要符号，不要markdown。
内容包含：匹配分数、匹配优势、不匹配点、改进建议。

简历：
{resume_text}

岗位JD：
{jd_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=8192,
            stream=False
        )
        return response.choices[0].message.content

    # 面试题生成（纯净文本，无格式）
    def gen_interview(self, info_text):
        prompt = f"""
根据信息生成10道面试题和详细答案，只输出纯文本，不要任何格式，不要符号，不要markdown。
每题单独一行，答案紧跟题目，分点清晰但不用任何符号。
输出格式：
题目1：[题目内容]
【详细答案】：
要点1：xxx
要点2：xxx
要点3：xxx
补充说明：xxx

题目2：[题目内容]
【详细答案】：
要点1：xxx
要点2：xxx
要点3：xxx
补充说明：xxx

以此类推，生成10道题。
信息：
{info_text}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=8192,
            stream=False
        )
        return response.choices[0].message.content

    # 智能问答（纯净文本）
    def qa_ask(self, question):
        prompt = f"""
详细回答以下问题，只输出纯文本，不要任何格式，不要符号，不要markdown。

问题：
{question}
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=8192,
            stream=False
        )
        return response.choices[0].message.content

ai_agent = AIAgent(api_key=API_KEY, model=CHAT_MODEL)