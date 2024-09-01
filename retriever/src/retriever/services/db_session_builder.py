from contextlib import contextmanager

from neo4j import GraphDatabase

from retriever.utilities.config import config


class DbSessionBuilder:
    def __init__(self):
        self.driver = None

    @contextmanager
    def build(self):
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
