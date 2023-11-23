import azure.functions as func

from .dto.game import GameDTO
from .utils import as_response, get_route_param
from ..context import Context

games_bp = func.Blueprint()


@games_bp.route(route="games", methods=["GET"])
def list_games(req: func.HttpRequest) -> func.HttpResponse:
    games = [GameDTO(id="1", name="Game 1"), GameDTO(id="2", name="Game 2")]
    return as_response(games)


@games_bp.route(route="games/{gid}", methods=["GET"])
def get_game(req: func.HttpRequest) -> func.HttpResponse:
    game_id = get_route_param(req, "gid")
    game = GameDTO(id=game_id, name=f"Game {game_id}")
    return as_response(game)
