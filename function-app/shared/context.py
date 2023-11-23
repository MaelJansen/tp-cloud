from .data import RawgDataCollector, Cosmos
from .utils import get_logger

logger = get_logger(__name__)


class Context:
    cosmos: Cosmos
    rawg_data_collector: RawgDataCollector

    @classmethod
    def initialize(cls):
        # TODO : Enlever le capture d'exception pour forcer le crash lorsque vous utiliserez CosmosDB
        try:
            cls.cosmos = Cosmos.from_env()
            cls.rawg_data_collector = RawgDataCollector.from_env()  # Should not be in the same try/except
        except Exception as e:
            logger.warning("Failed to initialize context")
            logger.exception(e)


Context.initialize()
