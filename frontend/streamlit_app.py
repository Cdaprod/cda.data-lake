import streamlit as st
from dataclasses import dataclass
from typing import Optional, List, Dict
from data_lake_schema import (
    Cdaprod,
    ClientConnection,
    LangChainRepo,
    Repository,
    Server,
    Metastore,
    MetastoreAsset,
)

# Define your Streamlit app
def main():
    st.title("Data Lake Frontend")

    # Define your LANGCHAIN API configuration
    cdaprod_config = {
        'server': Server(ip='192.168.1.1', creds={'username': 'user', 'password': 'pass'}, connection_type='SSH'),
        'repository': 'https://github.com/Cdaprod/main-repo',
        'services': [],
        'metastore': Metastore(metastore_id='metastore1', assets={}, repository='https://github.com/Cdaprod/metastore-repo'),
    }

    # Define your repositories, clients, and assets
    repo_list = [
        RepoConfig(repo_url='https://github.com/Cdaprod/langchain-repo', apps=['app1', 'app2']),
        RepoConfig(repo_url='https://github.com/Cdaprod/other-repo', name='NonLangchainRepo'),
    ]

    client_list = [
        ClientConfig(service_name='DatabaseService', hostname='db.example.com', credentials={'username': 'user', 'password': 'pass'}),
        ClientConfig(service_name='ApiService', hostname='api.example.com', credentials={'api_key': 'key'}),
    ]

    asset_list = [
        {'asset_id': 'asset1', 'asset_type': 'table', 'location': 'http://example.com/asset1', 'schema': {'field1': 'type1', 'field2': 'type2'}},
        {'asset_id': 'asset2', 'asset_type': 'model', 'location': 'http://example.com/asset2', 'schema': {'fieldA': 'typeA', 'fieldB': 'typeB'}},
    ]

    # Instantiate the builder and build the data lake
    builder = BuildDataLake(cdaprod_config)
    cdaprod_instance = builder.build(repo_list, client_list, asset_list)

    # Display the data lake information
    st.subheader("Data Lake Configuration")
    st.write(cdaprod_instance)

# Data classes for LANGCHAIN API configuration
@dataclass
class RepoConfig:
    repo_url: str
    apps: Optional[List[str]] = None
    name: Optional[str] = None

@dataclass
class ClientConfig:
    service_name: str
    hostname: str
    credentials: Dict[str, str]

class BuildDataLake:
    def __init__(self, cdaprod_config: Dict):
        # Initialize the Cdaprod instance with its config
        self.cdaprod = Cdaprod(**cdaprod_config)

    def register_repository(self, repo_config: RepoConfig):
        if repo_config.apps is not None:  # LangChainRepo is distinguished by the presence of 'apps'
            repo_instance = LangChainRepo(repo_url=repo_config.repo_url, apps=repo_config.apps)
            self.cdaprod.services.append({'LangChainRepo': repo_instance})
        else:
            repo_instance = Repository(repo_url=repo_config.repo_url, name=repo_config.name)
            self.cdaprod.services.append({'Repository': repo_instance})

    def register_client(self, client_config: ClientConfig):
        client_instance = ClientConnection(
            service_name=client_config.service_name,
            hostname=client_config.hostname,
            credentials=client_config.credentials
        )
        self.cdaprod.services.append({'ClientConnection': client_instance})

    def register_metastore_asset(self, asset_config: Dict):
        asset_instance = MetastoreAsset(**asset_config)
        self.cdaprod.metastore.add_asset(asset_instance)

    def build(self, repo_list: List[RepoConfig], client_list: List[ClientConfig], asset_list: List[Dict]):
        for repo_config in repo_list:
            self.register_repository(repo_config)

        for client_config in client_list:
            self.register_client(client_config)

        for asset_config in asset_list:
            self.register_metastore_asset(asset_config)

        # Additional setup tasks can be added here
        # Return the fully built Cdaprod instance
        return self.cdaprod

if __name__ == "__main__":
    main()


import streamlit as st
from dataclasses import dataclass
from typing import Optional, List, Dict
from data_lake_schema import (
    Cdaprod,
    ClientConnection,
    LangChainRepo,
    Repository,
    Server,
    Metastore,
    MetastoreAsset,
)

@dataclass
class RepoConfig:
    repo_url: str
    apps: Optional[List[str]] = None
    name: Optional[str] = None

@dataclass
class ClientConfig:
    service_name: str
    hostname: str
    credentials: Dict[str, str]

