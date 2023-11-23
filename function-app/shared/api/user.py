import azure.functions as func

from .dto.user import UserDTO
from .utils import as_response, get_body

users_bp = func.Blueprint()


@users_bp.route(route="users", methods=["POST"])
def register(req: func.HttpRequest) -> func.HttpResponse:
    user = get_body(req, cls=UserDTO)
    return as_response(user)
