# cda/metastore/models.py
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from . import MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, BUCKET_NAME  # Importing global vars from __init__.py

Base = declarative_base()
engine = create_engine('sqlite:///metastore.db', echo=True)  # Or any other database
Session = scoped_session(sessionmaker(bind=engine))

class Metastore(Base):
    __tablename__ = 'metastores'
    id = Column(Integer, primary_key=True)
    metastore_id = Column(String, unique=True)
    repository_url = Column(String)
    bucket_path = Column(String)
    assets = relationship('MetastoreAsset', back_populates='metastore')

class MetastoreAsset(Base):
    __tablename__ = 'metastore_assets'
    id = Column(Integer, primary_key=True)
    asset_id = Column(String, unique=True)
    asset_type = Column(String)
    file_path = Column(String)
    schema = Column(JSON)
    metastore_id = Column(Integer, ForeignKey('metastores.id'))
    metastore = relationship('Metastore', back_populates='assets')

# Abstract Configuration Manager
class AbstractConfigManager:
    def load_configuration(self, config_name: str):
        raise NotImplementedError

    def save_configuration(self, config_name: str, config_value: dict):
        raise NotImplementedError

# SQL Configuration Manager Implementation
class SQLConfigManager(AbstractConfigManager):
    def load_configuration(self, config_name: str):
        session = Session()
        config = session.query(Configuration).filter_by(name=config_name).first()
        Session.remove()
        return config.value if config else None

    def save_configuration(self, config_name: str, config_value: dict):
        session = Session()
        config = session.query(Configuration).filter_by(name=config_name).first()
        if config:
            config.value = config_value
        else:
            new_config = Configuration(name=config_name, value=config_value)
            session.add(new_config)
        session.commit()
        Session.remove()

class Configuration(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    value = Column(JSON)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
