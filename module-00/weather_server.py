# Create an MCP server
from fastmcp import FastMCP
import random

# Dictionary to store known weather data for cities
known_weather_data = {'Copenhagen': 20.0}

# Create an MCP server instance with the name "Demo 🚀"
mcp = FastMCP("Demo 🚀")

# Register get_weather as an MCP tool
@mcp.tool
def get_weather(city: str) -> float:
    """
    Retrieves the temperature for a specified city.
    Parameters:
        city (str): The name of the city for which to retrieve weather data.
    Returns:
        float: The temperature associated with the city.
    """
    city = city.strip().lower() # Normalize city name
    if city in known_weather_data:
        return known_weather_data[city] # Return known temperature if available
    return round(random.uniform(-5, 35), 1) # Otherwise, return a random temperature

# Register set_weather as an MCP tool
@mcp.tool
def set_weather(city: str, temp: float) -> str:
    """
    Sets the temperature for a specified city.
    Parameters:
        city (str): The name of the city for which to set the weather data.
        temp (float): The temperature to associate with the city.
    Returns:
        str: A confirmation string 'OK' indicating successful update.
    """
    city = city.strip().lower()         # Normalize city name
    known_weather_data[city] = temp     # Update the temperature in the dictionary
    return 'OK'                         # Return confirmation

if __name__ == "__main__":
    # Start the MCP server (default transport is stdio)
    mcp.run()