﻿
# WeatherAPI MCP Server

This repository provides a custom implementation of a Model Context Protocol (MCP) server for interacting with [WeatherAPI](https://www.weatherapi.com/). By converting the API endpoints into callable tools, you can integrate real-time weather functionalities into GitHub Copilot Chat or other MCP-compatible platforms using the VS Code MCP extension.

## Overview

Model Context Protocol (MCP) is an open specification that allows developers to extend language models like GitHub Copilot by connecting them with real-time external tools via APIs. With MCP, you can register your own tools and allow the model to call them as needed.

This project turns the [WeatherAPI](https://www.weatherapi.com/) endpoints into MCP-compatible tools that can:

- Get current weather conditions
- Get daily weather forecasts
- Get historical weather data
- Get astronomy details (sunrise, sunset, moon phase)
- Get weather alerts

---

## Features

- **Live Integration**: Connects real-time weather data to Copilot Chat.
- **5 Custom Tools**: Each WeatherAPI function is exposed as a distinct MCP tool.
- **FastAPI Server**: Powered by `fastmcp.FastMCP` for asynchronous support.

---

## How to Use

### 1. Setup `mcp.json`

```json
{
  "inputs": [],
  "servers": {
    "weatherapi-server": {
      "command": "python",
      "args": ["weather_mcp_server.py"],
      "env": {
        "WEATHER_API_KEY": "your_weather_api_key"
      }
    }
  }
}
```

### 2. Install Dependencies

Ensure you have Python 3.8+ and install required libraries:

```bash
pip install fastmcp httpx
```

### 3. Run the Server

```bash
python weather_mcp_server.py
```

### 4. Enable in VS Code

- Open the Command Palette and choose: `Model Context: Select Tools`
- Check `MCP Server: weatherapi-server` and the listed tools

---

## Tools Description

| Tool Name             | Description                                         |
|----------------------|-----------------------------------------------------|
| `get_current_weather`| Fetch current weather for a given location          |
| `get_forecast`       | Get a multi-day weather forecast                    |
| `get_historical_weather` | Retrieve past weather data for a given date      |
| `get_astronomy`      | Return sunrise, sunset, and moon phase data         |
| `get_weather_alerts` | Display real-time alerts for severe weather         |

---

## Example
![image](https://github.com/user-attachments/assets/fb1bc9a4-2d5d-4ca8-9edc-28a418436a97)


## Why Model Context Protocol?

MCP is revolutionizing AI by allowing language models to:
- Access up-to-date external information
- Perform actions beyond natural language (like APIs, calculations, automation)
- Improve user workflows without leaving your editor

In this project, MCP bridges GitHub Copilot and WeatherAPI, letting developers and data scientists access meteorological data without ever leaving their coding environment.

---

## License

This project is open source under the MIT License.
