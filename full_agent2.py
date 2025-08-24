from google import genai
from google.genai.types import Content, Part
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
client = genai.Client()


def get_response_text(response):
    """Safely extract text from a Gemini response."""
    if not response or not response.candidates:
        return ""
    cand = response.candidates[0]
    if cand.content and cand.content.parts:
        return cand.content.parts[0].text or ""
    return ""

def safe_json_loads(s: str):
    """Parse JSON safely, handle empty/double-encoded cases."""
    if not s or not s.strip():
        return {}
    try:
        obj = json.loads(s)
        if isinstance(obj, str):  # double encoded JSON
            obj = json.loads(obj)
        return obj
    except Exception as e:
        print("⚠️ JSON parse error:", e)
        print("Raw string was:", s)
        return {}


def get_weather(city: str):
    url=f"http://wttr.in/{city}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
       return f"the weather in{city} is{response.text}" 
    return "something went wrong"

def run_command(command):
    result=os.system(command=command)
    return result



available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "takes a city name for input and returns the current weather for the city"
    },
    "run_command":{
        "fn":run_command,
         "description": "takes a command as input andperform the opeation "

    }
}


system_prompt = """
You are a helpful AI assistant specialized in tool-using agents.
You must always follow the reasoning steps: plan → action → observe → output.
For each step, return exactly ONE JSON object.

RULES:
1. Return ONLY valid JSON. 
   - No explanations, no prose, no Markdown, no natural language.
   - Keys and strings MUST use double quotes.
2. Only one JSON object per response.
3. Perform exactly one step at a time.
4. Always follow this schema:

{
  "step": "string",
  "content": "string (if step is plan or output)",
  "function": "string (only if step is action)",
  "input": "string (only if step is action)",
  "output": "string (only if step is observe)"
}

Example sequence for query "What is the weather of New York?":
{"step": "plan", "content": "The user is asking about weather of New York."}
{"step": "plan", "content": "From the available tools, I should call get_weather."}
{"step": "action", "function": "get_weather", "input": "New York"}
{"step": "observe", "output": "12 degree Celsius"}
{"step": "output", "content": "The weather in New York is 12 degree Celsius."}

Available tools:
- get_weather: takes a city name and returns the current weather for the city.
- run_command:  takes a command as input andperform the opeation 
"""



contents = [Content(role="user", parts=[Part(text=system_prompt)])]

query = input("> ")
contents.append(Content(role="user", parts=[Part(text=query)]))


while True:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    raw_text = get_response_text(response)
    print("DEBUG raw_text:", repr(raw_text))

   
    if not raw_text.strip().startswith("{"):
        # print("⚠️ Model returned prose instead of JSON. Re-prompting...")
        contents.append(Content(role="user", parts=[Part(text="Please respond ONLY with valid JSON according to the schema.")]))
        continue

    parsed_response = safe_json_loads(raw_text)
    if not parsed_response:
        contents.append(Content(role="user", parts=[Part(text="Please respond with valid JSON only.")]))
        continue

    contents.append(Content(role="model", parts=[Part(text=json.dumps(parsed_response))]))


    step = parsed_response.get("step")

    if step == "plan":
        print(parsed_response.get("content"))
        continue

    if step == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")
        if available_tools.get(tool_name):
            output = available_tools[tool_name]["fn"](tool_input)
            contents.append(
                Content(role="model", parts=[Part(text=json.dumps({"step": "observe", "output": output}))])
            )
        continue

    if step == "observe":
        print("Observation:", parsed_response.get("output"))
        continue

    if step == "output":
        print(parsed_response.get("content"))
        break
