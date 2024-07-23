import asyncio
import math
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.tools.tool_registry import register_tool


# 使用装饰器注册工具
# “math”的tag用于将工具分类为数学工具，include_functions 参数用于指定要包含的函数。这有利于`DataInterpreter`选择并理解工具
@register_tool(
    tags=["math"],
    include_functions=[
        "__init__",
        "add",
        "subtract",
        "multiply",
        "divide",
        "factorial",
    ],
)
class Calculator:
    """
    一个简单的计算器工具，可以执行基本的算术运算并计算阶乘。
    """

    @staticmethod
    def add(a, b):
        """
        计算两个数的和。
        """
        return a + b

    @staticmethod
    def subtract(a, b):
        """
        计算两个数的差。
        """
        return a - b

    @staticmethod
    def multiply(a, b):
        """
        计算两个数的乘积。
        """
        return a * b

    @staticmethod
    def divide(a, b):
        """
        计算两个数的商。
        """
        if b == 0:
            return "错误：除数不能为零"
        else:
            return a / b

    @staticmethod
    def factorial(n):
        """
        计算非负整数的阶乘。
        """
        if n < 0:
            raise ValueError("输入必须是非负整数")
        return math.factorial(n)


async def main(requirement: str):
    role = DataInterpreter(tools=["Calculator"])  # 集成工具
    await role.run(requirement)


if __name__ == "__main__":
    requirement = "请计算 3 和 11 的和，然后计算 5 的阶乘"
    asyncio.run(main(requirement))
