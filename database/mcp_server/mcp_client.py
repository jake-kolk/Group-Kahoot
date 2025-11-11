import asyncio
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from dotenv import load_dotenv
from llama_ccp import Llama
import os

MODEL_PATH = "./tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llama = Llama(model_path=MODEL_PATH, temperature=TEMPERATURE, max_tokens=MAX_TOKENS)

    async def connect_to_server(self, server_script_path: str):
        """Connect to MCP server
        
        Args:
            server_script_path: Path to server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print(f"Connected to MCP server with tools: {tools}")

    async def process_query(self, query: str) -> str:
        """Process a query using the MCP server
        
        Args:
            query: The input query string
        
        Returns:
            The response from the MCP server
        """
        messages = [
            {"role": "user", "content": query}
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        response = self.llama(messages, tools=available_tools, temperature=TEMPERATURE)

        final_text = []

        assistant_message_content = []
        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                response = self.llama(messages, tools=available_tools, temperature=TEMPERATURE)

                final_text.append(response.content[0].text)

        return "\n".join(final_text)
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.exit_stack.aclose()

        
async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <path_to_mcp_server_script>")
        sys.exit(1)
    
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])

    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())