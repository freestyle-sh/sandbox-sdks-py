# Freestyle Sandboxes Python SDK

SDKs to let you or your AI run code.

For more information check out the [API documentation](https://api.freestyle.sh).

## Installation

```bash
pip install freestyle
```

### Notes

This package has a general SDK for human interaction with the API, and a series of one liners for easily adding it to any of the popular AI providers.

- `import freestyle` for the general SDK
- `import freestyle.openai` for OpenAI SDK
- `import freestyle.gemini` for Gemini SDK
- `import freestyle.pipecat` for Pipecat SDK
- `import freestyle.langgraph` for Langgraph SDK

## Use of AI SDKs

All of the AI SDKs export a function called `execute_tool` or some variation of it. They are generally used like this

```python
definition, runner = freestyle.provider.execute_tool(YOUR_API_KEY, your_config)
```

This split declaration is necessary because the `definition` is used in the initialization of the AI and the runner is used during the runtime of the AI in some form.

### Pipecat

Pipecat uses the tool format of the underlying AI provider for the declaration of its tools, however uses a pipecat specific format for the execution of its tools. To make it easy to work with, we provide `execute_tool_gemini` and `execute_tool_openai` functions that output `(definition, runner)` tuples that can be used with the `pipecat` SDK and the AI provider of your choice. If you are using Pipecat with a different provider, we separately export the `execute_tool_executor` that can be used as the executor for an independent tool declaration you provide.
