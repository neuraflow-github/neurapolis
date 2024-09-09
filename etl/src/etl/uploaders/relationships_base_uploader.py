import logging
from abc import abstractmethod
from typing import Dict, List

from etl.services.db_session_builder import db_session_builder

from .base_uploader import BaseUploader


class RelationshipsBaseUploader(BaseUploader):
    def __init__(
        self,
        start_node_name: str,
        end_node_name: str,
        relationship_name: str,
    ):
        super().__init__()
        self.start_node_name = start_node_name
        self.end_node_name = end_node_name
        self.relationship_name = relationship_name

    @abstractmethod
    def _get_pairs(self) -> List[Dict[str, str]]:
        pass

    def _update_or_create_relationships(self, db_tx, pairs):
        db_query = f"""
        UNWIND $pairs AS relationship_pair
        MATCH (start_node:{self.start_node_name} {{id: relationship_pair.start_id}})
        MATCH (end_node:{self.end_node_name} {{id: relationship_pair.end_id}})
        MERGE (start_node)-[r:{self.relationship_name}]->(end_node)
        """
        db_tx.run(db_query, pairs=pairs)

    def upload_items(self):
        logging.info(
            f"{self.__class__.__name__}: Started uploading {self.relationship_name} relationships..."
        )
        pairs = self._get_pairs()
        logging.info(
            f"{self.__class__.__name__}: Found {len(pairs)} {self.relationship_name} relationships"
        )
        with db_session_builder.build() as db_session:
            db_session.write_transaction(self._update_or_create_relationships, pairs)
        logging.info(
            f"{self.__class__.__name__}: Finished uploading {self.relationship_name} relationships"
        )
