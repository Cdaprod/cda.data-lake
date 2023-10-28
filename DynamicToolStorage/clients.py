#!/usr/local/bin python3

# clients.py
import os
import weaviate
import minio

def initialize_weaviate_client():
    client = weaviate.Client(
        os.environ.get("WEAVIATE_URL", "http://localhost:8080")
    )
    return client

def initialize_minio_client():
    minio_client = minio.Minio(
        os.environ.get("MINIO_URL", "localhost:9000"),
        access_key=os.environ.get("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.environ.get("MINIO_SECRET_KEY", "minioadmin"),
        secure=False
    )
    return minio_client
