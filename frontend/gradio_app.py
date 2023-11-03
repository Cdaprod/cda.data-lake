import gradio as gr
from DataLakeAgent import DataLakeAgent
from DynamicToolStorage import MinioManager

def ingest_data(bucket_name, data, object_name):
    minio_manager = MinioManager()
    agent = DataLakeAgent(minio_manager)
    response = agent.run('ingest', bucket_name=bucket_name, data=data, object_name=object_name)
    return response

def retrieve_data(bucket_name, object_name):
    minio_manager = MinioManager()
    agent = DataLakeAgent(minio_manager)
    data = agent.run('retrieve', bucket_name=bucket_name, object_name=object_name)
    return data

ingest_interface = gr.Interface(
    ingest_data,
    [gr.Textbox(label="Bucket Name"), gr.Textbox(label="Data"), gr.Textbox(label="Object Name")],
    outputs="text",
    title="Data Ingestion",
    description="Upload data to the data lake."
)

retrieve_interface = gr.Interface(
    retrieve_data,
    [gr.Textbox(label="Bucket Name"), gr.Textbox(label="Object Name")],
    outputs="text",
    title="Data Retrieval",
    description="Retrieve data from the data lake."
)

if __name__ == "__main__":
    ingest_interface.launch()
    retrieve_interface.launch()
