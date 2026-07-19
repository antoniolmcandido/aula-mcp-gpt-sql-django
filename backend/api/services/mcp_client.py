import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def execute_tool_async(function_name: str, function_args: dict):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "api.services.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(function_name, function_args)

            if not result.content:
                return ""

            partes = []
            for item in result.content:
                texto = getattr(item, "text", None)
                if texto:
                    partes.append(texto)

            return "".join(partes)


def execute_tool(function_name: str, function_args: dict):
    return asyncio.run(execute_tool_async(function_name, function_args))
