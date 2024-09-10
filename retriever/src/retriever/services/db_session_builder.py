from contextlib import contextmanager
from typing import Generator

from neo4j import Driver, GraphDatabase, Session

from retriever.config import config


class DbSessionBuilder:
    driver: Driver | None

    def __init__(self):
        self.driver = None

    @contextmanager
    def build(self) -> Generator[Session, None, None]:
        if self.driver is None:
            self.driver = GraphDatabase.driver(
                config.db_uri, auth=(config.db_username, config.db_password)
            )
        try:
            with self.driver.session(database=config.db_name) as session:
                yield session
        finally:
            if self.driver is not None:
                self.driver.close()
                self.driver = None


db_session_builder = DbSessionBuilder()
