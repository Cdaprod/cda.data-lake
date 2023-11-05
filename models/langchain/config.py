from pydantic import BaseSettings, HttpUrl
from typing import List, Dict, Union, Any

class LangchainConfig(BaseSettings):
    # Repository details
    REPO_URL: HttpUrl = "https://github.com/Cdaprod/cda.langchain"

    # Application settings
    APP_NAME: str = "Langchain Application"
    LLM_TYPE: str = "GPT-4"  # Can be 'GPT-4', 'llama', or 'code-llama'

    # Define lists of chains, agents, pipelines, and runnables
    # These are placeholders and should be replaced with actual implementations
    LLM_CHAINS: List[Any] = []
    AGENTS: List[Any] = []
    CUSTOM_PIPELINES: List[Any] = []
    RUNNABLES: List[Any] = []

    # Metadata and additional configurations can be included as a dictionary
    METADATA: Dict[str, Union[str, int, List[str]]] = {
        "last_updated": "2023-11-03",
        "maintainer": "cdaprod",
        # ... add more metadata as needed
    }

    # Define any other configurations your application needs
    # ...

    class Config:
        # Pydantic will read environment variables with a prefix of 'LANGCHAIN_'
        env_prefix = 'LANGCHAIN_'
        env_file = '.env'

# Instantiate the config which will be used by the application
config = LangchainConfig()

# You can then access the config attributes like so:
# config.APP_NAME, config.REPO_URL, etc.