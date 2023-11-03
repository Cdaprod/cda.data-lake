

# main.py for the data lake agent application
import logging
import DataLakeAgent
from DynamicToolStorage import MinioManager
from frontend.gradio_app import create_gradio_app

# Set up basic logging
logging.basicConfig(level=logging.INFO)

def main():
    # Create MinioManager instance with actual connection details
    minio_manager = MinioManager()

    # Create DataLakeAgent instance
    agent = DataLakeAgent(minio_manager)
    
    gradio_app = create_gradio_app(data_lake_agent)

    # Launch the Gradio app
    gradio_app.launch()  
    
    # Determine action to perform, here hard-coded for demonstration
    # In practice, you would get these from command line arguments or another source
    action = 'ingest'
    bucket_name = 'example_bucket'
    data = b'sample data'
    object_name = 'data.txt'
    file_path = 'schema.txt'

    # Run the agent with the action and parameters
    if action == 'ingest':
        agent.run(action, bucket_name=bucket_name, data=data, object_name=object_name)
    elif action == 'retrieve':
        agent.run(action, bucket_name=bucket_name, object_name=object_name)
    elif action == 'generate_schema':
        agent.run(action, bucket_name=bucket_name, object_name=object_name, file_path=file_path)
    elif action == 'learn_language':
        input_text = 'input text for language learning'
        agent.run(action, input=input_text)
    else:
        logging.error(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
