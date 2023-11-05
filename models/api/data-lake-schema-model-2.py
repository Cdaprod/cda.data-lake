
from pydantic import BaseModel, Field, SecretStr, HttpUrl
from typing import Any, List, Dict, Optional, Union
from datetime import datetime


# Global constants
DATA_SOURCE_TYPES = ['S3', 'database', 'api', 'local']
DEFAULT_DATA_FORMAT = 'json'
DEFAULT_EXTRACTION_METHOD = 'full'
VALIDATION_RULES = {'null_check': 'No null values', 'accuracy': 99.5}

# Global configuration
API_BASE_URL = "https://api.your-service.com"
CONNECTION_TIMEOUT = 30  # seconds

# Security credentials (These should ideally be loaded from a secure environment or config file)
API_KEY = "your-api-key-here"
SECRET_KEY = "your-secret-key-here"




### CDAPROD ###
class Server(BaseModel):
    ip: str
    creds: Dict[str, Any]  # This could be further defined to include specific credential fields
    connection_type: str  # This could be an instance of a ConnectionType class if defined

class Cdaprod(BaseModel):
    server: Server
    repository: HttpUrl  # URL to the repository
    services: List[Dict[str, BaseModel]]  # A list of services, each represented as a dictionary
    metastore: Metastore  # Instance of a Metastore class

    def add_service(self, service_name: str, service_instance: BaseModel):
        """
        Add a new service to the Cdaprod instance.
        
        :param service_name: A string identifier for the service.
        :param service_instance: An instance of a service class.
        """
        self.services.append({service_name: service_instance})

    def get_service(self, service_name: str) -> BaseModel:
        """
        Retrieve a service from the Cdaprod instance by its name.
        
        :param service_name: The name of the service to retrieve.
        :return: An instance of the requested service class.
        """
        for service in self.services:
            if service_name in service:
                return service[service_name]
        raise ValueError(f"Service {service_name} not found")

# Example usage:
# server_details = Server(ip='192.168.1.1', creds={'username': 'user', 'password': 'pass'}, connection_type='SSH')
# repository_url = HttpUrl(url='https://github.com/Cdaprod/cda.langchain')
# initial_services = [{'LangChainRepo': LangChainRepo(...)}, {'ClientConnection': ClientConnection(...)}]
# metastore_instance = Metastore(...)
# cdaprod_instance = Cdaprod(server=server_details, repository=repository_url, services=initial_services, metastore=metastore_instance)



### GITHUB ###
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




### LANGCHAIN ###
# Define the base class for Runnables
class Runnable(BaseModel):
    id: str
    description: Optional[str]
    entry_point: str  # The command or function to run the Runnable

# Define a model for RunnableBranch
class RunnableBranch(BaseModel):
    id: str
    description: Optional[str]
    conditions: List[str]  # LCEL expressions to evaluate conditions
    runnables: List[Runnable]  # List of Runnables corresponding to conditions

# Define a model for LLM Chains
class LLMChain(BaseModel):
    chain_id: str
    description: Optional[str]
    components: List[str]  # IDs of components that make up this chain
    runnables: List[Union[Runnable, RunnableBranch]]  # Runnables and RunnableBranches in this chain

# Define a model for Agents
class Agent(BaseModel):
    agent_id: str
    description: Optional[str]
    capabilities: List[str]  # A list of actions or operations the agent can perform

# Define a model for custom pipelines
class CustomPipeline(BaseModel):
    pipeline_id: str
    description: Optional[str]
    steps: List[str]  # A list of step IDs that make up the pipeline

# Define a model for a Langchain application
class LangchainApp(BaseModel):
    app_id: str
    description: Optional[str]
    llm_chains: List[LLMChain]
    agents: List[Agent]
    custom_pipelines: List[CustomPipeline]
    runnables: List[Runnable]
    metadata: Dict[str, Union[str, int, List[str]]] = Field(default_factory=dict)

