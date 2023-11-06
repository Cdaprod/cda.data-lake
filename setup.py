from setuptools import setup, find_packages

setup(
    name='cda-data-lake',
    version='0.1.0',
    author='David Cannan',
    author_email='Cdaprod@Cdaprod.dev',
    description='A data lake system for storing and processing data for CDA applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cdaprod/cda-data-lake',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'sqlalchemy',
        'fastapi',
        'pydantic',
        'weaviate-client',
        'minio',
        'langchain',
    ],
    entry_points={
        'console_scripts': [
            # define console scripts if any
        ],
    },
)
