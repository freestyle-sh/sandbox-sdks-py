from _openapi_client.models.freestyle_execute_script_params_configuration import (
    FreestyleExecuteScriptParamsConfiguration,
)
from typing import Tuple, Callable
from google.genai import types

# from google.genai import Content
from freestyle import Freestyle


def execute_tool(
    apiKey: str, params: FreestyleExecuteScriptParamsConfiguration = None
) -> Tuple[types.Tool, Callable[[types.Content], None]]:
    freestyle = Freestyle(apiKey)

    def codeExecutor(completion: types.Content):
        calls = [t for t in completion.parts if t.function_call.name == "executeCode"]

        if not calls:
            return None

        results = [
            # freestyle.executeScript(
            #     json.loads(call.function_call.args)["script"], params
            # )
            freestyle.execute_script(call.function_call.args["script"], params)
            for call in calls
        ]

        return [
            types.FunctionResponseDict(
                id=call.function_call.id,
                name=call.function_call.name,
                response=result.to_str(),
            )
            for result, call in zip(results, calls)
        ]

        # return [
        #     types.Tool(
        #         content=result.to_str(), role="tool", tool_call_id=call.id
        #     )
        #     for result, call in zip(results, calls)
        # ]

    return (execute_tool_definition(params), codeExecutor)


def execute_tool_definition(
    params: FreestyleExecuteScriptParamsConfiguration = None,
) -> types.Tool:
    params = params or FreestyleExecuteScriptParamsConfiguration()
    env_vars = list((params.env_vars or {}).keys())
    node_modules = list((params.node_modules or {}).keys())

    description = (
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

    return types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="executeCode",
                description=description,
                parameters={
                    "type": "object",
                    "required": ["script"],
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
                },
            )
        ]
    )
