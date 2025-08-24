
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