class BuildDataLake:
    def __init__(self, cdaprod_config: Dict):
        # Initialize the Cdaprod instance with its config
        self.cdaprod = Cdaprod(**cdaprod_config)

    def register_repository(self, repo_config: RepoConfig):
        if repo_config.apps is not None:  # LangChainRepo is distinguished by the presence of 'apps'
            repo_instance = LangChainRepo(repo_url=repo_config.repo_url, apps=repo_config.apps)
            self.cdaprod.services.append({'LangChainRepo': repo_instance})
        else:
            repo_instance = Repository(repo_url=repo_config.repo_url, name=repo_config.name)
            self.cdaprod.services.append({'Repository': repo_instance})

    def register_client(self, client_config: ClientConfig):
        client_instance = ClientConnection(
            service_name=client_config.service_name,
            hostname=client_config.hostname,
            credentials=client_config.credentials
        )
        self.cdaprod.services.append({'ClientConnection': client_instance})

    def register_metastore_asset(self, asset_config: Dict):
        asset_instance = MetastoreAsset(**asset_config)
        self.cdaprod.metastore.add_asset(asset_instance)

    def build(self, repo_list: List[RepoConfig], client_list: List[ClientConfig], asset_list: List[Dict]):
        for repo_config in repo_list:
            self.register_repository(repo_config)

        for client_config in client_list:
            self.register_client(client_config)

        for asset_config in asset_list:
            self.register_metastore_asset(asset_config)

        # Additional setup tasks can be added here
        # Return the fully built Cdaprod instance
        return self.cdaprod

# Configuration for server, metastore, and the main repository
cdaprod_config = {
    'server': Server(ip='192.168.1.1', creds={'username': 'user', 'password': 'pass'}, connection_type='SSH'),
    'repository': 'https://github.com/Cdaprod/main-repo',
    'services': [],
    'metastore': Metastore(metastore_id='metastore1', assets={}, repository='https://github.com/Cdaprod/metastore-repo'),
}

# Configuration for repositories, clients, and assets
repo_list = [
    RepoConfig(repo_url='https://github.com/Cdaprod/langchain-repo', apps=['app1', 'app2']),
    RepoConfig(repo_url='https://github.com/Cdaprod/other-repo', name='NonLangchainRepo'),
]

client_list = [
    ClientConfig(service_name='DatabaseService', hostname='db.example.com', credentials={'username': 'user', 'password': 'pass'}),
    ClientConfig(service_name='ApiService', hostname='api.example.com', credentials={'api_key': 'key'}),
]

asset_list = [
    {'asset_id': 'asset1', 'asset_type': 'table', 'location': 'http://example.com/asset1', 'schema': {'field1': 'type1', 'field2': 'type2'}},
    {'asset_id': 'asset2', 'asset_type': 'model', 'location': 'http://example.com/asset2', 'schema': {'fieldA': 'typeA', 'fieldB': 'typeB'}},
]

# Instantiate the builder and build the data lake
builder = BuildDataLake(cdaprod_config)
cdaprod_instance = builder.build(repo_list, client_list, asset_list)

# Streamlit app
def main():
    st.title("Data Lake Frontend Interface")

    # Display the Cdaprod instance
    st.subheader("Cdaprod Instance")
    st.write(cdaprod_instance)

if __name__ == "__main__":
    main()


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


# Import necessary libraries
import streamlit as st

# Define login function
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    
    if login_button:
        # Perform authentication logic here
        if username == "admin" and password == "password":
            st.success("Login successful")
            return True  # Return True if login is successful
        else:
            st.error("Invalid username or password")
    return False  # Return False if login is unsuccessful or not attempted yet

# Define sidebar function
def sidebar():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ["Dashboard", "Search", "Upload/Download", "System Interaction"])
    
    if selected_page == "Dashboard":
        # Display dashboard
        st.write("Dashboard")
    elif selected_page == "Search":
        # Display search interface
        st.write("Search Interface")
    elif selected_page == "Upload/Download":
        # Display upload/download interface
        st.write("Upload/Download Interface")
    elif selected_page == "System Interaction":
        # Display system interaction controls
        st.write("System Interaction Controls")

# Define main function to run Streamlit app
def main():
    user_logged_in = login()
    if user_logged_in:
        sidebar()

# Check if this script is run directly and call the main function
if __name__ == "__main__":
    main()
    
    
import streamlit as st

def main():
    st.title("Data Lake Frontend Interface")

    # Input fields
    repo_url = st.text_input("Repository URL")
    apps = st.text_input("Apps (comma-separated)")
    name = st.text_input("Name")

    service_name = st.text_input("Service Name")
    hostname = st.text_input("Hostname")
    credentials = st.text_input("Credentials")

    asset_id = st.text_input("Asset ID")
    asset_type = st.text_input("Asset Type")
    location = st.text_input("Location")
    schema = st.text_input("Schema")

    # Button to register repository
    if st.button("Register Repository"):
        repo_config = {
            "repo_url": repo_url,
            "apps": apps.split(",") if apps else None,
            "name": name if name else None
        }
        # Perform the registration logic here
        register_repository(repo_config)
        st.success("Repository registered successfully!")

    # Button to register client
    if st.button("Register Client"):
        client_config = {
            "service_name": service_name,
            "hostname": hostname,
            "credentials": credentials
        }
        # Perform the registration logic here
        register_client(client_config)
        st.success("Client registered successfully!")

    # Button to register metastore asset
    if st.button("Register Metastore Asset"):
        asset_config = {
            "asset_id": asset_id,
