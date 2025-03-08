from _openapi_client.models.freestyle_execute_script_params_configuration import (
    FreestyleExecuteScriptParamsConfiguration,
)
from freestyle.client import Freestyle
from typing import Tuple, Callable
from freestyle.gemini import execute_tool_definition as gemini_execute_tool_definition
from freestyle.openai import execute_tool_definition as openai_execute_tool_definition

EXECUTE_TOOL_NAME = "executeCode"


def execute_tool_executor(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> Callable:
    freestyle = Freestyle(apiKey)

    async def toolExecutor(
        function_name, tool_call_id, args, llm, context, result_callback
    ):
        if function_name == "executeCode":
            script = args["script"]
            execution = freestyle.execute_script(script, params)
            await result_callback(execution.to_json())
        else:
            await result_callback(None)

    return toolExecutor


def execute_tool_gemini(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> Tuple[str, Callable]:
    return gemini_execute_tool_definition(params), execute_tool_executor(apiKey, params)


def execute_tool_openai(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> Tuple[str, Callable]:
    return openai_execute_tool_definition(params), execute_tool_executor(apiKey, params)
