class DataIngestion(Runnable):
    def run(self, bucket_name, data, object_name):
        try:
            minio_client.put_object(
                bucket_name, object_name, data,
                length=len(data),
            )
        except SomeSpecificException as e:
            # Handle or log exception
            pass
        ...
