from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MATH_SERVER")

@mcp.tool()
def add(a:int, b:int) -> int:
    """
add two numbers
    """
    return a+b

def multiply(a:int,b:int)-> int:
    """
    multiply two  numbers 
    """
