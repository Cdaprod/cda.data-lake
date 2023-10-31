class BucketManager(Runnable):
    def __init__(self):
        self.minio_client = Minio(
            endpoint='minio.example.com',
            access_key='your-access-key',
            secret_key='your-secret-key',
            secure=False
        )
    ...
