from typing import Dict, Any

class DataLakeSystem:
    def __init__(self, repo: DataLakeRepo):
        self.repo = repo
        self.routers = {}
        self.runnables = {}
        self.load_repo()

    def load_repo(self):
        # Load and initialize all components from the repo
        for app in self.repo.apps:
            for router_config in app.routers:
                self.routers[router_config.id] = self.create_router(router_config)
            for runnable_config in app.runnables:
                self.runnables[runnable_config.id] = self.create_runnable(runnable_config)

    def create_router(self, router_config: RouterConfig):
        # Create and return a Router instance
        runnable_branches = [self.create_runnable_branch(branch_config) for branch_config in router_config.branches]
        return Router(runnable_branches=runnable_branches)

    def create_runnable_branch(self, branch_config: RunnableBranchConfig):
        # Create and return a RunnableBranch instance
        conditions = [self.create_condition(condition_config) for condition_config in branch_config.conditions]
        runnables = [self.runnables[runnable_id] for runnable_id in branch_config.runnables]
        return RunnableBranch(id=branch_config.id, conditions=conditions, runnables=runnables)

    def create_condition(self, condition_config: ConditionConfig):
        # Create and return a condition callable
        return lambda data: condition_config.expression(data)

    def create_runnable(self, runnable_config: RunnableConfig):
        # Create and return a Runnable instance that can be executed
        return Runnable(id=runnable_config.id, entry_point=runnable_config.entry_point)

    def execute(self, router_id: str, input_data: Dict[str, Any]):
        # Execute the router with the given ID on the input_data
        router = self.routers.get(router_id)
        if router:
            # Process the input using the router
            return router.route(input_data)
        else:
            raise ValueError(f"No router found with ID: {router_id}")

# Example usage:
data_lake_system = DataLakeSystem(repo=data_lake_repo)
output = data_lake_system.execute(router_id='router1', input_data={'data_type': 'blog_article', 'content': 'Latest insights on cloud computing.'})
print(output)
