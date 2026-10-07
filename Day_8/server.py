from datetime import datetime, timezone, timedelta
from fastmcp import FastMCP
import random
import secrets,string

mcp = FastMCP(
    "Time Server"
)

@mcp.tool()
def current_time():
    """Return the current date and time."""
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S")

@mcp.tool()
def roll_dice():
    """Roll a six-sided die."""
    return random.randint(1, 6)

@mcp.tool()
def generate_password(length: int = 12):
    """Generate a secure password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("starting MCP server...")
    mcp.run()

