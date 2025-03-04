from _openapi_client import *

class Freestyle:
  def __init__(self, token: str, baseUrl: str = "https://api.freestyle.sh"):
    self.token = token
    self.baseUrl = baseUrl

  def _client(self):
    configuration = Configuration()
    configuration.host = self.baseUrl

    client =  ApiClient(configuration)
    client.set_default_header("Authorization", f"Bearer {self.token}")
    return client

  def executeScript(self, code: str, nodeModules: dict[str, str] = {}):
    api = ExecuteApi(self._client())
    return api.handle_execute_script(FreestyleExecuteScriptParams(
      script=code,
      config=FreestyleExecuteScriptParamsConfiguration(nodeModules=nodeModules),
    ))
