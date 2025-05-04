import os
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Initialize MCP server
mcp = FastMCP("weatherapi")

# WeatherAPI base URL and API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "xxx")
BASE_URL = "https://api.weatherapi.com/v1"

async def make_weatherapi_request(endpoint: str, params: dict) -> dict:
    """Make authenticated requests to WeatherAPI."""
    params['key'] = WEATHER_API_KEY
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/{endpoint}.json", params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API Error: {e.response.status_code} {e.response.text}")

@mcp.tool()
async def get_current_weather(location: str) -> dict:
    """Get current weather conditions."""
    params = {"q": location}
    data = await make_weatherapi_request("current", params)
    current = data["current"]
    return {
        "last_updated": current["last_updated"],
        "temp_c": current["temp_c"],
        "temp_f": current["temp_f"],
        "condition": current["condition"]["text"],
        "icon": current["condition"]["icon"],
        "wind_kph": current["wind_kph"],
        "humidity": current["humidity"],
        "uv_index": current["uv"]
    }

@mcp.tool()
async def get_forecast(location: str, days: int = 3) -> list:
    """Get daily weather forecast for specified days."""
    params = {"q": location, "days": days}
    data = await make_weatherapi_request("forecast", params)
    forecast_days = data["forecast"]["forecastday"]
    return [{
        "date": day["date"],
        "maxtemp_c": day["day"]["maxtemp_c"],
        "mintemp_c": day["day"]["mintemp_c"],
        "condition": day["day"]["condition"]["text"],
        "icon": day["day"]["condition"]["icon"],
        "uv_index": day["day"]["uv"]
    } for day in forecast_days]

@mcp.tool()
async def get_historical_weather(location: str, date: str) -> dict:
    """Get historical weather for a specific date."""
    params = {"q": location, "dt": date}
    data = await make_weatherapi_request("history", params)
    history_day = data["forecast"]["forecastday"][0]["day"]
    return {
        "date": date,
        "avgtemp_c": history_day["avgtemp_c"],
        "maxtemp_c": history_day["maxtemp_c"],
        "mintemp_c": history_day["mintemp_c"],
        "condition": history_day["condition"]["text"]
    }

@mcp.tool()
async def get_astronomy(location: str, date: str) -> dict:
    """Get astronomy details (sunrise, sunset, moon phase)."""
    params = {"q": location, "dt": date}
    data = await make_weatherapi_request("astronomy", params)
    astro = data["astronomy"]["astro"]
    return {
        "sunrise": astro["sunrise"],
        "sunset": astro["sunset"],
        "moonrise": astro["moonrise"],
        "moonset": astro["moonset"],
        "moon_phase": astro["moon_phase"]
    }

@mcp.tool()
async def get_weather_alerts(location: str) -> list:
    """Get weather alerts for a location."""
    params = {"q": location}
    data = await make_weatherapi_request("forecast", params)  # Alerts are included in the forecast endpoint
    alerts = data.get("alerts", {}).get("alert", [])
    return [{
        "headline": alert.get("headline"),
        "severity": alert.get("severity"),
        "description": alert.get("desc"),
        "effective_date": alert.get("effective"),
        "expires_date": alert.get("expires")
    } for alert in alerts]

if __name__ == "__main__":
    mcp.run()
