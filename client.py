import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Tell the client how to start and connect to the server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize the connection
            await session.initialize()
            
            # Discover what tools the server has
            tools = await session.list_tools()
            print("=== Connected to Consulting Toolkit ===")
            print(f"Available tools: {[tool.name for tool in tools.tools]}\n")
            
            # Get input from the user
            print("Paste your text below. When done, type END on a new line and press Enter.\n")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            
            user_text = "\n".join(lines)
            
            if not user_text.strip():
                print("No text provided. Exiting.")
                return
            
            # Call the summarize_text tool on the server
            print("\nAnalyzing...\n")
            result = await session.call_tool(
                "summarize_text",
                arguments={"text": user_text}
            )
            
            print("=== CONSULTING SUMMARY ===\n")
            print(result.content[0].text)
            print("\n=== END OF SUMMARY ===")

if __name__ == "__main__":
    asyncio.run(main())