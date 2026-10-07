import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import os
from mcp_client import *

# Load configuration
load_dotenv()

# Create AI client
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Build Tool Descriptionns
def build_tool_descriptions(tools):
    descriptions = ""
    for tool in tools:
        descriptions += f"""
    Tool:
    {tool.name}
    Description:
    {tool.description}
    """
    return descriptions

# Planner
def planner(user_request, tools):
    tool_descriptions = build_tool_descriptions(
        tools
    )

# Then create a prompt by combining user input and tool description and give this prompt to model
    prompt = f"""
    You are an AI planner.
    Available Tools
    {tool_descriptions}
    Instructions
    1. Select the best tool.
    2. Reply ONLY with the tool name.
    3. Do not reply with anything else.
    User Request:
    {user_request}
    """

# Give prompt to model
    response = client.chat.completions.create(
        model= os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

# Model returns the tool name
    tool_name = response.choices[0].message.content
    return tool_name.strip()

def generate_response(user_request,tool_result):
    prompt = f"""
    The user asked: {user_request}
    The tool returned: {tool_result}
    Respond directly to the user in natural, conversational way.
    Use the tool result as the factual source.
    Transform raw tool output into a human-friendly answer.
    Do not simply copy raw values when a natural sentence would be better.
    Do not add information that is not needded to answer the request.
    Do not mention tools, internal processing, planning or reasoning.
    Keep the response concise.
    """
    response = client.chat.completions.create(
        model= os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content

async def main():
    # Step 1: connect to the MCP Server.
    client = await connect()
    # Step 2: discover the available tools.
    tools = await discover_tools(
        client
    )
    print()
    print("Available Tools")
    print("=================")
    for tool in tools:
        print(tool.name)
    print()

    # Step 3: Planner : Take the user input. create tool descriptions for each tool. Then crreate a prompt by combining user input and tool description and give this prompt to model
    user_request = input(
        "User: "
    )

    tool_name = planner(
        user_request,
        tools
    )
    print()
    print("Planner Selected Tool: ", tool_name)
    print()

    # Step 5: Execute the selected tool.
    tool_result = await execute_tool(
        client,
        tool_name
        )
    
    # Setp 6: Generate a natural language response based on the tool result.
    final_answer = generate_response(
        user_request,
        tool_result
    )
    print()
    print("Final Answer: ", final_answer)
    
    await disconnect(
        client
    )

if __name__ == "__main__":
    asyncio.run(main())

    