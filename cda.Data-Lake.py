#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os

# Project root directory name
project_root = "my-lcel-project"

my_lcel_app = "my-lcel-app"

structure = {
    "Dockerfile.data-lake": """
FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SENSITIVE_VAR=sensitive_value

RUN pip install nbconvert

ENTRYPOINT ["python", "webhook.py"]

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

EXPOSE 8000
    """,
    "requirements.txt": """
fastapi==0.75.0
uvicorn==0.17.6
minio==7.1.0
pydantic==1.9.0
jupyter==1.0.0
    """,
    ".dockerignore": """
.env
*.pyc
*.pyo
*.pyd
__pycache__
    """,
    ".env.production": """
SENSITIVE_VAR=production_value
ANOTHER_VAR=value
    """,
    "webhook.py": """
# Import statements
# Flask or FastAPI app setup
# Webhook endpoint definitions
    """,
    "preprocessor.py": """
# Functions for data preprocessing
    """,
    "convert_and_run_notebook.sh": """
#!/bin/bash
# Convert Jupyter notebooks to Python scripts
# Run the converted scripts
    """,
    "start_services.sh": """
#!/bin/bash
# Start the MinIO service
# Run other service start commands
    """,
    "notebooks/babyagi.ipynb": """
{
 "cells": [
  // Notebook cells in JSON format
 ],
 "metadata": {
  // Notebook metadata
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
    """,
    "notebooks/babyagiagent.ipynb": """
{
 "cells": [
  // Notebook cells in JSON format
 ],
 "metadata": {
  // Notebook metadata
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
    """,
    "scripts/some_langchain_pipeline.py": """
# Python code for a langchain pipeline
    """,
    # Add additional files and directories as needed
}

# Python script logic to generate these files and directories will follow...


def create_structure(base_path, structure_dict):
    for name, content in structure_dict.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recursively create subdirectories and files
        else:
            # It's a file
            with open(path, 'w') as f:
                f.write(content)  # Create an empty file or write content to it

# Creating the project root directory
os.makedirs(project_root, exist_ok=True)

# Creating the rest of the structure
create_structure(project_root, structure)

print(f"{project_root} structure has been created.")


# In[ ]:


# ClientConnector.py
# ClientConnector/Pydantic Validator
from pydantic import BaseModel, Field, SecretStr, validator
from typing import Optional, Dict, Union

class ClientConnection(BaseModel):
    service_name: str = Field(..., description="Name of the service to connect to")
    service_type: str = Field(..., description="Type of service (e.g., 'database', 'api', 'cloud_storage')")
    hostname: Optional[str] = Field(None, description="Hostname of the service")
    port: Optional[int] = Field(None, description="Port to use for the connection")
    username: Optional[str] = Field(None, description="Username for authentication")
    password: Optional[SecretStr] = Field(None, description="Password for authentication")
    api_key: Optional[SecretStr] = Field(None, description="API key for services that require it")
    database_name: Optional[str] = Field(None, description="Name of the database to connect to, if applicable")
    additional_params: Optional[Dict[str, Union[str, int, bool]]] = Field(
        None, description="Additional parameters required for the connection"
    )
    
    @validator('service_type')
    def validate_service_type(cls, v):
        allowed_types = ['database', 'api', 'cloud_storage', 'message_broker', 'custom']
        if v not in allowed_types:
            raise ValueError(f'service_type must be one of {allowed_types}')
        return v
    
    @validator('port')
    def validate_port(cls, v, values, **kwargs):
        if 'hostname' in values and values['hostname'] and (v is None or v <= 0):
            raise ValueError('Port must be a positive integer when hostname is provided')
        return v

    class Config:
        min_anystr_length = 1  # Ensuring that strings are not empty
        anystr_strip_whitespace = True  # Stripping whitespace from strings

connection_details = ClientConnection(
    service_name="My Database Service",
    service_type="database",
    hostname="db.example.com",
    port=5432,
    username="user",
    password=SecretStr("securepassword"),
    database_name="mydatabase"
)

# Now, you can use `connection_details` to establish a connection to the service
# The logic for actually establishing the connection would be in another part of your application


# In[4]:


load_dotenv(dotenv_path='./.env')
print(os.getenv('MINIO_ENDPOINT'))  # Do this for each variable


# In[1]:


for key, value in os.environ.items():
    print(f"{key}: {value}")


# In[5]:


minio_config = MinIOClientConfig()
print(minio_config.dict())  # This should print the configuration if loaded correctly


