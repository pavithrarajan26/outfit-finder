
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

import config
from schemas import ShoppingProduct, ShoppingResponse


class ShoppingError(Exception):
    pass


def search_products(query: str, limit: int = 10) -> ShoppingResponse:
    """Search Google Shopping for similar products in the US."""

    if not config.SERPAPI_KEY:
        raise ShoppingError("SerpApi key is missing. Check your backend .env file.")

    if not query.strip():
        raise ShoppingError("Please provide a shopping search query.")

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": config.SERPAPI_KEY,
        "gl": "us",
        "hl": "en",
        "google_domain": "google.com",
    }

    url = "https://serpapi.com/search.json?" + urlencode(params)

    try:
        with urlopen(url, timeout=25) as response:
            data: dict[str, Any] = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        raise ShoppingError(
            f"Shopping provider returned an error: HTTP {error.code}."
        ) from error
    except (URLError, TimeoutError) as error:
        raise ShoppingError(
            "Shopping search timed out. Please try again."
        ) from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ShoppingError("Could not read the shopping search results.") from error

    if data.get("error"):
        raise ShoppingError(str(data["error"]))

    products = []

    for item in data.get("shopping_results", []):
        products.append(
            ShoppingProduct(
                title=item.get("title", "Untitled product"),
                price=item.get("price"),
                extracted_price=item.get("extracted_price"),
                merchant=item.get("source"),
                product_url=item.get("product_link") or item.get("link"),
                image_url=item.get("thumbnail"),
                rating=item.get("rating"),
                reviews=item.get("reviews"),
                delivery=item.get("delivery"),
            )
        )

    # Put products with known prices first, from cheapest to most expensive.
    products.sort(
        key=lambda product: (
            product.extracted_price is None,
            product.extracted_price
            if product.extracted_price is not None
            else float("inf"),
        )
    )

    return ShoppingResponse(
        query=query,
        products=products[:limit],
    )
