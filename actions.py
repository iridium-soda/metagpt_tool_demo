import re
from metagpt.actions import Action
from metagpt.logs import logger


class AnalysisAndDecide(Action):
    """
    This action belongs to the role `analyzer` and  analysis the requirement from the user and decide what datas to get from the datafile.
    """

    name: str = "AnalysisAndDecide"
    PROMPT_TEMPLATE: str = """Analysis the request and decide what data need to be retrived to finish the following job:{instruction} Return a python list object contains which data need to be retrived to finish this job without any other texts.Your analysis and desicion:
        """

    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)

        code_text = AnalysisAndDecide.parser(rsp)

        return code_text

    @staticmethod
    def parser(input_string):
        # 正则表达式匹配方括号中的内容
        pattern = re.compile(r"\[([^\[\]]*)\]")

        # 查找所有匹配的列表字符串
        matches = pattern.findall(input_string)

        # 解析每个匹配的列表字符串
        parsed_lists = []
        for match in matches:
            # 将匹配的字符串按逗号分隔并去除空格
            elements = [element.strip() for element in match.split(",")]
            parsed_lists.append(elements)

        return parsed_lists

class AnalysisData(Action):
    """This action belongs to ReportGenerator and analysis data extract from the .csv file and give the analysis result
    """
    name:str="AnalysisData"
    PROMPT_TEMPLATE:str="""Analysis the data and give your conclusion about the question in the following:{instruction} then give your brief answer in points in a **bulleted** list start with `- ` without any other text.
    Your analysis result:
    """
    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)

        code_text = AnalysisAndDecide.parser(rsp)

        return code_text # A list of conclusions
    
    @staticmethod
    def parser(input_string):
        # 使用正则表达式匹配以*、-、•或者空格后的数字开头的行
        bullet_pattern = re.compile(r'(?:^\s*[\*\-\•]|\d+\.\s+)', re.MULTILINE)
        
        # 使用re.split将字符串拆分为各个列表项
        items = re.split(bullet_pattern, input_string)
        
        # 去除空字符串和首尾的空白字符
        items = [item.strip() for item in items if item.strip()]
        
        return items

class WriteReport(Action):
    """This action belongs to ReportGenerator and write formatted report with the given conclusions
    """
    name:str="WriteReport"
    PROMPT_TEMPLATE:str="""Referring conclusions and write a report about {instruction} with the given format. Your report should use MARKDOWN grammar and contains the following element:
    1. Describe the situation of the data
    2. Analysis about the trends
    3. What does the treand stands for
    4. Give your suggestion
    
    Your report in markdown without any other text:
    """
    async def run(self, instruction: str):
        prompt = self.PROMPT_TEMPLATE.format(instruction=instruction)
        rsp = await self._aask(prompt)

        code_text = AnalysisAndDecide.parser(rsp)

        return code_text # A list of conclusions