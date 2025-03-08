from langchain_core.tools import tool

from _openapi_client.models.freestyle_execute_script_params_configuration import (
    FreestyleExecuteScriptParamsConfiguration,
)
from freestyle.client import Freestyle


def execute_tool(apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None):
    freestyle = Freestyle(apiKey)

    @tool
    def tool_executor(
        script: str,
    ):
        return freestyle.execute_script(script, params).to_json()

    return tool_executor
