from freestyle import Freestyle
import os
import freestyle

client = Freestyle(os.environ.get("FREESTYLE_API_KEY"))


try:
    a = client.deploy_web(
        src=freestyle.DeploymentSource.from_dict(
            {
                "kind": "git",
                "url": "https://github.com/freestyle-sh/freestyle-base-nextjs-shadcn",
            }
        ),
        config=freestyle.FreestyleDeployWebConfiguration(
            domains=["testingpy.style.dev"],
            build=freestyle.DeploymentBuildOptions.from_dict(True),
            entrypoint="server.js",
        ),
    )

    print("VALUES", a)
except Exception as e:
    print("exception thrown here", e)
