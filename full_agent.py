from google import genai
from google.genai.types import Content,Part
from dotenv import load_dotenv
import json

load_dotenv()
client = genai.Client()

def get_weather(city:str):
    return "31"

available_tools={
   "get_weather":{
      "fn":get_weather,
      "description":"takes a city name for input and returns the current weather for the city"
   }
}

system_prompt="""
 You are a helpful AI assistant specialized in tool-using agents.

You must always follow the reasoning steps: plan → action → observe → output.  
For each step, return exactly ONE JSON object.  

⚠️ RULES (must follow strictly):
1. Output ONLY valid JSON. 
   - No explanations, no extra text, no Markdown, no natural language.
   - Keys and string values MUST be wrapped in double quotes.
   - Do not include backticks, comments, or "output{{ }}" wrappers.
2. Only one JSON object per response.
3. Perform exactly one step at a time.
4. Always follow the schema:

{
  "step": "string",
  "content": "string (if step is plan or output)",
  "function": "string (only if step is action)",
  "input": "string (only if step is action)",
  "output": "string (only if step is observe)"
}

---

### Example:

User query: "What is the weather of New York?"

Response sequence (step by step):

{"step": "plan", "content": "The user is asking about weather of New York."}
{"step": "plan", "content": "From the available tools, I should call get_weather."}
{"step": "action", "function": "get_weather", "input": "New York"}
{"step": "observe", "output": "12 degree Celsius"}
{"step": "output", "content": "The weather in New York is 12 degree Celsius."}

---

### Available tools:
- get_weather: takes a city name and returns the current weather for the city.

"""
contents = [
    Content(role="user", parts=[Part(text=system_prompt)])
]

query = input("> ")

# Add user query
contents.append(
    Content(role="user", parts=[Part(text=query)])
)

while True:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    raw_text= response.candidates[0].content.parts[0].text
   
    parsed_response = json.loads(raw_text)



    # Save assistant reply
    contents.append(
        Content(role="model", parts=[Part(text=json.dumps(parsed_response))])
    )
    


    if parsed_response.get("step") == "plan":
      
      print(parsed_response.get("content"))
      continue

    if parsed_response.get("step") == "action":
       tool_name=parsed_response.get("function")
       tool_input=parsed_response.get("input")

       if available_tools.get(tool_name,False)!=False:
          output=available_tools[tool_name].get("fn")(tool_input)# simple fn calling with ()
          contents.append(
                  Content(role="model", parts=[Part(text=json.dumps({"step":"observe","output":output}))])
                  )
          continue
       
    if parsed_response.get("step") == "action":
       print(parsed_response.get("content"))
    

    
      
















# response=client.models.generate_content(
#         model="gemini-2.5-flash", contents=[
#         Content(role="user", parts=[Part(text=system_prompt)]),# we cant use role=sytem bcs google gemini doesnt allow it  
#         Content(role="user", parts=[Part(text="what is the current weather of Patiala?")]),
         
#          Content(role="user", parts=[Part(text=json.dumps({
#   "step": "plan",
#   "content": "The user is asking for the current weather of Patiala. I should use a tool to get weather information."
# }))]),
#            Content(role="user", parts=[Part(text=json.dumps({"step": "plan", "content": "From the available tools, I should call a function that can provide weather information. Assuming 'get_weather' is the appropriate function for this task."} ))]),
#          ]
#       ) 
# print(response.text)

# this is doing step by step calling model without automating.



















