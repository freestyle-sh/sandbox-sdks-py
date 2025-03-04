import freestyle

from freestyle.pipecat import *


client = freestyle.Freestyle(
  "NuoZujN7MV6PF4qxw3kGDP-ENachqAf9jw56pJDysiY1squRxSzg9GMTqgUzehgsQti",
  "http://localhost:8080"
)

print("API Key:", client.token)
print("Base URL:", client.baseUrl)
try:
  a = client.executeScript(
  """
  import { loadPyodide } from "pyodide";


export default async () => {
  try {
  const pyodide = await loadPyodide();



  console.log(output);
  } catch (e) {

  console.error(e);
    return e.toString();
  }

  return 0;
};
  """,
  {
    "pyodide": "0.27.3"
  }
  )

  print("VALUES", a)
except Exception as e:
  print(e)
