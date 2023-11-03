from pydantic import BaseModel, Field, SecretStr
from typing import Optional, List, Dict

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