# Define a model for the entire langchain repo
class LangChainRepo(BaseModel):
    repo_url: HttpUrl
    apps: List[LangchainApp]  # List of LangchainApps within this repo
    class Config:
        schema_extra = {
            "example": {
                "repo_url": "https://github.com/Cdaprod/cda.langchain",
                "apps": [
                    {
                        "app_id": "app1",
                        "description": "First langchain application",
                        "llm_chains": [
                            {
                                "chain_id": "chain1",
                                "description": "LLM Chain 1",
                                "components": ["comp1", "comp2"],
                                "runnables": [
                                    {
                                        "id": "runnable1",
                                        "description": "Runnable 1",
                                        "entry_point": "python scripts/run1.py"
                                    }
                                ]
                            }
                        ],
                        "agents": [
                            {
                                "agent_id": "agent1",
                                "description": "Agent 1",
                                "capabilities": ["analyze_sentiment"]
                            }
                        ],
                        "custom_pipelines": [
                            {
                                "pipeline_id": "pipeline1",
                                "description": "Custom Pipeline 1",
                                "steps": ["step1", "step2"]
                            }
                        ],
                        "runnables": [
                            {
                                "id": "runnable2",
                                "description": "Runnable 2",
                                "entry_point": "python scripts/run2.py"
                            }
                        ],
                        "metadata": {"key1": "value1"}
                    }
                    # ... Additional LangchainApps could be defined in a similar structure
                ]
            }
        }


 
### CLIENTS ### 
# Define connection settings that could apply to any data source/storage
class ConnectionDetails(BaseModel):
    """
    A model representing the connection details for a data source or storage.
    Attributes:
        type: The type of connection (e.g., 'S3', 'database', 'api').
        identifier: A unique identifier for the connection (e.g., bucket name, database name).
        credentials: A dictionary containing the credentials for the connection.
        additional_config: Additional configuration details as needed.
    """
    type: str
    identifier: str
    credentials: Dict[str, str]
    additional_config: Optional[Dict[str, Any]] = None


# Define a model for the Client Connection to manage service interactions
class ClientConnection(BaseModel):
    """
    A model representing the configuration for connecting to a service.
    Attributes:
        service_name: The name of the service.
        service_type: The type of service (e.g., 'database', 'api', 'cloud_storage').
        hostname: The service's hostname.
        port: The port to use for connecting to the service.
        username: The username for authentication.
        password: The password for authentication (kept secret).
        api_key: The API key for services that require it (kept secret).
        database_name: The name of the database, if applicable.
        additional_params: Any additional parameters required for the connection.
        tools: List of tools associated with the service.
        required_vars: List of required environment variables for the service.
    """
    service_name: str = Field(..., description="Name of the service to connect to")
    service_type: str = Field(..., description="Type of service (e.g., 'database', 'api', 'cloud_storage')")
    hostname: Optional[str] = Field(None, description="Hostname of the service")
    port: Optional[int] = Field(None, description="Port to use for the connection")
    username: Optional[str] = Field(None, description="Username for authentication")
    password: Optional[SecretStr] = Field(None, description="Password for authentication")
    api_key: Optional[SecretStr] = Field(None, description="API key for services that require it")
    database_name: Optional[str] = Field(None, description="Name of the database to connect to, if applicable")
    additional_params: Optional[Dict[str, Any]] = Field(None, description="Additional parameters required for the connection")
    tools: Optional[List[str]] = Field(None, description="List of tools associated with the service")
    required_vars: Optional[List[str]] = Field(None, description="List of required environment variables for the service")

    @classmethod
    def build_service(cls, **data):
        # Initialize the service with the provided data
        service = cls(**data)
        # Here you can add logic to initialize connections or sessions with the service
        # For example, you might want to create a database session or an API client
        # This is a placeholder for wherever you would implement such logic
        # Return the initialized service
        return service



### METASTORE ###
# Define a model for Metastore Assets
class MetastoreAsset(BaseModel):
    asset_id: str = Field(..., description="Unique identifier for the asset")
    asset_type: str = Field(..., description="Type of the asset (e.g., 'table', 'view', 'model')")
    description: Optional[str] = Field(None, description="Description of the asset")
    location: HttpUrl = Field(..., description="URL to the asset location")
    schema: Dict[str, str] = Field(..., description="Schema definition of the asset")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    lineage: List[str] = Field(default_factory=list, description="List of asset_ids that are predecessors to this asset")

