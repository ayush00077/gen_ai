# from google import genai
# from dotenv import load_dotenv
# load_dotenv()
# import json


# client = genai.Client()

# system_prompt = """
# You are a helpful assistant.
# Always respond ONLY in strict JSON format with keys: step, content.

# Examples:
# User: What is 2+2?
# Assistant: {"step":"reasoning","content":"2+2=4"}

# User: What is the capital of France?
# Assistant: {"step":"output","content":"Paris"}

# Now continue in the same style.
# """


# contents = [
#     {"role": "system", "content": system_prompt}# try and understand that we give two things intiially one is system prompt and othe is our query always , thats basically few shot prompting
# ]

# query=input(">")

# contents.append({"role":"user","content":query})

# while True:
#     response=client.models.generate_content(
#         model="gemini-2.5-flash", contents=contents

#     )

#     parsed_response=json.loads(response.text)
#     contents.append({"role":"assistant","content":json.dumps(parsed_response)})

#     if parsed_response.get("step")!="output":
#         print(parsed_response.get("content"))
#         continue

#     print(parsed_response.get("content"))
#     break


from google import genai
from google.genai.types import Content, Part
from dotenv import load_dotenv
import json

load_dotenv()
client = genai.Client()

system_prompt = """
You are a helpful assistant.
Always respond ONLY in strict JSON format with keys: step, content.

Examples:
User: What is 2+2?
Assistant: {"step":"reasoning","content":"2+2=4"}

User: What is the capital of France?
Assistant: {"step":"output","content":"Paris"}

Now continue in the same style.
"""

# Put system prompt as first "user" message
contents = [
    Content(role="user", parts=[Part.from_text(text=system_prompt)])
]

query = input("> ")

# Add user query
contents.append(
    Content(role="user", parts=[Part.from_text(text=query)])
)

while True:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )

    parsed_response = json.loads(response.text)

    # Save assistant reply
    contents.append(
        Content(role="model", parts=[Part.from_text(text=response.text)])
    )

    print(parsed_response.get("content"))

    if parsed_response.get("step") == "output":
        break
