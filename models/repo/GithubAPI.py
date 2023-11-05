import requests
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime
from Repository_model import Repository, Owner

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
