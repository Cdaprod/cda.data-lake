import streamlit as st
from DataLakeAgent import DataLakeAgent
from DynamicToolStorage import MinioManager

st.title('Data Lake Management System')

bucket_name = st.sidebar.text_input('Bucket Name')
data = st.sidebar.text_area('Data to Ingest')
object_name = st.sidebar.text_input('Object Name for Ingestion')
action = st.sidebar.selectbox('Choose Action', ['ingest', 'retrieve'])

minio_manager = MinioManager()
agent = DataLakeAgent(minio_manager)

if st.sidebar.button('Execute'):
    if action == 'ingest':
        response = agent.run('ingest', bucket_name=bucket_name, data=data.encode(), object_name=object_name)
        st.write('Ingestion Response:', response)
    elif action == 'retrieve':
        data = agent.run('retrieve', bucket_name=bucket_name, object_name=object_name)
        st.write('Retrieved Data:', data)

st.sidebar.write('Please enter the details and select an action to perform.')

if __name__ == "__main__":
    st.mainloop()
