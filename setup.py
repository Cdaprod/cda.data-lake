from setuptools import setup, find_packages

setup(
    name='DynamicToolStorage',
    version='0.1.0',
    description='Dynamic Tool Storage and Retrieval with Weaviate and Minio',
    packages=find_packages(),
    install_requires=[
        'weaviate-client',
        'minio',
        'langchain',
    ],
)