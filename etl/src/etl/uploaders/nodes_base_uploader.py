import logging
from abc import abstractmethod
from typing import Generic, List, Type, TypeVar

from etl.models.db_dict import DbDict
from etl.services.db_session_builder import db_session_builder

from .base_uploader import BaseUploader

T = TypeVar("T", bound=DbDict)


class NodesBaseUploader(BaseUploader, Generic[T]):
    def __init__(self, item_class: Type[T], node_label: str):
        super().__init__()
        self._item_class = item_class
        self._node_label = node_label

    @abstractmethod
    def _load_items(self) -> List[T]:
        pass

    def _delete_obsolete_nodes(self, db_tx, current_node_ids: List[str]):
        db_query = f"""
        MATCH (node:{self._node_label})
        WHERE NOT node.id IN $current_node_ids
        DETACH DELETE node
        """
        db_tx.run(db_query, current_node_ids=current_node_ids)

    def _update_or_create_nodes(self, db_tx, items: List[T]):
        db_query = f"""
        UNWIND $items AS item
        MERGE (node:{self._node_label} {{id: item.id}})
        SET node += item
        """
        item_db_dicts = []
        for item in items:
            item_db_dict = self._item_class.to_db_dict(item)
            item_db_dicts.append(item_db_dict)
        db_tx.run(db_query, items=item_db_dicts)

    def upload_items(self):
        logging.info(f"{self.__class__.__name__}: Started uploading")
        items = self._load_items()
        logging.info(
            f"{self.__class__.__name__}: Found {len(items)} {self._node_label} items"
        )
        current_node_ids = []
        for item in items:
            current_node_ids.append(item.id)
        with db_session_builder.build() as db_session:
            db_session.write_transaction(self._delete_obsolete_nodes, current_node_ids)
            db_session.write_transaction(self._update_or_create_nodes, items)
        logging.info(f"{self.__class__.__name__}: Finished uploading")
