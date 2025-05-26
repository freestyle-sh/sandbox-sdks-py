from _openapi_client import (
    Configuration,
    ApiClient,
    FreestyleExecuteScriptParamsConfiguration,
    ExecuteApi,
    FreestyleExecuteScriptParams,
    FreestyleDeployWebPayloadV2,
    WebApi,
    DeploymentSource,
    FreestyleDeployWebConfiguration,
)


class Freestyle:
    def __init__(self, token: str, baseUrl: str = "https://api.freestyle.sh"):
        self.token = token
        self.baseUrl = baseUrl

    def _client(self):
        configuration = Configuration()
        configuration.host = self.baseUrl

        client = ApiClient(configuration)
        client.set_default_header("Authorization", f"Bearer {self.token}")
        return client

    def execute_script(
        self, code: str, config: FreestyleExecuteScriptParamsConfiguration = None
    ):
        api = ExecuteApi(self._client())
        return api.handle_execute_script(
            FreestyleExecuteScriptParams(script=code, config=config)
        )

    def deploy_web(
        self,
        src: DeploymentSource,
        config: FreestyleDeployWebConfiguration = None,
    ):
        api = WebApi(self._client())
        return api.handle_deploy_web_v2(
            FreestyleDeployWebPayloadV2(source=src, config=config)
        )
