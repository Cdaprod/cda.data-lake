import requests
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from Repository_model import Repository, Owner
import os
import subprocess
import json

# Insert your previously defined Owner and Repository classes here

class GitHubAPI:
    BASE_URL = 'https://api.github.com'

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json',
        }
    
    def create_webhook(self, repository: Repository, webhook_url: str, events: List[str], secret: Optional[str] = None):
        """
        Create a webhook for the given repository.
        :param repository: Repository object
        :param webhook_url: The payload URL to deliver the payload to
        :param events: The list of events that the hook is triggered for
        :param secret: An optional secret for the hook's payload
        """
        webhook_data = {
            'config': {
                'url': webhook_url,
                'content_type': 'json',
                'secret': secret
            },
            'events': events,
            'active': True
        }

        # Construct the URL for webhook creation
        url = f"{self.BASE_URL}/repos/{repository.owner.name}/{repository.name}/hooks"

        response = requests.post(url, headers=self.headers, json=webhook_data)
        if response.status_code == 201:
            print(f"Webhook created for {repository.full_name}")
            return response.json()
        else:
            print(f"Failed to create webhook for {repository.full_name}: {response.text}")
            response.raise_for_status()

    def clone_repository(self, repository: Repository):
        """
        Clone the given repository to the current working directory.
        """
        clone_url = repository.clone_url.replace('https://', f'https://{self.access_token}@')
        repo_path = os.path.join(os.getcwd(), repository.name)
        
        if not os.path.exists(repo_path):
            subprocess.run(["git", "clone", clone_url], check=True)
            print(f"Repository {repository.name} cloned into {repo_path}")
        else:
            print(f"Repository {repository.name} already exists in the current directory.")

    def generate_build_structure_json(self):
        """
        Generate a JSON file of the build structure of the cloned repositories.
        """
        # Assuming the build structure is a list of repository names
        build_structure = {
            'repositories': [repo.name for repo in self.cloned_repositories]
        }
        with open('build_structure.json', 'w') as f:
            json.dump(build_structure, f, indent=2)
        print("Generated build_structure.json")

# Usage
# Construct your GitHubAPI object and Repository objects as before
# Call the clone_repository method for each repository
# After cloning, call generate_build_structure_json to create the JSON file

# Import the list of repository names from repo_list.py
from repo_list import repo_names

# Instantiate the GitHubAPI class
github_api = GitHubAPI(access_token=os.environ.get('GH_TOKEN'))

# Loop over the repository names and clone them
for repo_name in repo_names:
    repository = github_api.get_repository(repo_name)  # You need to implement get_repository method
    github_api.clone_repository(repository)

# After cloning, generate the build structure JSON
github_api.generate_build_structure_json()
