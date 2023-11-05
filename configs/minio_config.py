from models import ClientConnection  # Importing the ClientConnection model

minio_config = ClientConnection(
    service_name="Minio",
    service_type="cloud_storage",
    hostname="localhost",
    port=9000,
    username="your-access-key",
    password="your-secret-key",
    additional_params={
        "secure": False  # Set to True if using HTTPS
    }
)
