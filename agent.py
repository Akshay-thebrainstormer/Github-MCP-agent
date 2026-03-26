import asyncio
import os
from textwrap import dedent
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.mcp import MCPTools
from mcp import StdioServerParameters


async def run_github_agent(message):

    if not os.getenv("GITHUB_TOKEN"):
        return "Error: GitHub token not provided"

    if not os.getenv("OPENAI_API_KEY"):
        return "Error: OpenAI API key not provided"

    try:
        server_params = StdioServerParameters(
            command="docker",
            args=[
                "run", "-i", "--rm",
                "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
                "-e", "GITHUB_TOOLSETS",
                "ghcr.io/github/github-mcp-server"
            ],
            env={
                **os.environ,
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN"),
                "GITHUB_TOOLSETS": "repos,issues,pull_requests"
            }
        )

        async with MCPTools(server_params=server_params) as mcp_tools:

            agent = Agent(
                tools=[mcp_tools],
                instructions=dedent("""
                You are a GitHub assistant.
                Help users explore repositories and activity.
                Use markdown formatting and provide insights.
                """),
                markdown=True
            )

            response: RunOutput = await asyncio.wait_for(
                agent.arun(message), timeout=120.0
            )

            return response.content

    except asyncio.TimeoutError:
        return "Error: Request timed out"
    except Exception as e:
        return f"Error: {str(e)}"