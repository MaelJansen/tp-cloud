from typing import Union, List, Any, Optional, TypeVar, Dict, Type

import azure.functions as func
from pydantic import BaseModel
import json

T = TypeVar("T", bound=BaseModel)


def as_response(data: Optional[Union[List[BaseModel], BaseModel]], status_code: int = 200) -> func.HttpResponse:
    """
    Converts the given data into a formatted HTTP response.

    :param data: The data to be converted into JSON.
    :param status_code: The HTTP status code to be set in the response. Defaults to 200.
    :return: An instance of func.HttpResponse containing the formatted JSON response.
    """
    return func.HttpResponse(
        mimetype="application/json",
        body=None if not data else json.dumps([d.model_dump() for d
                                               in data]) if isinstance(data, list) else json.dumps(data.model_dump()),
        status_code=status_code if data else 404,
    )


def get_route_param(request: func.HttpRequest, key: str) -> Optional[Any]:
    """
    Retrieves the value of a route parameter from the given `request` object.

    :param request: The `HttpRequest` object representing the incoming request.
    :param key: The key of the route parameter to retrieve.

    :return: The value of the route parameter as a string, or `None` if the parameter is not found.
    """
    return request.route_params.get(key)


def get_route_arg(request: func.HttpRequest, key: str) -> Optional[Any]:
    """
    Get the value of a route argument from the provided Http request.

    :param request: The Http request object.
    :param key: The key of the route argument to retrieve.

    :return: The value of the route argument, or None if it doesn't exist.
    """
    return request.params.get(key)


def get_body(request: func.HttpRequest, cls: Optional[Type[T]] = None) -> Optional[Union[Dict[str, Any], T]]:
    """
    Extracts the body from an Azure function HTTP request.

    :param request: The HTTP request object.
    :param cls: The optional Pydantic model to validate the body against.

    :return: The extracted body as a dictionary or an instance of the Pydantic model.
    """
    content = request.get_json()
    if cls is not None and content:
        return cls(**content)
    return content
