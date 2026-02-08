from openai import OpenAI
import os
import json
from src.mcp.server import mcp_server
from src.mcp.utils import registry
import src.mcp.tools

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful Todo AI Assistant. Your goal is to help users manage their tasks using natural language.
You have access to tools for adding, listing, updating, completing, and deleting tasks.
Always ask for clarification if a command is ambiguous (e.g., "Delete it" without context).
When a user wants to manage a task, use the appropriate tool.
You must always pass the 'user_id' provided in the context to every tool call.
"""

async def execute_agent(message: str, history: list, user_id: str):
    # Convert history to OpenAI message format
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append({"role": "assistant" if msg.role == "assistant" else "user", "content": msg.content})
    
    messages.append({"role": "user", "content": message})
    
    # This is a simplified version of the agent loop
    # In a real app with OpenAI Agents SDK, we'd use their higher-level abstractions
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": t['name'],
                    "description": t['description'],
                    "parameters": t['inputSchema']
                }
            } for t in registry.tools.values()
        ],
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    if assistant_message.tool_calls:
        # Execute tool calls
        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            args["user_id"] = user_id
            
            if name in registry.tool_implementations:
                func = registry.tool_implementations[name]
                success, result = func(**args)
            else:
                result = {"error": f"Unknown tool: {name}"}
            
            # Append tool result to messages and get final response
            messages.append(assistant_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": str(result)
            })
            
        final_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages
        )
        return final_response.choices[0].message.content, assistant_message.tool_calls
        
    return assistant_message.content, None