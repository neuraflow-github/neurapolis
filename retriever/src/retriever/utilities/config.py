import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class MyConfig(BaseSettings):
    # Keep sorted
    api_url: str = Field(env="API_URL")
    datastore_dir_path: str = Field(env="DATASTORE_DIR_PATH")
    db_name: str = Field(env="DB_NAME")
    db_password: str = Field(env="DB_PASSWORD")
    db_uri: str = Field(env="DB_URI")
    db_username: str = Field(env="DB_USERNAME")

    @property
    def logs_dir_path(self) -> str:
        return os.path.join(self.datastore_dir_path, "00_logs")

    @property
    def data_dir_path(self) -> str:
        return os.path.join(self.datastore_dir_path, "10_data")

    class Config:
        env_file = ".env"
        extra = "allow"


config = MyConfig()
