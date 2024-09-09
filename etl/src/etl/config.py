import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class MyConfig(BaseSettings):
    # Keep sorted
    api_url: str = Field(env="API_URL")
    azure_openai_api_key: str = Field(env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(env="AZURE_OPENAI_ENDPOINT")
    datastore_dir_path: str = Field(env="DATASTORE_DIR_PATH")
    db_name: str = Field(env="DB_NAME")
    db_password: str = Field(env="DB_PASSWORD")
    db_uri: str = Field(env="DB_URI")
    db_username: str = Field(env="DB_USERNAME")
    openai_api_key: str = Field(env="OPENAI_API_KEY")
    openai_api_version: str = Field(env="OPENAI_API_VERSION")
    unstructured_api_url: str = Field(env="UNSTRUCTURED_API_URL")

    @property
    def logs_dir_path(self) -> str:
        return os.path.join(self.datastore_dir_path, "00_logs")

    @property
    def data_dir_path(self) -> str:
        return os.path.join(self.datastore_dir_path, "10_data")

    @property
    def temp_dir_path(self) -> str:
        return os.path.join(self.datastore_dir_path, "20_temp")

    class Config:
        env_file = ".env"
        extra = "allow"


config = MyConfig()
