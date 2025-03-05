from langchain_core.tools import tool

from _openapi_client.models.freestyle_execute_script_params_configuration import (
    FreestyleExecuteScriptParamsConfiguration,
)
from freestyle.client import Freestyle


def executeTool(apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None):
    freestyle = Freestyle(apiKey)

    @tool
    def toolExecutor(
        script: str,
    ):
        return freestyle.executeScript(script, params).to_json()

    return toolExecutor
