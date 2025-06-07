from typing import Dict, List, Optional, Union, AsyncGenerator
from _openapi_client.api.dev_servers_api import DevServersApi
from _openapi_client.api_client import ApiClient
from _openapi_client.models import DevServer
from _openapi_client.models.dev_server_status_request import DevServerStatusRequest
from _openapi_client.models.git_commit_push_request import GitCommitPushRequest
from _openapi_client.models.shutdown_dev_server_request import ShutdownDevServerRequest
from _openapi_client.models.exec_request import ExecRequest
import requests


class FreestyleDevServerFilesystem:
    """Filesystem operations for a Freestyle dev server."""

    def __init__(self, client: ApiClient, dev_server_instance: DevServer):
        self.client = client
        self.dev_server_instance = dev_server_instance

    def ls(self, path: str = "") -> List[str]:
        """List files in the dev server directory."""
        # Workaround for OpenAPI client bug - manually construct request
        
        # Get bearer token from the client's default headers
        auth_header = self.client.default_headers.get('Authorization')
        
        if not auth_header:
            raise ValueError("No authorization header found in client")
        
        # Construct URL with filepath
        base_url = self.client.configuration.host
        # Try different URL constructions
        if path == "" or path == "/":
            # For root directory, try without any path
            url = f"{base_url}/ephemeral/v1/dev-servers/files/"
        else:
            # For other paths, encode properly
            from urllib.parse import quote
            encoded_path = quote(path.lstrip('/'), safe='/')
            url = f"{base_url}/ephemeral/v1/dev-servers/files/{encoded_path}"
        # Prepare request body
        request_body = {
            "devServer": self.dev_server_instance.actual_instance.to_dict(),
            "encoding": "utf-8"
        }
        
        # Make POST request
        response = requests.post(
            url,
            json=request_body,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        data = response.json()
        content = data.get('content', {})
        
        if content and content.get('kind') == 'directory':
            return content.get('files', [])
        elif content and content.get('kind') == 'file':
            # If it's a file, return empty list for ls
            return []
        return []

    def read_file(self, path: str, encoding: str = "utf-8") -> str:
        """Read a file from the dev server."""
        # Workaround for OpenAPI client bug - manually construct request
        
        # Get bearer token from the client's default headers
        auth_header = self.client.default_headers.get('Authorization')
        
        if not auth_header:
            raise ValueError("No authorization header found in client")
        
        # Construct URL with filepath
        base_url = self.client.configuration.host
        url = f"{base_url}/ephemeral/v1/dev-servers/files/{path.lstrip('/')}"
        
        # Prepare request body
        request_body = {
            "devServer": self.dev_server_instance.actual_instance.to_dict(),
            "encoding": encoding
        }
        
        # Make POST request
        response = requests.post(
            url,
            json=request_body,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
        
        data = response.json()
        content = data.get('content', {})
        
        if content and content.get('kind') == 'file':
            return content.get('content', '')
        
        raise FileNotFoundError(f"File not found or not a file: {path}")

    def write_file(
        self, path: str, content: Union[str, bytes], encoding: str = "utf-8"
    ) -> None:
        """Write a file to the dev server."""
        # Workaround for OpenAPI client bug - manually construct request
        
        # Get bearer token from the client's default headers
        auth_header = self.client.default_headers.get('Authorization')
        
        if not auth_header:
            raise ValueError("No authorization header found in client")
        
        # Convert content to string if needed
        content_str = content
        if isinstance(content, bytes):
            content_str = content.decode(encoding)
        
        # Construct URL with filepath
        base_url = self.client.configuration.host
        url = f"{base_url}/ephemeral/v1/dev-servers/files/{path.lstrip('/')}"
        
        # Prepare request body
        request_body = {
            "devServer": self.dev_server_instance.actual_instance.to_dict(),
            "content": content_str,
            "encoding": encoding
        }
        
        # Make PUT request
        response = requests.put(
            url,
            json=request_body,
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")


class FreestyleDevServerProcess:
    """Process operations for a Freestyle dev server."""

    def __init__(self, client, dev_server_instance: DevServer):
        self.client = client
        self.dev_server_instance = dev_server_instance

    def exec(self, cmd: str, background: bool = False) -> Dict:
        """Execute a command on the dev server."""
        api = DevServersApi(self.client)
        response = api.handle_exec_on_ephemeral_dev_server(
            exec_request=ExecRequest(
                dev_server=self.dev_server_instance,
                command=cmd,
                background=background,
            )
        )

        return {
            "id": response.id,
            "isNew": response.is_new,
            "stdout": response.stdout,
            "stderr": response.stderr,
        }


class FreestyleDevServer:
    """A Freestyle dev server instance."""

    def __init__(
        self, client: ApiClient, dev_server_instance: DevServer, response_data
    ):
        self.client = client
        self.dev_server_instance = dev_server_instance
        self._data = response_data

        # URLs
        self.ephemeral_url = response_data.get("ephemeralUrl") or response_data.get(
            "url"
        )
        self.mcp_ephemeral_url = response_data.get("mcpEphemeralUrl") or (
            response_data.get("url", "") + "/mcp"
        )
        self.code_server_url = (
            response_data.get("url", "") + "/__freestyle_code_server/?folder=/template"
        )

        # Status flags
        self.is_new = response_data.get("isNew", False)
        self.dev_command_running = response_data.get("devCommandRunning", False)
        self.install_command_running = response_data.get(
            "installCommandRunning", False
        )

        # Filesystem and process interfaces
        self.fs = FreestyleDevServerFilesystem(client, dev_server_instance)
        self.process = FreestyleDevServerProcess(client, dev_server_instance)

    def status(self) -> Dict[str, bool]:
        """Get the status of the dev server."""
        api = DevServersApi(self.client)
        response = api.handle_dev_server_status(
            dev_server_status_request=DevServerStatusRequest(
                dev_server=self.dev_server_instance
            )
        )

        return {"installing": response.installing, "devRunning": response.dev_running}

    def commit_and_push(self, message: str) -> None:
        """Commit and push changes to the dev server repository."""
        from _openapi_client.api.git_api import GitApi

        api = GitApi(self.client)
        api.handle_git_commit_push(
            git_commit_push_request=GitCommitPushRequest(
                dev_server=self.dev_server_instance,
                message=message,
            )
        )

    def shutdown(self) -> Dict[str, Union[bool, str]]:
        """Shutdown the dev server."""
        api = DevServersApi(self.client)
        response = api.handle_shutdown_dev_server(
            shutdown_dev_server_request=ShutdownDevServerRequest(
                dev_server=self.dev_server_instance
            )
        )

        return {"success": response.success, "message": response.message}