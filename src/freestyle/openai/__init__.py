from _openapi_client import FreestyleExecuteScriptParamsConfiguration
from openai.types.chat import (
    ChatCompletionToolParam,
    ChatCompletionToolMessageParam,
    ChatCompletionMessage,
)
from freestyle import Freestyle
from typing import Callable, Tuple
import json


def execute_tool(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> Tuple[
    ChatCompletionToolParam,
    Callable[[ChatCompletionMessage], list[ChatCompletionToolMessageParam] | None],
]:
    freestyle = Freestyle(apiKey)

    def codeExecutor(completion: ChatCompletionMessage):
        if any("executeCode" == t.function.name for t in completion.tool_calls):
            calls = [
                t for t in completion.tool_calls if t.function.name == "executeCode"
            ]
            if not calls:
                return None
            results = []
            for call in calls:
                script = json.loads(call.function.arguments)["script"]
                execution = freestyle.execute_script(script, params)
                results.append(
                    ChatCompletionToolMessageParam(
                        content=execution.to_str(), role="tool", tool_call_id=call.id
                    )
                )
            return results
        else:
            return None

    return execute_tool_definition(params), codeExecutor


def execute_tool_definition(
    params: FreestyleExecuteScriptParamsConfiguration = None,
) -> ChatCompletionToolParam:
    params = params or FreestyleExecuteScriptParamsConfiguration()
    env_vars = list((params.env_vars or {}).keys())
    node_modules = list((params.node_modules or {}).keys())

    desc = (
        "Execute a JavaScript or TypeScript script.\n"
        + (
            f"You can use the following environment variables: {', '.join(env_vars)}\n"
            if env_vars
            else ""
        )
        + (
            f"You can use the following node modules: {', '.join(node_modules)}"
            if node_modules
            else "You cannot use any node modules."
        )
    )

    return {
        "type": "function",
        "function": {
            "name": "executeCode",
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": (
                            "The JavaScript or TypeScript script to execute, must be in the format of:\n\n"
                            'import { someModule } from "someModule";\n'
                            "export default () => {\n"
                            "   ... your code here ...\n"
                            "   return output;\n"
                            "}\n\n"
                            "or for async functions:\n\n"
                            'import { someModule } from "someModule";\n\n'
                            "export default async () => {\n"
                            "    ... your code here ...\n"
                            "    return output;\n"
                            "}\n"
                        ),
                    }
                },
                "required": ["script"],
            },
        },
    }
