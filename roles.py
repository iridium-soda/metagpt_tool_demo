from metagpt.roles import Role
from metagpt.logs import logger
from metagpt.schema import Message
from metagpt.actions.add_requirement import UserRequirement
from metagpt.const import (
    MESSAGE_ROUTE_CAUSE_BY,
    MESSAGE_ROUTE_FROM,
    MESSAGE_ROUTE_TO,
    MESSAGE_ROUTE_TO_ALL,
    PRDS_FILE_REPO,
    SYSTEM_DESIGN_FILE_REPO,
    TASK_FILE_REPO,
    MESSAGE_ROUTE_TO_NONE,
)
from metagpt.roles.di.data_interpreter import DataInterpreter
from metagpt.tools.tool_recommend import BM25ToolRecommender, ToolRecommender
from actions import *
from utils import *


class Analyzer(DataInterpreter):
    name: str = "Alice"
    profile: str = "Analyzer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnalysisAndDecide])  # Only one action thus no _think required
        self._watch({UserRequirement})  # Assign to watch user's input as a main entry

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be AnalysisAndDecide()

        msg = self.get_memories(k=1)[0]  # find the most recent messages
        output = await todo.run(msg.content)
        msg = Message(
            content=output,
            role=self.profile,
            cause_by=type(todo),
            send_to=DataQueryOperator,
        )  # 这里做的是对的
        self.rc.env.publish_message(msg)  # Seng message to DataQueryOperator
        self.rc.memory.add(msg)  # Add msg to the latest memory
        return Message(content="dummy message", send_to=MESSAGE_ROUTE_TO_NONE)


class DataQueryOperator(DataInterpreter):
    name: str = "Sofia"
    profile: str = "DataQueryOperator"
    tools: list = ["query_fields", "query_data"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch({AnalysisAndDecide})  # Listen message from AnalysisAndDecide
        """
        if self.tools and not self.tool_recommender:
            self.tool_recommender = BM25ToolRecommender(tools=self.tools)
        """

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        output = await todo.run(msg.content)
        msg = Message(
            content=output,
            role=self.profile,
            cause_by=type(todo),
            send_to=ReportGenerator,
        )
        self.rc.env.publish_message(msg)  # Seng message to DataQueryOperator
        self.rc.memory.add(msg)

        return Message(content="dummy message", send_to=MESSAGE_ROUTE_TO_NONE)


class ReportGenerator(DataInterpreter):
    name: str = "Issa"
    profile: str = "ReportGenerator"
    tools: list = ["draw_picture"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnalysisData, WriteReport])
        self._watch({DataQueryOperator})  # Listen message from DataQueryOperator
        # self._set_react_mode("plan_and_act")  # use plan and act mode

    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # Select what act to run
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        output = await todo.run(msg.content)
        msg = Message(content=output, role=self.profile, cause_by=type(todo))

        return msg  # Finish the process
