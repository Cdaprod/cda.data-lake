import importlib
import pkgutil
import sys
from typing import Dict, Any

# Your existing FeatureStore class
class FeatureStore:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {
            'runnables': {},
            'chains': {},
            'pipelines': {},
            'agents': {}
        }

    def add_feature(self, feature_type: str, name: str, feature: Any):
        if feature_type not in self.store:
            raise ValueError(f"Invalid feature type: {feature_type}")
        self.store[feature_type][name] = feature

    def get_feature(self, feature_type: str, name: str) -> Any:
        if feature_type not in self.store:
            raise ValueError(f"Invalid feature type: {feature_type}")
        return self.store[feature_type].get(name)


# Function to import all modules from a package and store in FeatureStore
def import_and_store(package_name: str, feature_store: FeatureStore):
    package = importlib.import_module(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f'{package_name}.{module_name}'
        module = importlib.import_module(full_module_name)
        # Assuming each module has a class named 'Feature'
        feature_class = getattr(module, 'Feature', None)
        if feature_class is not None:
            feature_instance = feature_class()
            feature_store.add_feature('runnables', module_name, feature_instance)


# Usage
feature_store = FeatureStore()
import_and_store('your_package_name', feature_store)

# Now your feature_store has the 'Feature' instances from all modules in 'your_package_name'
