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
    DevServer,
    DomainsApi,
)
from _openapi_client.api.dev_servers_api import DevServersApi
from _openapi_client.models.access_level import AccessLevel
from _openapi_client.models.create_repo_source import CreateRepoSource
from _openapi_client.models.handle_create_repo_request import HandleCreateRepoRequest
from _openapi_client.models.revoke_git_token_request import RevokeGitTokenRequest
from _openapi_client.models.update_permission_request import UpdatePermissionRequest
from _openapi_client.models.dev_server_request import DevServerRequest
from _openapi_client.models.dev_server_one_of import DevServerOneOf
from _openapi_client.models.freestyle_domain_verification_request import (
    FreestyleDomainVerificationRequest,
)
from _openapi_client.models.freestyle_verify_domain_request import (
    FreestyleVerifyDomainRequest,
)
from _openapi_client.models.freestyle_delete_domain_verification_request import (
    FreestyleDeleteDomainVerificationRequest,
)
from .dev_server import FreestyleDevServer
from typing import Dict, Optional


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

    def create_git_identity(self):
        api = GitApi(self._client())
        return api.handle_create_identity()

    def delete_git_identity(self, identity_id: str):
        api = GitApi(self._client())
        return api.handle_delete_identity(identity=identity_id)

    def list_repository_permissions_for_identity(
        self, identity_id: str, limit: int = 100, offset: int = 0
    ):
        api = GitApi(self._client())
        return api.handle_list_permissions(
            identity=identity_id, limit=limit, offset=offset
        )

    def grant_permission_to_identity(self, identity_id: str, repository_id: str):
        api = GitApi(self._client())
        return api.handle_grant_permission(identity=identity_id, repo=repository_id)

    def revoke_permission_from_identity(self, identity_id: str, repository_id: str):
        api = GitApi(self._client())
        return api.handle_revoke_permission(
            identity=identity_id,
            repo=repository_id,
        )

    def update_permission_for_identity(
        self, identity_id: str, repository_id: str, permission: AccessLevel
    ):
        api = GitApi(self._client())
        return api.handle_update_permission(
            identity=identity_id,
            repo=repository_id,
            update_permission_request=UpdatePermissionRequest(permission=permission),
        )

    def list_access_tokens_for_identity(self, identity_id: str):
        api = GitApi(self._client())
        return api.handle_list_git_tokens(
            identity=identity_id,
        )

    def create_access_token_for_identity(self, identity_id: str):
        api = GitApi(self._client())
        return api.handle_create_git_token(identity=identity_id)

    def revoke_access_token_for_identity(self, identity_id: str, access_token_id: str):
        api = GitApi(self._client())
        # return api.handle_revoke_access_token_for_identity(
        return api.handle_revoke_git_token(
            identity=identity_id,
            revoke_git_token_request=RevokeGitTokenRequest(tokenId=access_token_id),
        )

    def list_repositories(self, limit: int = 100, offset: int = 0):
        api = GitApi(self._client())
        return api.handle_list_repositories(limit=limit, offset=offset)

    def create_repository(
        self,
        name: str = "Unnamed Repository",
        public: bool = True,
        source: Optional[CreateRepoSource] = None,
    ):
        api = GitApi(self._client())
        return api.handle_create_repo(
            handle_create_repo_request=HandleCreateRepoRequest(
                name=name, public=public, source=source
            )
        )

    def delete_repository(self, repository_id: str):
        api = GitApi(self._client())
        return api.handle_delete_repo(repo=repository_id)

    def request_dev_server(
        self,
        repo_id: str,
        base_id: Optional[str] = None,
        dev_command: Optional[str] = None,
        pre_dev_command_once: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        compute_class: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> FreestyleDevServer:
        """
        Request a dev server for a repository. If a dev server is already running
        for that repository, it will return a url to that server. Dev servers are
        ephemeral so you should call this function every time you need a url. Do
        not store the url in your database!
        """
        client = self._client()
        api = DevServersApi(client)

        # Create DevServerRequest object
        dev_server_request = DevServerRequest(
            repo_id=repo_id,
            base_id=base_id,
            dev_command=dev_command,
            pre_dev_command_once=pre_dev_command_once,
            env_vars=env_vars,
            compute_class=compute_class,
            timeout=timeout,
        )

        # Make the API call
        response = api.handle_ephemeral_dev_server(
            dev_server_request=dev_server_request
        )

        # Create DevServer instance for subsequent operations
        dev_server_one_of = DevServerOneOf(
            repo_id=repo_id,
            kind="repo",
        )
        dev_server_instance = DevServer(dev_server_one_of)

        # Convert response to dict for FreestyleDevServer
        response_data = {
            "url": getattr(response, "url", ""),
            "ephemeralUrl": getattr(response, "ephemeral_url", None),
            "mcpEphemeralUrl": getattr(response, "mcp_ephemeral_url", None),
            "isNew": getattr(response, "is_new", False),
            "devCommandRunning": getattr(response, "dev_command_running", False),
            "installCommandRunning": getattr(
                response, "install_command_running", False
            ),
        }

        return FreestyleDevServer(client, dev_server_instance, response_data)

    def create_domain_verification_request(self, domain: str):
        """
        Create a domain verification request. Returns a verification code that needs
        to be placed in a TXT record at _freestyle_custom_hostname.thedomain.com
        """
        api = DomainsApi(self._client())
        return api.handle_create_domain_verification(
            freestyle_domain_verification_request=FreestyleDomainVerificationRequest(
                domain=domain
            )
        )

    def verify_domain(self, domain: str):
        """
        Verify a domain. Note, this requires the domain verification token to be
        already set up in DNS as a TXT record.
        """
        api = DomainsApi(self._client())
        return api.handle_verify_domain(
            freestyle_verify_domain_request=FreestyleVerifyDomainRequest(domain=domain)
        )

    def list_domains(self):
        """
        List verified domains for the account, including *.style.dev domains
        the account has claimed.
        """
        api = DomainsApi(self._client())
        return api.handle_list_domains()

    def list_domain_verification_requests(self):
        """
        List domain verification requests for the current account.
        """
        api = DomainsApi(self._client())
        return api.handle_list_domain_verification_requests()

    def delete_domain_verification_request(self, domain: str, verification_code: str):
        """
        Delete a domain verification request.
        """
        api = DomainsApi(self._client())
        return api.handle_delete_domain_verification(
            freestyle_delete_domain_verification_request=FreestyleDeleteDomainVerificationRequest(
                domain=domain, verification_code=verification_code
            )
        )

    def provision_wildcard(self, domain: str):
        """
        Provision a wildcard certificate for a verified domain. Requires adding
        _acme-challenge.yourdomain.com NS dns.freestyle.sh to DNS.
        """
        api = DomainsApi(self._client())
        return api.handle_verify_wildcard(domain=domain)
