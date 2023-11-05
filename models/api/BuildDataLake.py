from dataclasses import dataclass
from typing import Optional, List, Dict
from data_lake_schema import (
    Cdaprod,
    ClientConnection,
    LangChainRepo,
    Repository,
    Server,
    Metastore,
    MetastoreAsset,
)

@dataclass
class RepoConfig:
    repo_url: str
    apps: Optional[List[str]] = None
    name: Optional[str] = None

@dataclass
class ClientConfig:
    service_name: str
    hostname: str
    credentials: Dict[str, str]

class BuildDataLake:
    def __init__(self, cdaprod_config: Dict):
        # Initialize the Cdaprod instance with its config
        self.cdaprod = Cdaprod(**cdaprod_config)

    def register_repository(self, repo_config: RepoConfig):
        if repo_config.apps is not None:  # LangChainRepo is distinguished by the presence of 'apps'
            repo_instance = LangChainRepo(repo_url=repo_config.repo_url, apps=repo_config.apps)
            self.cdaprod.services.append({'LangChainRepo': repo_instance})
        else:
            repo_instance = Repository(repo_url=repo_config.repo_url, name=repo_config.name)
            self.cdaprod.services.append({'Repository': repo_instance})

    def register_client(self, client_config: ClientConfig):
        client_instance = ClientConnection(
            service_name=client_config.service_name,
            hostname=client_config.hostname,
            credentials=client_config.credentials
        )
        self.cdaprod.services.append({'ClientConnection': client_instance})

    def register_metastore_asset(self, asset_config: Dict):
        asset_instance = MetastoreAsset(**asset_config)
        self.cdaprod.metastore.add_asset(asset_instance)

    def build(self, repo_list: List[RepoConfig], client_list: List[ClientConfig], asset_list: List[Dict]):
        for repo_config in repo_list:
            self.register_repository(repo_config)

        for client_config in client_list:
            self.register_client(client_config)

        for asset_config in asset_list:
            self.register_metastore_asset(asset_config)

        # Additional setup tasks can be added here
        # Return the fully built Cdaprod instance
        return self.cdaprod

# Configuration for server, metastore, and the main repository
cdaprod_config = {
    'server': Server(ip='192.168.1.1', creds={'username': 'user', 'password': 'pass'}, connection_type='SSH'),
    'repository': 'https://github.com/Cdaprod/main-repo',
    'services': [],
    'metastore': Metastore(metastore_id='metastore1', assets={}, repository='https://github.com/Cdaprod/metastore-repo'),
}

# Configuration for repositories, clients, and assets
repo_list = [
    RepoConfig(repo_url='https://github.com/Cdaprod/langchain-repo', apps=['app1', 'app2']),
    RepoConfig(repo_url='https://github.com/Cdaprod/other-repo', name='NonLangchainRepo'),
]

client_list = [
    ClientConfig(service_name='DatabaseService', hostname='db.example.com', credentials={'username': 'user', 'password': 'pass'}),
    ClientConfig(service_name='ApiService', hostname='api.example.com', credentials={'api_key': 'key'}),
]

asset_list = [
    {'asset_id': 'asset1', 'asset_type': 'table', 'location': 'http://example.com/asset1', 'schema': {'field1': 'type1', 'field2': 'type2'}},
    {'asset_id': 'asset2', 'asset_type': 'model', 'location': 'http://example.com/asset2', 'schema': {'fieldA': 'typeA', 'fieldB': 'typeB'}},
]

# Instantiate the builder and build the data lake
builder = BuildDataLake(cdaprod_config)
cdaprod_instance = builder.build(repo_list, client_list, asset_list)

# You can now work with the cdaprod_instance as needed