# In[8]:


from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os

# Ensure this is called at the very beginning of your script
load_dotenv(dotenv_path='./.env')


class MinIOClientConfig(BaseModel):
    minio_endpoint: str = Field(..., env='MINIO_ENDPOINT')
    minio_access_key: str = Field(..., env='MINIO_ACCESS_KEY')
    minio_secret_key: str = Field(..., env='MINIO_SECRET_KEY')
    minio_secure: bool = Field(False, env='MINIO_SECURE')

    def load_configuration(self):
        # Your method implementation
        pass

# Now this should work without a ValidationError, assuming your .env is set correctly
minio_config = MinIOClientConfig().load_configuration()


# In[2]:


from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

class ClientConfigABC(ABC):
    @abstractmethod
    def load_configuration(self):
        pass

class SupabaseClientConfig(ClientConfigABC, BaseModel):
    supabase_url: str = Field(..., env='SUPABASE_URL')
    supabase_api_key: str = Field(..., env='SUPABASE_API_KEY')

    def load_configuration(self):
        # Implementation for loading Supabase configuration
        return {"url": self.supabase_url, "key": self.supabase_api_key}

class MariaDBClientConfig(ClientConfigABC, BaseModel):
    mariadb_host: str = Field(..., env='MARIADB_HOST')
    mariadb_user: str = Field(..., env='MARIADB_USER')
    mariadb_password: str = Field(..., env='MARIADB_PASSWORD')
    mariadb_database: str = Field(..., env='MARIADB_DATABASE')

    def load_configuration(self):
        # Implementation for loading MariaDB configuration
        return {"host": self.mariadb_host, "user": self.mariadb_user,
                "password": self.mariadb_password, "database": self.mariadb_database}

class MinIOClientConfig(ClientConfigABC, BaseModel):
    minio_endpoint: str = Field(..., env='MINIO_ENDPOINT')
    minio_access_key: str = Field(..., env='MINIO_ACCESS_KEY')
    minio_secret_key: str = Field(..., env='MINIO_SECRET_KEY')
    minio_secure: bool = Field(..., env='MINIO_SECURE')

    def load_configuration(self):
        # Implementation for loading MinIO configuration
        return {"endpoint": self.minio_endpoint, "access_key": self.minio_access_key,
                "secret_key": self.minio_secret_key, "secure": self.minio_secure}

# Example usage:
# supabase_config = SupabaseClientConfig().load_configuration()
# mariadb_config = MariaDBClientConfig().load_configuration()
minio_config = MinIOClientConfig().load_configuration()


# In[ ]:


# supabase_client.py
# Supabase Client with Env
# !pip install supabase-py

import os
from dotenv import load_dotenv
from supabase_py import create_client

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')

# Initialize a Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# mariadb_client.py
# MariaDB Client with Env
# !pip install mysql-connector-python

import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Access environment variables
MARIADB_HOST = os.getenv('MARIADB_HOST')
MARIADB_USER = os.getenv('MARIADB_USER')
MARIADB_PASSWORD = os.getenv('MARIADB_PASSWORD')
MARIADB_DATABASE = os.getenv('MARIADB_DATABASE')

# Initialize a MariaDB connection
mariadb_connection = mysql.connector.connect(
    host=MARIADB_HOST,
    user=MARIADB_USER,
    password=MARIADB_PASSWORD,
    database=MARIADB_DATABASE
)


# minio_client.py
# minio_client using .env
import os
from dotenv import load_dotenv
from minio import Minio

# Load environment variables from .env file
load_dotenv()

# Access environment variables
endpoint = os.getenv('MINIO_ENDPOINT')
access_key = os.getenv('MINIO_ACCESS_KEY')
secret_key = os.getenv('MINIO_SECRET_KEY')
secure = os.getenv('MINIO_SECURE') == 'True'  # Convert string to boolean

# Initialize a Minio client
minio_client = Minio(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=secure
)
minio_client

# List all buckets
buckets = minio_client.list_buckets()
for bucket in buckets:
    print(bucket.name)

# List all objects in a bucket
objects = minio_client.list_objects("my-bucket")
for obj in objects:
    print(obj.object_name)

# Get an object from a bucket
data = minio_client.get_object("my-bucket", "my-file.txt")
with data as d:
    print(d.read().decode())


# In[ ]:


# repo_model.py
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
    'cda.langchain', 'cda.agents',
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


