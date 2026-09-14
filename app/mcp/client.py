import anyio

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client


server = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp.server"]
)


async def call_tool(tool_name, arguments):

    async with stdio_client(server) as transport:

        async with Client(transport) as client:

            result = await client.call_tool(
                tool_name,
                arguments
            )

            return result


async def main():

    result = await call_tool(
        "calculate_risk",
        {
            "application": {
                "age": 35,
                "income": 800000,
                "credit_score": 720
            }
        }
    )

    print(result)


if __name__ == "__main__":
    anyio.run(main)