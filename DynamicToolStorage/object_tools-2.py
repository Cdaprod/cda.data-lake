
from langchain.tools import Tool
import boto3
import os
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from weaviate import Client
from minio import Minio
from minio.error import MinioException

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level="INFO")

# Environment Checks
def check_env():
    missing_vars = [var for var in ['MINIO_ENDPOINT', 'MINIO_ACCESS_KEY', 'MINIO_SECRET_KEY'] if var not in os.environ]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")

<<< OLD

>>> NEW

# Initialize Minio Client
def get_minio_client() -> Minio:
    try:
        return Minio(
            endpoint=os.environ['MINIO_ENDPOINT'],
            access_key=os.environ['MINIO_ACCESS_KEY'],
            secret_key=os.environ['MINIO_SECRET_KEY'],
        )
    except MinioException as e:
        logger.error(f"Error initializing Minio client: {e}")
        raise

def generate_text_embeddings(text):
    logger.info("Generating text embeddings.")
    
    try:
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        inputs = tokenizer(text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
    except Exception as e:
        logger.error(f"Tokenizer failed: {e}")
        return None
    
    try:
        model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
        outputs = model(**inputs)
    except Exception as e:
        logger.error(f"Model failed: {e}")
        return None
    
    try:
        pooled_output = outputs.pooler_output
        embeddings = pooled_output.detach().cpu().numpy()
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return None
    
    logger.info("Text embeddings generated successfully.")
    return embeddings

# Create custom object in Weaviate
def create_custom_object(embeddings):
    logger.info("Creating custom object in Weaviate.")
    client = initialize_weaviate_client()
    className = "MyCustomClass"
    client.create_class(className)
    properties = {
        "text": {"type": "string"},
        "embeddings": {"type": "vector", "dimensions": 768},
        "code": {"type": "string"}
    }
    client.update_class(className, properties)
    objName = "MyCustomObject"
    objProperties = {
        "text": "This is my custom object.",
        "embeddings": embeddings,
        "code": ""
    }
    client.create_object(objName, className, objProperties)
    logger.info(f"Custom object created: {objName}")
    return objName

def process_and_index_object(key, s3, tokenizer, model, client):
    logger.info(f"Processing and indexing object with key: {key}")
    
    file_path = f"s3://{os.environ['MINIO_ENDPOINT']}/{key}"
    try:
        with open(file_path, 'r') as f:
            text = f.read()
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        return
    
    try:
        embeddings = generate_text_embeddings(text)
    except Exception as e:
        logger.error(f"Failed to generate text embeddings: {e}")
        return
        
    try:
        obj_name = create_custom_object(embeddings)
    except Exception as e:
        logger.error(f"Failed to create custom object: {e}")
        return
    
    logger.info(f"Successfully created custom object: {obj_name}")  # Fixed indentation

def object_tool(inp: str) -> str:
    logger.info(f"Processing object: {inp}")
    check_env()
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
    client = Client("http://192.168.0.25:8082")
    s3 = initialize_minio_client()
    process_and_index_object(inp, s3, tokenizer, model, client)
    logger.info(f"Object processed and indexed: {inp}")
    return f"Processed and indexed object: {inp}"


<<< NEW

>>> OLD

# Generate text embeddings
def generate_text_embeddings(text):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
    outputs = model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
    pooled_output = outputs.pooler_output
    embeddings = pooled_output.cpu().numpy()
    return embeddings

# Create custom object in Weaviate
def create_custom_object(embeddings):
    className = "MyCustomClass"
    client.create_class(className)
    properties = {
        "text": {"type": "string"},
        "embeddings": {"type": "vector", "dimensions": 768},
        "code": {"type": "string"}
    }
    client.update_class(className, properties)
    objName = "MyCustomObject"
    objProperties = {
        "text": "This is my custom object.",
        "embeddings": embeddings,
        "code": ""
    }
    client.create_object(objName, className, objProperties)
    return objName

# Process and index the specified object
def process_and_index_object(key, s3, tokenizer, model, client, minio_endpoint):
    file_path = f"s3://{minio_endpoint}/{key}"
    with open(file_path, 'r') as f:
        text = f.read()
        embeddings = generate_text_embeddings(text)
        obj_name = create_custom_object(embeddings)
        logger.info(f"Created custom object: {obj_name}")

# Main object tool function
def object_tool(inp: str) -> str:
    check_env()
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
    client = Client("http://192.168.0.25:8082")
    s3 = get_minio_client()
    minio_endpoint = os.environ['MINIO_ENDPOINT']
    process_and_index_object(inp, s3, tokenizer, model, client, minio_endpoint)
    return f"Processed and indexed object: {inp}"

# Define tools
def define_tools():
    # Assuming SerpAPIWrapper is imported or defined elsewhere
    search = SerpAPIWrapper()
    search_tool = Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )
    data_tools = []
    object_tools = [
        Tool(
            name="ObjectTool",
            func=object_tool,
            description="A function to process and index objects based on unstructured data"
        )
    ]
    ALL_TOOLS = [search_tool] + data_tools + object_tools
    return ALL_TOOLS

# Usage
if __name__ == "__main__":
    check_env()  
    tools = define_tools()
    object_tool_result = tools[2].func("some-object-key.txt")  # Assuming ObjectTool is at index 2
