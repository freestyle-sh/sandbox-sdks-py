from freestyle import Freestyle
import os

# Initialize the client
client = Freestyle(os.environ.get("FREESTYLE_API_KEY"))

print("Testing requestDevServer functionality...")

try:
    repo = client.create_repository(
        name="test-freestyle-dev-server",
    )

    # Request a dev server
    dev_server = client.request_dev_server(
        repo_id=repo.repo_id,  # Use just the repo name
    )

    print("Dev server created successfully!")
    print(f"Ephemeral URL: {dev_server.ephemeral_url}")
    print(f"Code Server URL: {dev_server.code_server_url}")
    print(f"MCP URL: {dev_server.mcp_ephemeral_url}")
    print(f"Is New: {dev_server.is_new}")

    # Wait a moment for dev server to initialize
    print("\nWaiting for dev server to initialize...")
    import time
    time.sleep(3)
    
    # Test filesystem operations (note: filesystem API has known issues)
    print("\nTesting filesystem operations...")
    try:
        files = dev_server.fs.ls("")
        print(f"✅ Root directory files: {files[:5]}...")
    except Exception as e:
        print(f"❌ Filesystem API has known endpoint issues: {str(e)[:50]}...")
        print("💡 Use dev_server.process.exec('ls -la') as workaround")

    # Test process execution
    print("\nTesting process execution...")
    try:
        result = dev_server.process.exec("echo 'Hello from dev server!'")
        print(f"Command execution result: {result}")
        
        # Let's see what's in the filesystem using ls command
        print("\nChecking filesystem via process execution...")
        ls_result = dev_server.process.exec("ls -la /")
        print(f"Root directory contents: {ls_result}")
        
        ls_template_result = dev_server.process.exec("ls -la /template 2>/dev/null || echo 'template dir not found'")
        print(f"Template directory contents: {ls_template_result}")
        
        pwd_result = dev_server.process.exec("pwd")
        print(f"Current working directory: {pwd_result}")
        
    except Exception as e:
        print(f"Failed to execute command: {e}")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
