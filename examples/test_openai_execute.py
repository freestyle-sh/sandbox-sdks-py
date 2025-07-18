import os
import openai
import freestyle.openai


(definition, runner) = freestyle.openai.execute_tool(
    os.environ.get("FREESTYLE_API_KEY"),
    freestyle.FreestyleExecuteScriptParamsConfiguration(
        nodeModules={"mathjs": "14.3.1"},
    ),
)

query = "What is the sum of every number from 50 to 65 divided by 17"
messages = [{"role": "user", "content": query}]
print("Question: ", query)
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

res = client.chat.completions.create(
    model="gpt-4-turbo", messages=messages, tools=[definition]
)


result = runner(res.choices[0].message)

messages.append(res.choices[0].message)
if len(result) > 0:
    messages.extend(result)

res = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=messages,
    tools=[definition],
)

print("Answer: ", res.choices[0].message.content)
