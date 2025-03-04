import freestyle
import os
from freestyle.pipecat import *

client = freestyle.Freestyle(
  os.environ.get("FREESTYLE_API_KEY"),
  os.environ.get("FREESTYLE_API_BASE_URL")
)

print("API Key:", client.token)
print("Base URL:", client.baseUrl)
try:
  a = client.executeScript(
  """
  import { loadPyodide } from "pyodide";


export default async () => {
  await loadPyodide()
  return process.env.HELLO;
};
  """,
  freestyle.FreestyleExecuteScriptParamsConfiguration(
    env_vars={
      "HELLO": "WORLD"
    },
    node_modules={
      "pyodide": "0.27.3"
    }
  )
  )

  print("VALUES", a)
except Exception as e:
  print(e)
