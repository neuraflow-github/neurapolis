import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class MyConfig(BaseSettings):
    # Keep sorted
    azure_openai_api_key: str = Field(env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: str = Field(env="AZURE_OPENAI_ENDPOINT")
    azure_openai_resource: str = Field(env="AZURE_OPENAI_RESOURCE")
    db_name: str = Field(env="DB_NAME")
    db_password: str = Field(env="DB_PASSWORD")
    db_uri: str = Field(env="DB_URI")
    db_username: str = Field(env="DB_USERNAME")
    openai_api_key: str = Field(env="OPENAI_API_KEY")
    openai_api_version: str = Field(env="OPENAI_API_VERSION")

    class Config:
        env_file = ".env"
        extra = "allow"


config = MyConfig()
