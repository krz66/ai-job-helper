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
你是专业简历解析助手，请从简历中提取完整信息。
要求：
1. 只输出纯文本，不要任何格式、符号、Markdown
2. 分模块清晰输出，每个模块单独成行
3. 信息完整不省略
4. 不要多余空行，不要多余符号，自动换行

简历：
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
你是专业简历优化师，请对简历进行专业润色。
要求：
1. 只输出纯文本，不要任何格式、符号、Markdown
2. 语言更专业、简洁、有说服力
3. 不改变原意，不编造信息
4. 分段清晰，自动换行

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
你是求职匹配专家，根据简历与岗位JD进行匹配分析。
要求：
1. 只输出纯文本，不要任何格式、符号、Markdown
2. 输出：匹配分数、优势、不足、改进建议
3. 内容详细、实用、条理清晰
4. 自动换行，不分多余空行

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
你是专业求职顾问，请详细回答用户的求职问题。
要求：
1. 只输出纯文本，不要任何格式、符号、Markdown
2. 回答专业、详细、有条理
3. 自动换行，排版整洁

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