# Define a model for Metastore
class Metastore(BaseModel):
    metastore_id: str = Field(..., description="Unique identifier for the metastore")
    assets: Dict[str, MetastoreAsset] = Field(default_factory=dict, description="Dictionary of assets by asset_id")
    repository: HttpUrl = Field(..., description="URL of the GitHub repository serving as the metastore")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    def add_asset(self, asset: MetastoreAsset) -> None:
        """
        Adds a new asset to the metastore.
        """
        self.assets[asset.asset_id] = asset
        self.updated_at = datetime.now()

    def get_asset(self, asset_id: str) -> MetastoreAsset:
        """
        Retrieves an asset from the metastore by its asset_id.
        """
        asset = self.assets.get(asset_id)
        if not asset:
            raise ValueError(f"Asset with ID {asset_id} not found in the metastore.")
        return asset

    def remove_asset(self, asset_id: str) -> None:
        """
        Removes an asset from the metastore by its asset_id.
        """
        if asset_id in self.assets:
            del self.assets[asset_id]
            self.updated_at = datetime.now()
        else:
            raise ValueError(f"Asset with ID {asset_id} not found in the metastore.")



### API GATEWAY ###
class ApiGateway(BaseModel):
    """
    ApiGateway model for advanced API interactions within the infrastructure.

    Attributes:
        name: A unique name for the API gateway.
        services: A list of services that the API gateway can route to.
        load_balancer: The type of load balancing strategy.
        connection_pool: Details of the connection pool for efficient API calls.
        security_details: Security settings such as tokens, API keys, or other credentials.
        timeout: The timeout value for API requests.
        health_check_endpoint: An endpoint for performing health checks on the API.
    """
    name: str = Field(..., description="Unique name for the API gateway")
    services: List[ClientConnection] = Field(..., description="List of client connections for services")
    load_balancer: str = Field("round_robin", description="Load balancing strategy")
    connection_pool: Optional[Dict[str, Any]] = Field(None, description="Connection pool settings")
    security_details: Optional[Dict[str, Any]] = Field(None, description="Security settings for the gateway")
    timeout: Optional[int] = Field(30, description="Timeout for API requests in seconds")
    health_check_endpoint: Optional[str] = Field("/health", description="Endpoint for health checks")

    def get_service_endpoint(self, service_name: str) -> str:
        """
        Retrieves the endpoint for a given service by name, applying load balancing as configured.

        Args:
            service_name: The name of the service to retrieve the endpoint for.

        Returns:
            The endpoint URL for the service.
        """
        # This is a placeholder for load balancer logic.
        # In a real scenario, you'd implement the strategy here.
        services = [service for service in self.services if service.service_name == service_name]
        if not services:
            raise ValueError(f"No service found for name: {service_name}")
        # Simple round-robin for example purposes
        service = services[0]  # Would cycle through services based on load_balancing strategy
        return f"{service.hostname}:{service.port}"

    def perform_health_check(self) -> bool:
        """
        Performs health checks on all services to ensure they are up and running.

        Returns:
            A boolean indicating if all services are healthy.
        """
        # In a real scenario, this would make HTTP requests to the health check endpoints of each service.
        # Here we'll just return True to indicate all services are healthy.
        return True

    def send_request(self, service_name: str, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Send a request to a specified service and endpoint via the API gateway.

        Args:
            service_name: The name of the service to send the request to.
            endpoint: The endpoint to which the request should be sent.
            method: The HTTP method to use for the request.
            data: The data to be sent in the request, if any.

        Returns:
            The response from the API call.
        """
        # Construct the full URL
        service_endpoint = self.get_service_endpoint(service_name)
        url = f"{service_endpoint}/{endpoint}"

        # Here you would add logic to handle the request.
        # For example, using requests or an async HTTP client if you need high performance.
        # response = requests.request(method, url, json=data, headers=self.security_details, timeout=self.timeout)
        # return response.json()

        # Since we can't make actual HTTP requests in this environment,
        # we'll return a placeholder response
        return {"message": "This is a simulated response", "data": data}
        
    class Config:
        schema_extra = {
            "example": {
                "name": "MainGateway",
                "services": [
                    {
                        "service_name": "UserService",
                        "service_type": "api",
                        "hostname": "user.api.your-service.com",
                        "port": 443,
                        "api_key": "example-api-key"
                    },
                    # ...other services...
                ],
                "load_balancer": "round_robin",
                "connection_pool": {"max_size": 10, "timeouts": {"connect": 5}},
                "security_details": {"method": "token", "token": "example-token"},
                "timeout": 30,
                "health_check_endpoint": "/health"
            }
        }