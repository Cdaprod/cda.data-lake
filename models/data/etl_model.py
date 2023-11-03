from pydantic import BaseModel, Field, root_validator
from typing import Any, List, Optional, Dict, Union
from datetime import datetime

# Define connection settings that could apply to any data source/storage
class ConnectionDetails(BaseModel):
    type: str  # E.g., 'S3', 'database', 'api', etc.
    identifier: str  # Name of the bucket, database, endpoint, etc.
    credentials: Dict[str, str]  # Could include tokens, keys, etc.
    additional_config: Optional[Dict[str, Any]]  # Any other necessary configuration

# Define a generic source model for extraction
class Source(BaseModel):
    source_id: str
    connection_details: ConnectionDetails
    data_format: Optional[str] = None  # E.g., 'csv', 'json', 'parquet', etc.
    extraction_method: Optional[str] = None  # E.g., 'full', 'incremental', etc.
    extraction_query: Optional[str] = None  # SQL query, API endpoint, etc.

# Define a generic transformation model
class Transformation(BaseModel):
    transformation_id: str
    description: Optional[str] = None
    logic: Optional[str] = None  # Reference to a transformation script or function
    dependencies: Optional[List[str]] = []  # IDs of transformations this one depends on

# Define a generic destination model for loading
class Destination(BaseModel):
    destination_id: str
    connection_details: ConnectionDetails
    data_format: Optional[str] = None

# Define a data lifecycle model
class DataLifecycle(BaseModel):
    stage: str  # E.g., 'raw', 'transformed', 'aggregated', etc.
    retention_policy: Optional[str] = None
    archival_details: Optional[str] = None
    access_permissions: Optional[List[str]] = None  # E.g., 'read', 'write', 'admin', etc.

# Define a job control model for ETL orchestration
class JobControl(BaseModel):
    job_id: str
    schedule: Optional[str] = None  # Cron expression for job scheduling
    dependencies: Optional[List[str]] = []  # IDs of jobs this one depends on
    alerting_rules: Optional[Dict[str, Any]] = None  # Alerting configuration

# Define a quality validation model
class QualityValidation(BaseModel):
    checks: Optional[Dict[str, Any]] = None  # E.g., {'null_check': 'No null values'}
    thresholds: Optional[Dict[str, float]] = None  # E.g., {'accuracy': 99.5}
    validation_rules: Optional[Dict[str, Any]] = None  # Custom validation rules

# Define an audit model for tracking ETL jobs
class Audit(BaseModel):
    timestamps: Dict[str, datetime] = Field(default_factory=lambda: {'created_at': datetime.now(), 'modified_at': datetime.now()})
    user_info: Optional[Dict[str, Any]] = None
    operation_type: Optional[str] = None  # E.g., 'ETL Process', 'Data Import', etc.

# Define a performance model for monitoring ETL jobs
class Performance(BaseModel):
    metrics: Optional[Dict[str, Any]] = None  # E.g., {'runtime_seconds': 120}
    logs: Optional[Dict[str, List[str]]] = None  # E.g., {'errors': ['error1', 'error2']}
    bottlenecks: Optional[List[str]] = None

# Define the main ETL process model
class ETLProcess(BaseModel):
    source: List[Source]
    transformations: List[Transformation]
    destination: List[Destination]
    lifecycle: DataLifecycle
    job_control: JobControl
    quality_validation: QualityValidation
    audit: Audit
    performance: Performance

@root_validator(pre=True)
def validate_structure(cls, values):
    """
    Custom validation to ensure the ETL process structure is coherent.
    This could include checks like ensuring all dependencies exist within
    the process definition, or that the data formats between source and
    destination are compatible.
    """
    # Example validation: Check if transformation dependencies are valid
    transformations = values.get('transformations', [])
    transformation_ids = {t.transformation_id for t in transformations}
    for transformation in transformations:
        if any(dep not in transformation_ids for dep in transformation.dependencies):
            raise ValueError('Invalid transformation dependency.')
    return values

if __name__ == "__main__":
    # Define an ETL process
    etl_process = ETLProcess(
        source=[
            Source(
                source_id='source1',
                connection_details=ConnectionDetails(
                    type='S3',
                    identifier='my-s3-bucket',
                    credentials={'access_key': 'ACCESSKEY', 'secret_key': 'SECRETKEY'},
                    additional_config={'region': 'us-east-1'}
                ),
                data_format='csv'
            )
        ],
        transformations=[
            Transformation(
                transformation_id='trans1',
                description='Normalize column names',
                logic='path/to/transformation/script.py',
                dependencies=[]
            )
        ],
        destination=[
            Destination(
                destination_id='dest1',
                connection_details=ConnectionDetails(
                    type='database',
                    identifier='my_database',
                    credentials={'username': 'user', 'password': 'pass'}
                ),
                data_format='table'
            )
        ],
        lifecycle=DataLifecycle(
            stage='raw',
            retention_policy='30 days',
            archival_details='Archive to Glacier after 1 year',
            access_permissions=['read', 'write']
        ),
        job_control=JobControl(
            job_id='job1',
            schedule='0 0 * * *',  # Run daily at midnight
            dependencies=[],
            alerting_rules={'email': 'alert@example.com'}
        ),
        quality_validation=QualityValidation(
            checks={'null_check': 'No null values allowed'},
            thresholds={'accuracy': 99.5},
            validation_rules={'regex': '^[a-zA-Z0-9]+$'}
        ),
        audit=Audit(
            user_info={'initiated_by': 'ETL System'},
            operation_type='Data Import'
        ),
        performance=Performance(
            metrics={'runtime_seconds': 120},
            logs={'errors': []},
            bottlenecks=['transformation_time']
        )
    )

    # Print the ETL process details
    print(etl_process.json(indent=2))


