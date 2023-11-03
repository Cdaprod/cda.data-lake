from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Union, Dict

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
                    },
                    {
                        "app_id": "app2",
                        "description": "Second langchain application",
                        # ... similar fields as app1
                    }
                ]
            }
        }

# Example instantiation of the LangChainRepo model
langchain_repo = LangChainRepo(
    repo_url="https://github.com/Cdaprod/cda.langchain",
    apps=[
        LangchainApp(
            app_id="app1",
            llm_chains=[LLMChain(chain_id="chain1", components=["comp1", "comp2"], runnables=[Runnable(id="runnable1", entry_point="python scripts/run1.py")])],
            agents=[Agent(agent_id="agent1", capabilities=["analyze_sentiment"])],
            custom_pipelines=[CustomPipeline(pipeline_id="pipeline1", steps=["step1", "step2"])],
            runnables=[Runnable(id="runnable2", entry_point="python scripts/run2.py")],
            metadata={"key1": "value1"}
        ),
        # ... similar instantiation for app2
    ]
)

# Print the example JSON representation of the langchain repo
print(langchain_repo.json(indent=2))
