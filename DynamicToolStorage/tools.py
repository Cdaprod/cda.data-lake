from langchain.tools import Tool
import boto3
import os
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer
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
        
# Your existing functions, integrated with new ones
# def generate_text_embeddings(text, tokenizer, model):
def generate_text_embeddings(text):
    # Tokenize the text
    inputs = tokenizer(text, return_tensors="pt", max_length=512, padding="max_length", truncation=True)

    # Run the text through the BERT model to get the embeddings
    outputs = model(inputs["input_ids"], attention_mask=inputs["attention_mask"])
    pooled_output = outputs.pooler_output

    # Convert the embeddings to a list
    embeddings = pooled_output.cpu().numpy()

    return embeddings

# def create_custom_object(embeddings, client):
def create_custom_object(embeddings):
    # Create a new class with the specified name
    className = "MyCustomClass"
    client.create_class(className)

    # Add properties to the class
    properties = {
        "text": {"type": "string"},
        "embeddings": {"type": "vector", "dimensions": 768},
        "code": {"type": "string"}
    }
    client.update_class(className, properties)

    # Create a new object with the specified name and properties
    objName = "MyCustomObject"
    objProperties = {
        "text": "This is my custom object.",
        "embeddings": embeddings,
        "code": ""  # Initialize the "code" property with an empty string
    }
    client.create_object(objName, className, objProperties)

    return objName


def process_and_index_object(key, s3, tokenizer, model, client):
    file_path = f"s3://{os.environ['MINIO_ENDPOINT']}/{key}"
    with open(file_path, 'r') as f:
        text = f.read()
        embeddings = generate_text_embeddings(text, tokenizer, model)
        obj_name = create_custom_object(embeddings, client)
        print(f"Created custom object: {obj_name}")

def object_tool(inp: str) -> str:
    # Set up the necessary clients and models
    check_env()  # New Line: Check environment variables
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=8)
    client = Client("http://192.168.0.25:8082")
    s3 = get_minio_client()  # New Line: Initialize Minio Client

    # Process and index the specified object
    process_and_index_object(inp, s3, tokenizer, model, client)

    return f"Processed and indexed object: {inp}"

def define_tools():
    search = SerpAPIWrapper()
    search_tool = Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    )

    data_tools = [
        # Define data_tools as needed...
    ]

    object_tools = [
        Tool(
            name="ObjectTool",
            func=object_tool,
            description="A function to process and index objects based on unstructured data"
        )
    ]

    ALL_TOOLS = [search_tool] + data_tools + object_tools
    return ALL_TOOLS

# Usage:
tools = define_tools()
object_tool_result = tools[2].func("some-object-key.txt")  # Assuming ObjectTool is at index 2
