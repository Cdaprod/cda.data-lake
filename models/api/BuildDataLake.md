from data_lake_schema import Cdaprod, Server, Metastore, LangChainRepo, ClientConnection, ApiGateway
from typing import List

class BuildDataLake:
    def __init__(self, repo_list: List[str]):
        self.cdaprod = Cdaprod(
            server=None,  # Server details would be initialized here
            repository=None,  # Main repository details
            services=[],  # Services would be added here
            metastore=None  # Metastore details
        )
        self.repo_list = repo_list

    def setup_server(self):
        # Setup server details
        self.cdaprod.server = Server(
            ip='192.168.1.1',  # Example IP
            creds={'username': 'user', 'password': 'pass'},  # Credentials
            connection_type='SSH'  # Connection type
        )

    def setup_metastore(self):
        # Setup metastore details
        self.cdaprod.metastore = Metastore(
            metastore_id='metastore123',  # Example Metastore ID
            assets={},  # Initialize with no assets
            repository='https://github.com/Cdaprod/cda.metastore'  # Metastore repository URL
        )

    def setup_services(self):
        # Setup services from the repository list
        for repo_url in self.repo_list:
            lang_chain_repo = LangChainRepo(repo_url=repo_url, apps=[])
            # The service dictionary should match the structure expected by the 'services' list in Cdaprod
            service = {'LangChainRepo': lang_chain_repo}
            self.cdaprod.services.append(service)

    def setup_api_gateway(self):
        # Setup API gateway details
        self.cdaprod.api_gateway = ApiGateway(
            name='MyApiGateway',
            services=[],  # This would be filled with instances of ClientConnection
            # Additional API gateway configuration goes here
        )
        # Here you would also configure the routing and any other API gateway specifics

    def build(self):
        # Method to orchestrate the building of the data lake
        self.setup_server()
        self.setup_metastore()
        self.setup_services()
        self.setup_api_gateway()
        # Any other setup steps would be added here
        return self.cdaprod

# Example usage
repo_list = [
    'https://github.com/Cdaprod/cda.langchain',
    'https://github.com/Cdaprod/cda.analytics',
    # Add other repositories as needed
]
builder = BuildDataLake(repo_list)
cdaprod_instance = builder.build()


from data_lake_schema import Cdaprod, ClientConnection, LangChainRepo, Repository, Server, Metastore, MetastoreAsset

class BuildDataLake:
    def __init__(self, cdaprod_config):
        self.cdaprod = Cdaprod(**cdaprod_config)  # Initialize the Cdaprod instance with its config

    def register_repository(self, repo_config):
        # Check if it's a LangChainRepo type
        if 'apps' in repo_config:  # Assuming 'apps' is a distinguishing feature of LangChainRepo
            repo_instance = LangChainRepo(**repo_config)
            self.cdaprod.services.append({'LangChainRepo': repo_instance})
        else:  # Otherwise, treat it as a generic Repository
            repo_instance = Repository(**repo_config)
            self.cdaprod.services.append({'Repository': repo_instance})

    def register_client(self, client_config):
        # Instantiate ClientConnection with credentials and connection details
        client_instance = ClientConnection(**client_config)
        # Add to services as a ClientConnection
        self.cdaprod.services.append({'ClientConnection': client_instance})

    def register_metastore_asset(self, asset_config):
        # Instantiate MetastoreAsset
        asset_instance = MetastoreAsset(**asset_config)
        # Add asset to the Metastore
        self.cdaprod.metastore.add_asset(asset_instance)

    def build(self, repo_list, client_list, asset_list):
        # Register repositories
        for repo_config in repo_list:
            self.register_repository(repo_config)
        
        # Register clients
        for client_config in client_list:
            self.register_client(client_config)

        # Register metastore assets
        for asset_config in asset_list:
            self.register_metastore_asset(asset_config)
        
        # After all services are registered, you could perform additional setup tasks
        return self.cdaprod

# Example configuration for repositories, clients, and assets
repo_list = [
    {'repo_url': 'https://github.com/Cdaprod/langchain-repo', 'apps': ['app1', 'app2']},
    {'repo_url': 'https://github.com/Cdaprod/other-repo', 'name': 'NonLangchainRepo'}
]

client_list = [
    {'service_name': 'DatabaseService', 'hostname': 'db.example.com', 'credentials': {'username': 'user', 'password': 'pass'}},
    {'service_name': 'ApiService', 'hostname': 'api.example.com', 'credentials': {'api_key': 'key'}}
]

asset_list = [
    {'asset_id': 'asset1', 'asset_type': 'table', 'location': 'http://example.com/asset1', 'schema': {'field1': 'type1', 'field2': 'type2'}},
    {'asset_id': 'asset2', 'asset_type': 'model', 'location': 'http://example.com/asset2', 'schema': {'fieldA': 'typeA', 'fieldB': 'typeB'}}
]

# Example usage:
cdaprod_config = {
    'server': Server(ip='192.168.1.1', creds={'username': 'user', 'password': 'pass'}, connection_type='SSH'),
    'repository': 'https://github.com/Cdaprod/main-repo',
    'services': [],  # Initially empty, will be populated in the build process
    'metastore': Metastore(metastore_id='metastore1', assets={}, repository='https://github.com/Cdaprod/metastore-repo')
}

builder = BuildDataLake(cdaprod_config)
cdaprod_instance = builder.build(repo_list, client_list, asset_list)
