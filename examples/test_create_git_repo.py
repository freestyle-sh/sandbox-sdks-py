#!/usr/bin/env python3
"""
Test for creating a git repository using the Freestyle SDK.
"""

import freestyle
import os

# Initialize the client
client = freestyle.Freestyle(os.environ.get("FREESTYLE_API_KEY"))

# Create a new repository
repo = client.create_repository(
    name="Test Repository from Python SDK",
    public=True,
    source=freestyle.CreateRepoSource.from_dict(
        {
            "type": "git",
            "url": "https://github.com/freestyle-sh/freestyle-base-nextjs-shadcn",
        }
    ),
)

print("Git repository created successfully!")
print(f"Repository ID: {repo.repo_id}")
print(f"Repository URL: https://git.freestyle.sh/{repo.repo_id}")
