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
    GitApi,
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

    def list_git_identities(
        self, limit: int = 100, offset: int = 0, include_managed: bool = False
    ):
        api = GitApi(self._client())
        return api.handle_list_identities(
            limit=limit, offset=offset, include_managed=include_managed
        )

    def cretate_git_identity(self):
        api = GitApi(self._client())
        return api.handle_create_identity()

    def delete_git_identity(self, identity_id: str):
        api = GitApi(self._client())
        return api.handle_delete_identity(identity_id)

    def list_repository_permissions_for_identity(
        self, identity_id: str, limit: int = 100, offset: int = 0
    ):
        api = GitApi(self._client())
        return api.handle_list_repository_permissions_by_identity(
            identity_id=identity_id, limit=limit, offset=offset
        )

    def grant_permission_to_identity(self, identity_id: str, repository_id: str):
        api = GitApi(self._client())
        return api.handle_grant_permission_to_identity(
            identity_id=identity_id, repository_id=repository_id
        )

    def revoke_permission_from_identity(self, identity_id: str, repository_id: str):
        api = GitApi(self._client())
        return api.handle_revoke_permission_from_identity(
            identity_id=identity_id, repository_id=repository_id
        )

    def update_permission_for_identity(
        self, identity_id: str, repository_id: str, permission: str
    ):
        api = GitApi(self._client())
        return api.handle_update_permission_for_identity(
            identity_id=identity_id, repository_id=repository_id, permission=permission
        )

    def list_access_tokens_for_identity(
        self, identity_id: str, limit: int = 100, offset: int = 0
    ):
        api = GitApi(self._client())
        return api.handle_list_access_tokens_by_identity(
            identity_id=identity_id, limit=limit, offset=offset
        )

    def create_access_token_for_identity(
        self, identity_id: str, name: str = "Unnamed Access Token", expires_in: int = 0
    ):
        api = GitApi(self._client())
        return api.handle_create_access_token_for_identity(
            identity_id=identity_id, name=name, expires_in=expires_in
        )

    def revoke_access_token_for_identity(self, identity_id: str, access_token_id: str):
        api = GitApi(self._client())
        return api.handle_revoke_access_token_for_identity(
            identity_id=identity_id, access_token_id=access_token_id
        )

    def list_repositories(self, limit: int = 100, offset: int = 0):
        api = GitApi(self._client())
        return api.handle_list_repositories(limit=limit, offset=offset)

    def create_repository(self, name: str = "Unnamed Repository", private: bool = True):
        api = GitApi(self._client())
        return api.handle_create_repository(name=name, private=private)

    def delete_repository(self, repository_id: str):
        api = GitApi(self._client())
        return api.handle_delete_repository(repository_id=repository_id)
