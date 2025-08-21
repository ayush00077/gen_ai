from google import genai
from google.genai.types import Content, Part
from dotenv import load_dotenv
import json

load_dotenv()
client = genai.Client()

def get_weather(city:str):
    return "31"

system_prompt="""
  you are a helpful AI assistant who is specialised in resolving user query.
  you work on strat,plan , action and observe .
  for the given query and available tools plan the step by step  execution carefully.
  select the relevant tool from the available tools and based on tool selection perform an action to carefully wait for an observation 
  and based on the observation of the tool call resolve the user query

  RULES:
  1 follow the output JSON format.
  2. always perform one step at a time and wait for next input

output JSON format:
 {{
   "step":"string"
   " content":" string"
   "function":"the name of function if step is action "
   "input ":"the input parameter for the function"
 }}

  
  EXAMPLE:
  USER QUERY: what is the weather of new york
  output{{"step": "plan", "content":" the user is interested in weather data of new york"}}
  output{{"step": "plan", "content":" frm the available tools i should call get_weather"}}
  output{{"step": "action ", "function":" get_weather","input":" new york"}}
  output{{"step": "observe ", "output":"12 degree celcius"}}
  output{{"step": "output", "content":"the weather for patiala is 12 degree celcius"}}

"""


response=client.models.generate_content(
        model="gemini-2.5-flash", contents=[
        Content(role="user", parts=[Part(text=system_prompt)]),#we cant use role=sytem bcs google gemini doesnt allow it  
        Content(role="user", parts=[Part(text="what is the current weather of Patiala?")]),
         
         Content(role="user", parts=[Part(text=json.dumps({
  "step": "plan",
  "content": "The user is asking for the current weather of Patiala. I should use a tool to get weather information."
}))]),
           Content(role="user", parts=[Part(text=json.dumps({"step": "plan", "content": "From the available tools, I should call a function that can provide weather information. Assuming 'get_weather' is the appropriate function for this task."} ))]),
         ]
      ) 
print(response.text)

# this is doing step by step calling model without automating.



















