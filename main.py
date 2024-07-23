"""
main.py

This script provides a command-line interface (CLI) for fixing software vulnerabilities
using a team of AI agents. The script allows users to specify what to analysis and ask the LLM gives a detailed report with the given format.

Usage:
    python main.py [idea]
"""
import typer
import asyncio
from roles import *
from metagpt.logs import logger
from metagpt.team import Team

def app(idea:str):
    """Main entry of the app
    """
    logger.info(f"The idea is {idea}")
    
    team = Team()
    team.hire([Analyzer(),DataQueryOperator(),ReportGenerator()])

    team.invest(investment=100)

    async def run_team():
        """
        Run the AI team project asynchronously.
        """
        team.run_project(idea)
        await team.run(n_round=3,)
    
    asyncio.run(run_team())
    return 

    
if __name__=="__main__":
    typer.run(app)