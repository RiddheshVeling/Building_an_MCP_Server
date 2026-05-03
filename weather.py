import os
import requests
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

#Loading environment variables from .env file
load_dotenv()

#Initializing FastMCP server
mcp = FastMCP()

#Getting OpenWeatherMap API key and URL from environment variables
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPM_WEATHER_URL = os.getenv("OPM_WEATHER_URL")

@mcp.tool()
##Define weather retrieval tool function
def get_weather(city: str) -> str:
    """
    Fetch the current weather from OpenWeatherMap API for a given city.
    """
    try:
        ##url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric",
        }
        response = requests.get(OPM_WEATHER_URL, params=params)
        data = response.json()

        if response.status_code != 200 or "weather" not in data:
            return f"⚠️ Could not fetch weather for '{city}'."

        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        location = data["name"]
        return f"📍 {location}: {desc}, {temp}°C"

    except Exception as e:
        return f"❌ Error fetching weather: {str(e)}"
    
if __name__ == "__main__":
    #Initialize and run the MCP server
    mcp.run(transport='stdio')     ##Stido is useful for communication between the MCP server and the client (like a chatbot interface) through standard input and output streams(CLI or terminal).