from typing import Callable, List
from pydantic import BaseModel, Field

# Assuming LCEL is a module that can evaluate string expressions to boolean
import LCEL

# Define the base classes for Runnables and Routers using your schema
class Runnable(BaseModel):
    id: str
    description: str = Field(default="")
    entry_point: str  # The command or function to run the Runnable

# A condition for the router could be a simple callable returning a boolean
Condition = Callable[[dict], bool]

# Define the RunnableBranch with conditions and corresponding Runnables
class RunnableBranch(Runnable):
    conditions: List[Condition]
    runnables: List[Runnable]

    def invoke(self, input_data: dict) -> str:
        # Evaluate conditions and execute the corresponding Runnable
        for condition, runnable in zip(self.conditions, self.runnables):
            if condition(input_data):
                # Here you would actually execute the runnable.entry_point
                # For the example, we just return the description
                return runnable.description
        # Fallback or default action if no conditions are met
        return "Default action"

# Define the Router which manages the RunnableBranches
class Router(BaseModel):
    runnable_branches: List[RunnableBranch] = []

    def route(self, input_data: dict) -> str:
        # Iterate through registered runnable branches and invoke the one whose condition matches
        for branch in self.runnable_branches:
            action = branch.invoke(input_data)
            if action:
                return action
        # If no conditions are met, return a default action or raise an error
        raise ValueError("No valid routing condition met.")

# Example conditions and runnables for data lake operations
is_blog_article = lambda x: x.get("data_type") == "blog_article"
is_code_snippet = lambda x: x.get("data_type") == "code_snippet"

blog_article_processing = Runnable(id="blog_proc", entry_point="process_blog_articles")
code_snippet_processing = Runnable(id="code_proc", entry_point="process_code_snippets")

# Create instances of RunnableBranch for different types of data
blog_article_branch = RunnableBranch(id="blog_branch", runnables=[blog_article_processing], conditions=[is_blog_article])
code_snippet_branch = RunnableBranch(id="code_branch", runnables=[code_snippet_processing], conditions=[is_code_snippet])

# Instantiate a Router and add the runnable branches
data_lake_router = Router(runnable_branches=[blog_article_branch, code_snippet_branch])

# Example input data indicating the type of unstructured data
input_data = {"data_type": "blog_article", "content": "Latest insights on cloud computing."}

# Route the input to get the appropriate action
processing_action = data_lake_router.route(input_data)
print(processing_action)  # Outputs the description of the action to be taken based on the input data type
