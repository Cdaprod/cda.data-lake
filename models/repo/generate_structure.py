# Given the list of repositories provided by the user, we will fetch data from GitHub API for each.

import requests
from pydantic import BaseModel, ValidationError, HttpUrl
from typing import List, Optional
from datetime import datetime
import os
import subprocess
import json



repo_names = [
    'cda.langchain-templates', 'cda.agents',
    'cda.Juno', 'cda.actions',
    'cda.data-lake', 'cda.ml-pipeline', 'cda.notebooks',
    'cda.CMS_Automation_Pipeline', 'cda.ml-pipeline',
    'cda.data', 'cda.databases', 'cda.s3',
    'cda.docker', 'cda.kubernetes', 'cda.jenkins',
    'cda.weaviate', 'cda.WeaviateApiFrontend',
    'cda.Index-Videos',
    'cda.dotfiles', 'cda.faas', 'cda.pull', 'cda.resumes', 'cda.snippets', 'cda.superagent', 'cda.ZoomVirtualOverlay', 'cda.knowledge-platform',
    'cda.nginx'
]



# Define the Owner model
class Owner(BaseModel):
    name: str
    id: int
    type: str  # User or Organization

# Define the Repository model
class Repository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: Owner
    private: bool
    html_url: HttpUrl
    description: Optional[str]
    fork: bool
    url: HttpUrl
    created_at: datetime
    updated_at: datetime
    pushed_at: datetime
    git_url: str
    ssh_url: str
    clone_url: HttpUrl
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    forks_count: int
    mirror_url: Optional[HttpUrl]
    archived: bool
    disabled: bool
    open_issues_count: int
    license: Optional[str]
    allow_forking: bool
    is_template: bool
    topics: List[str]
    visibility: str  # 'public' or 'private'

class GitHubAPI:
    BASE_URL = 'https://api.github.com'

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json',
        }

    def get_repository(self, repo_name: str) -> Repository:
        """
        Fetch repository data from GitHub and return a Repository object.
        """
        url = f"{self.BASE_URL}/repos/{repo_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Repository(**response.json())
        else:
            print(f"Failed to fetch repository {repo_name}: {response.status_code}")
            return None

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

    def generate_build_structure_json(self, repositories: List[Repository]):
        """
        Generate a JSON file of the build structure of the cloned repositories.
        """
        build_structure = {
            'repositories': [repo.dict() for repo in repositories]
        }
        with open('build_structure.json', 'w') as f:
            json.dump(build_structure, f, indent=2)
        print("Generated build_structure.json")

github_api = GitHubAPI(access_token=os.environ.get('GH_TOKEN'))

cloned_repositories = []

for repo_name in repo_names:
    repo_data = github_api.get_repository(repo_name)
    if repo_data:
        github_api.clone_repository(repo_data)
        cloned_repositories.append(repo_data)

github_api.generate_build_structure_json(cloned_repositories)