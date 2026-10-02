from fastmcp import Client
async def connect():
    """
    Connect to the MCP Serverl
    """

    client = Client("server.py")
    # This starts the server behind the scenes, also establishes communication using the MCP portocol
    await client.__aenter__()
    print("Connected to MCP Server")
    # Return the client object because every future operation will use this same connection
    return client

async def disconnect(client):
    """
    close the MCP connection  
    """
    await client.__aexit__(
    None,
    None,
    None)

async def discover_tools(client):
    """
    Retrive all the tools available in the server
    """
    tools = await client.list_tools()
    return tools

async def execute_tool(
    client,
    tool_name,
    argument = None
):
    """Execute a tool"""
    if argument is None:
        arguments = {}
    else:
        arguments = argument
    result = await client.call_tool(tool_name, arguments)
    return result