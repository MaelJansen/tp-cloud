import os
from typing import List, Dict, Any, TypeVar, Type, Union, Optional, Generic
from urllib.parse import urljoin

import requests
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
G = TypeVar("G")


class ListResponse(Generic[T]):
    size: int
    results: List[G]

    def __init__(self, size: int, results: List[G]):
        self.size = size
        self.results = results


class RawgDataCollector:
    RAWG_API_URL = "https://api.rawg.io/api/"

    _api_key: str

    def __init__(self, api_key: str):
        self._api_key = api_key

    @classmethod
    def from_env(cls) -> "RawgDataCollector":
        """
        Create an instance of RawgDataCollector using the RAWG_API_KEY environment variable.

        :return: An instance of RawgDataCollector.
        :rtype: RawgDataCollector
        :raises ValueError: If RAWG_API_KEY environment variable is not set or empty.
        """
        api_key = os.getenv("RAWG_API_KEY")
        if not api_key or len(api_key) == 0:
            raise ValueError("RAWG_API_KEY environment variable is not set")
        return cls(api_key)

    def _request(self, url: str, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        :param url: The URL to send the request to.
        :param method: The HTTP method to use for the request. Must be either "GET" or "POST".
        :param params: Optional. Additional parameters to include in the request.

        :return: A dictionary containing the response from the API.

        """
        complete_url = urljoin(self.RAWG_API_URL, url)
        parameters = (params or {}) | {"key": self._api_key}
        match method:
            case "GET":
                return requests.get(complete_url, params=parameters).json()
            case "POST":
                return requests.post(complete_url, params=parameters).json()
            case _:
                raise ValueError(f"Unsupported method: {method}")

    def get_games(self, page: int = 1, page_size: int = 20, output_type: Optional[Type[T]] = None) -> ListResponse[
        Union[T, Dict[str, Any]]]:
        """
        Method to retrieve a list of games.
        Full arguments list can be found at https://api.rawg.io/docs/#operation/games_list

        :return: A list of rawg.Game objects representing games.
        """
        result = self._request("games", "GET", params={"page_size": page_size, "page": page})
        return ListResponse(result["count"],
                            result["results"] if output_type is None else [output_type(**x) for x in result["results"]])