# In[ ]:


# Construct Data Lake MonoRepo
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

def fetch_repo_data(repo_name: str):
    # Get GitHub API token from environment variables
    gh_token = os.getenv('GH_TOKEN')

    headers = {'Authorization': f'token {gh_token}'}
    response = requests.get(f'https://api.github.com/repos/Cdaprod/{repo_name}', headers=headers)
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

import json

# Fetch and construct the JSON object for the data lake
data_lake_json = construct_data_lake_json(repo_names)

# Write the JSON object to a file
with open('data_lake.json', 'w') as f:
    json.dump(data_lake_json, f, indent=2)


# In[ ]:


# etl_model.py
from pydantic import BaseModel, Field, root_validator
from typing import Any, List, Optional, Dict, Union
from datetime import datetime

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

if __name__ == "__main__":
    # Define an ETL process
    etl_process = ETLProcess(
        source=[
            Source(
                source_id='source1',
                connection_details=ConnectionDetails(
                    type='S3',
                    identifier='my-s3-bucket',
                    credentials={'access_key': 'ACCESSKEY', 'secret_key': 'SECRETKEY'},
                    additional_config={'region': 'us-east-1'}
                ),
                data_format='csv'
            )
        ],
        transformations=[
            Transformation(
                transformation_id='trans1',
                description='Normalize column names',
                logic='path/to/transformation/script.py',
                dependencies=[]
            )
        ],
        destination=[
            Destination(
                destination_id='dest1',
                connection_details=ConnectionDetails(
                    type='database',
                    identifier='my_database',
                    credentials={'username': 'user', 'password': 'pass'}
                ),
                data_format='table'
            )
        ],
        lifecycle=DataLifecycle(
            stage='raw',
            retention_policy='30 days',
            archival_details='Archive to Glacier after 1 year',
            access_permissions=['read', 'write']
        ),
        job_control=JobControl(
            job_id='job1',
            schedule='0 0 * * *',  # Run daily at midnight
            dependencies=[],
            alerting_rules={'email': 'alert@example.com'}
        ),
        quality_validation=QualityValidation(
            checks={'null_check': 'No null values allowed'},
            thresholds={'accuracy': 99.5},
            validation_rules={'regex': '^[a-zA-Z0-9]+$'}
        ),
        audit=Audit(
            user_info={'initiated_by': 'ETL System'},
            operation_type='Data Import'
        ),
        performance=Performance(
            metrics={'runtime_seconds': 120},
            logs={'errors': []},
            bottlenecks=['transformation_time']
        )
    )

    # Print the ETL process details
    print(etl_process.json(indent=2))


# In[ ]:


# Assuming repo_model.py and etl_model.py exist and are in the same directory or in PYTHONPATH
# from repo_model import fetch_repo_data, construct_repo_json, construct_data_lake_json
# from etl_model import ETLProcess, Source, Transformation, Destination, ConnectionDetails, DataLifecycle, JobControl, QualityValidation, Audit, Performance

# Function to run the ETL process
def run_etl_process(repo_names):
    # Extract data from GitHub repositories
    extracted_data = construct_data_lake_json(repo_names)
    
    # Here we would define the transformations required on the extracted data
    # For simplicity, we assume it's just passed through
    transformed_data = extracted_data
    
    # Load the transformed data into S3
    # Define the S3 bucket details
    s3_connection = ConnectionDetails(
        type='S3',
        identifier='my-s3-bucket',
        credentials={'access_key': 'ACCESSKEY', 'secret_key': 'SECRETKEY'},
        additional_config={'region': 'us-east-1'}
    )
    
    # Define the destination for the ETL process
    destination = Destination(
        destination_id='dest1',
        connection_details=s3_connection,
        data_format='json'
    )
    
    # Here we would actually write the code to load data into S3
    # For now, this is just a placeholder function call
    load_to_s3(transformed_data, destination)
    
    # Return a confirmation message
    return "ETL process completed successfully"

# Placeholder function for loading data to S3
def load_to_s3(data, destination):
    # This function would contain the actual logic to connect to S3 and upload the data
    # Currently, it's just a placeholder to illustrate the workflow
    print("Data would be loaded to S3 here")

# List of repository names to run the ETL process on
repo_names = [
    'cda.langchain-templates', 'cda.agents',
    # ... other repositories
]

# Call to run the ETL process
etl_confirmation = run_etl_process(repo_names)

# Output the result
print(etl_confirmation)

