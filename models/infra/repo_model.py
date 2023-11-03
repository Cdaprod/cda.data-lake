# Given the list of repositories provided by the user, we will fetch data from GitHub API for each.

import requests
from pydantic import BaseModel, ValidationError
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

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

def fetch_repo_data(repo_name: str):
    response = requests.get(f'https://api.github.com/repos/Cdaprod/{repo_name}')
    if response.status_code == 200:
        return response.json()  # Returns the repo data as a dictionary
    else:
        raise Exception(f'Failed to fetch data for {repo_name}, status code {response.status_code}')

# Function to construct the repository JSON object
def construct_repo_json(repo_data: dict):
    try:
        # Validate and create a Repository object
        repo = Repository(**repo_data)
        # Return the JSON representation
        return repo.json(indent=2)
    except ValidationError as e:
        raise Exception(f"Error in data for repository {repo_data['name']}: {e}")

# Main function to construct the data lake/monorepo JSON
def construct_data_lake_json(repo_names: List[str]):
    all_repos_json = []
    for repo_name in repo_names:
        repo_data = fetch_repo_data(repo_name)
        repo_json = construct_repo_json(repo_data)
        all_repos_json.append(repo_json)
    return all_repos_json

# Fetch and construct the JSON object for the data lake
data_lake_json = construct_data_lake_json(repo_names)

# Output or save the JSON object
print(data_lake_json)

