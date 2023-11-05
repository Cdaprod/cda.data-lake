from pydantic import BaseModel, Field, root_validator, SecretStr, HttpUrl, ValidationError
from typing import Any, List, Optional, Dict, Union
from datetime import datetime
import requests




# Define connection settings that could apply to any data source/storage
class ConnectionDetails(BaseModel):
    type: str  # E.g., 'S3', 'database', 'api', etc.
    identifier: str  # Name of the bucket, database, endpoint, etc.
    credentials: Dict[str, str]  # Could include tokens, keys, etc.
    additional_config: Optional[Dict[str, Any]]  # Any other necessary configuration

# Define a generic source model for extraction
class Source(BaseModel):
    source_id: str
    connection_details: ConnectionDetails
    data_format: Optional[str] = None  # E.g., 'csv', 'json', 'parquet', etc.
    extraction_method: Optional[str] = None  # E.g., 'full', 'incremental', etc.
    extraction_query: Optional[str] = None  # SQL query, API endpoint, etc.

# Define a generic transformation model
class Transformation(BaseModel):
    transformation_id: str
    description: Optional[str] = None
    logic: Optional[str] = None  # Reference to a transformation script or function
    dependencies: Optional[List[str]] = []  # IDs of transformations this one depends on

# Define a generic destination model for loading
class Destination(BaseModel):
    destination_id: str
    connection_details: ConnectionDetails
    data_format: Optional[str] = None

# Define a data lifecycle model
class DataLifecycle(BaseModel):
    stage: str  # E.g., 'raw', 'transformed', 'aggregated', etc.
    retention_policy: Optional[str] = None
    archival_details: Optional[str] = None
    access_permissions: Optional[List[str]] = None  # E.g., 'read', 'write', 'admin', etc.

# Define a job control model for ETL orchestration
class JobControl(BaseModel):
    job_id: str
    schedule: Optional[str] = None  # Cron expression for job scheduling
    dependencies: Optional[List[str]] = []  # IDs of jobs this one depends on
    alerting_rules: Optional[Dict[str, Any]] = None  # Alerting configuration

# Define a quality validation model
class QualityValidation(BaseModel):
    checks: Optional[Dict[str, Any]] = None  # E.g., {'null_check': 'No null values'}
    thresholds: Optional[Dict[str, float]] = None  # E.g., {'accuracy': 99.5}
    validation_rules: Optional[Dict[str, Any]] = None  # Custom validation rules

# Define an audit model for tracking ETL jobs
class Audit(BaseModel):
    timestamps: Dict[str, datetime] = Field(default_factory=lambda: {'created_at': datetime.now(), 'modified_at': datetime.now()})
    user_info: Optional[Dict[str, Any]] = None
    operation_type: Optional[str] = None  # E.g., 'ETL Process', 'Data Import', etc.

# Define a performance model for monitoring ETL jobs
class Performance(BaseModel):
    metrics: Optional[Dict[str, Any]] = None  # E.g., {'runtime_seconds': 120}
    logs: Optional[Dict[str, List[str]]] = None  # E.g., {'errors': ['error1', 'error2']}
    bottlenecks: Optional[List[str]] = None

# Define the main ETL process model
class ETLProcess(BaseModel):
    source: List[Source]
    transformations: List[Transformation]
    destination: List[Destination]
    lifecycle: DataLifecycle
    job_control: JobControl
    quality_validation: QualityValidation
    audit: Audit
    performance: Performance

@root_validator(pre=True)
def validate_structure(cls, values):
    """
    Custom validation to ensure the ETL process structure is coherent.
    This could include checks like ensuring all dependencies exist within
    the process definition, or that the data formats between source and
    destination are compatible.
    """
    # Example validation: Check if transformation dependencies are valid
    transformations = values.get('transformations', [])
    transformation_ids = {t.transformation_id for t in transformations}
    for transformation in transformations:
        if any(dep not in transformation_ids for dep in transformation.dependencies):
            raise ValueError('Invalid transformation dependency.')
    return values
    
 

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
                    },
                    {
                        "app_id": "app2",
                        "description": "Second langchain application",
                        # ... similar fields as app1
                    }
                ]
            }
        }
        

class ClientConnection(BaseModel):
    service_name: str = Field(..., description="Name of the service to connect to")
    service_type: str = Field(..., description="Type of service (e.g., 'database', 'api', 'cloud_storage')")
    hostname: Optional[str] = Field(None, description="Hostname of the service")
    port: Optional[int] = Field(None, description="Port to use for the connection")
    username: Optional[str] = Field(None, description="Username for authentication")
    password: Optional[SecretStr] = Field(None, description="Password for authentication")
    api_key: Optional[SecretStr] = Field(None, description="API key for services that require it")
    database_name: Optional[str] = Field(None, description="Name of the database to connect to, if applicable")
    additional_params: Optional[Dict[str, str]] = Field(None, description="Additional parameters required for the connection")
    tools: Optional[List[str]] = Field(None, description="List of tools associated with the service")
    required_vars: Optional[List[str]] = Field(None, description="List of required environment variables for the service")

    class Config:
        min_anystr_length = 1  # Ensuring that strings are not empty
        anystr_strip_whitespace = True  # Stripping whitespace from strings
        schema_extra = {
            "example": {
                "service_name": "Example API Service",
                "service_type": "api",
                "hostname": "api.example.com",
                "port": 443,
                "username": "apiuser",
                "password": "supersecretpassword",
                "api_key": "exampleapikey",
                "additional_params": {
                    "param1": "value1",
                    "param2": "value2"
                },
                "tools": ["curl", "httpie"],
                "required_vars": ["API_HOST", "API_KEY"]
            }
        }
        



class MetastoreAsset(BaseModel):
    asset_id: str = Field(..., description="Unique identifier for the asset")
    asset_type: str = Field(..., description="Type of the asset (e.g., 'table', 'view', 'model')")
    description: Optional[str] = Field(None, description="Description of the asset")
    location: HttpUrl = Field(..., description="URL to the asset location")
    schema: Dict[str, str] = Field(..., description="Schema definition of the asset")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, description="Last update timestamp")
    lineage: Optional[List[str]] = Field(default=[], description="List of asset_ids that are predecessors to this asset")

class Metastore(BaseModel):
    metastore_id: str = Field(..., description="Unique identifier for the metastore")
    assets: Dict[str, MetastoreAsset] = Field(default_factory=dict, description="Dictionary of assets by asset_id")
    repository: HttpUrl = Field(..., description="URL of the GitHub repository serving as the metastore")

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
        return self.assets[asset_id]

    def remove_asset(self, asset_id: str) -> None:
        """
        Removes an asset from the metastore by its asset_id.
        """
        del self.assets[asset_id]
        self.updated_at = datetime.now()
