import os
import asyncio
import requests
from multi_agent_orchestrator.orchestrator import MultiAgentOrchestrator
from multi_agent_orchestrator.agents import BaseAgent, AgentOptions

# Define AQI Agent
class AQIMonitorAgent(BaseAgent):
    def __init__(self, options: AgentOptions):
        super().__init__(options)
        self.api_key = os.getenv('AQI_API_KEY')  # Make sure to set your AQI API key as an environment variable
        self.endpoint = "http://api.openweathermap.org/data/2.5/air_pollution"

    async def process_request(self, user_input: str, user_id: str, session_id: str):
        if "aqi" in user_input.lower():
            return await self.get_aqi(user_input)
        else:
            return {"content": "Sorry, I can only provide AQI information."}

    async def get_aqi(self, location: str):
        if "nyc" in location.lower():
            lat, lon = 40.7128, -74.0060  # Coordinates for NYC
        elif "long island" in location.lower():
            lat, lon = 40.789142, -73.13496  # Coordinates for Long Island
        else:
            return {"content": "Please specify either NYC or Long Island."}

        # Fetch AQI data
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        response = requests.get(self.endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            aqi = data['list'][0]['main']['aqi']
            return {"content": f"The current AQI for {location.title()} is {aqi}."}
        else:
            return {"content": "Failed to retrieve AQI data. Please try again later."}

# Set up orchestrator and add the AQI Agent
orchestrator = MultiAgentOrchestrator()

aqi_agent = AQIMonitorAgent(AgentOptions(
    name="AQI Monitor Agent",
    description="Monitors the Air Quality Index (AQI) for NYC and Long Island."
))

orchestrator.add_agent(aqi_agent)

# Example usage
async def main():
    response = await orchestrator.route_request("What's the AQI in NYC?", 'user123', 'session456')
    print(response["content"])

if __name__ == "__main__":
    asyncio.run(main())