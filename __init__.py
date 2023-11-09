# cda/data-lake/__init__.py

# Import necessary packages and modules
import logging
from .config_manager import ConfigManager
from .metastore import MetaStore
from .repository_manager import RepositoryManager

# Initialize logging for the data-lake module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from minio import Minio
from minio.error import S3Error
from models.meta import models

# Configuration for MinIO client
MINIO_ENDPOINT = 'your-minio-server:port'
ACCESS_KEY = 'your-access-key'
SECRET_KEY = 'your-secret-key'
BUCKET_NAME = 'your-bucket-name'

# Initialize the MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # Set to True if using https
)

# Ensure the bucket exists and create if it doesn't
try:
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
except S3Error as e:
    print(f"Error occurred while interacting with MinIO: {e}")

# Perform initial setup for the data-lake module
def setup_data_lake(config_path):
    logger.info("Setting up the CDA Data Lake system")

    # Load configuration for the data lake
    config_manager = ConfigManager(config_path)
    config = config_manager.load_configuration()

    # Initialize the MetaStore
    metastore = MetaStore(config['metastore'])

    # Initialize the Repository Manager with the metastore
    repository_manager = RepositoryManager(metastore)

    # Additional initialization code can go here

    logger.info("CDA Data Lake setup complete")

# Optionally perform setup immediately upon module import
# setup_data_lake('path/to/config.json')

# Expose key components for external use
__all__ = ['minio_client', 'MetaStore', 'RepositoryManager', 'setup_data_lake']
