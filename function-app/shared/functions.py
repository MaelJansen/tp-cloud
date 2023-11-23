from .context import Context
from .utils import get_logger

logger = get_logger(__name__)


def import_rawg_data():
    logger.info("Starting to import rawg data")
    # TODO implémentez le code permettant d'aller chercher périodiquement de la donnée sur RAWG.io
    # Utilisez les classes RawgDataCollector (collecte de données) et Cosmos (persistence)
    # games = ...
    # for game in games:
    #     ...
    #     Context.cosmos.upsert(game)
    logger.info("Finished importing rawg data")
