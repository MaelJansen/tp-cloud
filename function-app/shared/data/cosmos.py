import logging
import os
from typing import Optional, Union, Any, Dict, TypeVar, Type, List

import urllib3
from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


class Cosmos:
    """
    Cosmos class provides a convenient interface to interact with Azure Cosmos DB.
    """

    _client: CosmosClient
    _database_proxy: DatabaseProxy
    _default_container: Optional[str]

    def __init__(self, connection_string: str, database: str):
        """
        :param connection_string: The connection string to connect to the Cosmos DB.
        :param database: The name of the database to connect to.

        Initialize a Cosmos object with the given connection string and database name.

        Raises:
            AssertionError: If the connection string or database name is empty.

        Example:
            >>> connection_string = "AccountEndpoint=<your-account-endpoint>;AccountKey=<your-account-key>"
            >>> database = "my-database"
            >>> cosmos = Cosmos(connection_string, database)

        """
        assert connection_string and len(connection_string) > 0
        assert database and len(database) > 0

        kwargs = {}
        if bool(os.getenv("LOCAL_MODE", False)):
            logger.info("CosmosDB : Disable SSL verification for local mode")
            kwargs["connection_verify"] = False
            urllib3.disable_warnings()
        self._client = CosmosClient.from_connection_string(connection_string, **kwargs)
        self._database_proxy = self._client.get_database_client(database)
        self._default_container = None
        logging.getLogger("azure").setLevel(logging.WARNING)

    @classmethod
    def from_env(cls):
        """
        Create a CosmosClient instance using the environment variables.

        :return: A CosmosClient instance.
        :rtype: Cosmos
        :raises ValueError: If any of the required environment variables are not set.
        """
        for env_var in ["COSMOSDB_CONNECTION_STRING", "COSMOSDB_DATABASE"]:
            if env_var not in os.environ:
                raise ValueError(f"{env_var} environment variable is not set")
        return cls(os.environ["COSMOSDB_CONNECTION_STRING"], os.environ["COSMOSDB_DATABASE"])

    @property
    def default_container(self) -> Optional[str]:
        """
        Returns the name of the default container in the CosmosClient instance.

        :return: The name of the default container as a string, or None if no default container is set.
        """
        return self._default_container

    @default_container.setter
    def default_container(self, value: Optional[str]):
        """
        Sets the default container for the Cosmos class instance.

        :param value: The name of the default container to be set.
        :type value: Optional[str]
        """
        self._default_container = value

    def _get_container_client(self, container_name: Optional[str] = None) -> ContainerProxy:
        container = container_name or self._default_container
        if container is None:
            raise ValueError("You must provide a container or set a default one")
        return self._database_proxy.get_container_client(container)

    def upsert(self, item: Union[Dict, BaseModel], container_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upserts an item in the specified container of the Cosmos database.

        :param item: The item to be upserted. It can be either a dictionary or an instance of a BaseModel subclass.
        :param container_name: The name of the container in which the item will be upserted. If not provided, the default container is used.
        :return: A dictionary representing the upserted item.

        :raises ValueError: If no container is provided and no default container is set.
        """
        client = self._get_container_client(container_name)
        return client.upsert_item(item if isinstance(item, dict) else item.model_dump())

    def query(self, query: str, output_type: Optional[Type[T]] = None,
              container_name: Optional[str] = None,
              **kwargs) -> Union[
        List[Dict[str, Any]], List[T]]:
        """
        Executes a query on the specified container in Cosmos DB.

        :param query: The query string to be executed.
        :param partition_key: THe partition key of the object being queried.
        :param output_type: Optional. The type of the output items to be returned. If specified, each item will be
            converted into an instance of the specified output type.
        :param container_name: Optional. The name of the container to execute the query on. If not provided,
            the default container will be used.
        :param kwargs: Optional additional query options.
        :return: A list of items resulting from the query. If `output_type` is specified, each item will be
            an instance of the specified output type.
        """
        client = self._get_container_client(container_name)
        if "enable_cross_partition_query" not in kwargs:
            kwargs["enable_cross_partition_query"] = True
        items = client.query_items(query, **kwargs)
        return [item if output_type is None else output_type(**item) for item in items]

    def try_get(self, item_id: str, output_type: Optional[Type[T]] = None, container_name: Optional[str] = None) -> \
            Optional[Union[Dict[str, Any], T]]:
        """
        Retrieves an item from the Cosmos DB container.

        :param item_id: The ID of the item to retrieve.
        :param output_type: The type to cast the retrieved item to. If not provided, the item will be returned as a dictionary.
        :param container_name: The name of the container in the Cosmos DB database. If not provided, the default container will be used.
        :return: The retrieved item, cast to the specified type if provided.
        """
        client = self._get_container_client(container_name)
        items = list(client.query_items(f"SELECT * FROM c WHERE c.id = '{item_id}'", enable_cross_partition_query=True))
        return None if len(items) == 0 else items[0] if output_type is None else output_type(**items[0])

    def get(self, item_id: str, partition_key: str, output_type: Optional[Type[T]] = None,
            container_name: Optional[str] = None,
            **kwargs) -> Union[Dict[str, Any], T]:
        """
        Get an item from the Cosmos database.
        Use it if you are really sure the object exists and if you already know its partition key.
        Else, use Cosmos.try_get().

        :param item_id: The ID of the item to retrieve.
        :param partition_key: The partition key of the item.
        :param output_type: The type to deserialize the item into. Default is None.
        :param container_name: The name of the container. Default is None.
        :param kwargs: Additional options to pass to the Cosmos client.
        :return: The retrieved item in dictionary format if output_type is None,
                 otherwise, the retrieved item deserialized into the specified output_type.
        """
        client = self._get_container_client(container_name)
        item = client.read_item(item_id, partition_key, **kwargs)
        return item if output_type is None else output_type(**item)
