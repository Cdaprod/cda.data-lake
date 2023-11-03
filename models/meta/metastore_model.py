from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, List, Optional
from datetime import datetime

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

if __name__ == "__main__":
    # Instantiate the metastore with the empty GitHub repository
    metastore = Metastore(
        metastore_id='cda_metastore',
        repository='https://github.com/Cdaprod/cda.metastore'
    )
    # Print the metastore details
    print(metastore.json(indent=2))
