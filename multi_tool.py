import requests

def call_weather_api(location):
    try:
        response = requests.get(f"https://api.example.com/weather?location={location}")
        return f"Weather in {location}: {response.json()['weather']}."
    except Exception as e:
        return f"Could not retrieve weather data: {e}"

def external_tool(question):
    if "weather" in question.lower():
        location = question.split("in")[-1].strip()
        return call_weather_api(location)
    return None

def multi_tool_mode(question):
    external_response = external_tool(question)
    if external_response:
        print(f"External Response: {external_response}")
        return True
    return False