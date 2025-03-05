from _openapi_client.models.freestyle_execute_script_params_configuration import (
    FreestyleExecuteScriptParamsConfiguration,
)
from freestyle.client import Freestyle

EXECUTE_TOOL_NAME = "executeCode"


async def executeTool(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> callable:
    freestyle = Freestyle(apiKey)

    async def toolExecutor(
        function_name, tool_call_id, args, llm, context, result_callback
    ):
        if function_name == "executeCode":
            script = args["script"]
            execution = freestyle.executeScript(script, params)
            result_callback(execution.to_json())
        else:
            result_callback(None)

    return toolExecutor
