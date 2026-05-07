from mcp.server.fastmcp import FastMCP
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Create the MCP server and give it a name
mcp = FastMCP("Consulting Toolkit")

client = Anthropic()

@mcp.tool()
def summarize_text(text: str) -> str:
    """Takes a block of text and returns a structured consulting summary."""
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You are an expert management consultant. When given a block of text, 
        return a structured summary in the following format:

        SITUATION: One sentence describing the core context or problem.
        
        KEY FINDINGS: 3-5 bullet points of the most important insights.
        
        RISKS: 2-3 bullet points of the most significant risks or concerns.
        
        RECOMMENDED ACTIONS: 2-3 clear, prioritized action items.
        
        OPEN QUESTIONS: 1-2 questions that need to be answered to move forward.
        
        Be concise, specific, and direct.""",
        messages=[
            {"role": "user", "content": f"Please analyze the following text:\n\n{text}"}
        ]
    )
    
    return message.content[0].text

@mcp.tool()
def extract_action_items(text: str) -> str:
    """Extracts a numbered list of clear action items from a block of text."""
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You are an expert management consultant. When given a block of text, identify any action items and return a bulleted list of action items, ordered by priority. Be concise, specific, and use direct professional language. Do not use any buzzwords or jargon.""",
        messages=[
            {"role": "user", "content": f"Please extract action items from the following text:\n\n{text}"}
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    mcp.run(transport="stdio")
