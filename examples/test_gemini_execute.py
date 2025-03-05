import google.genai as genai
import os
import freestyle.gemini
from google.genai import types

client = genai.Client(api_key=os.environ.get("GENERATIVEAI_API_KEY"))


# model = genai.client.com("gemini-2.0-flash")
definition, runner = freestyle.gemini.executeTool(
    os.environ.get("FREESTYLE_API_KEY"),
)
chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfigDict(
        tools=[definition],
    ),
    history=[],
)

response = chat.send_message(
    "What is the sum of every number from 50 to 65 divided by 17"
).candidates[0]
tool_result = runner(response.content)

print("Answer: ", tool_result)
# runner(response)
