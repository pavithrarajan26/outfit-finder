
from typing import List, Optional

from pydantic import BaseModel, Field


class OutfitItem(BaseModel):
    """One clothing item the vision model found in the photo."""

    id: str = ""
    category: str
    color: str
    style: str
    description: str
    search_query: str
    confidence: float = Field(ge=0, le=1)


class VisionPayload(BaseModel):
    """The JSON object we ask the vision model to return."""

    items: List[OutfitItem]


class AnalyzeResponse(BaseModel):
    items: List[OutfitItem]
    source: str


class ShoppingProduct(BaseModel):
    """One product found through Google Shopping."""

    title: str
    price: Optional[str] = None
    extracted_price: Optional[float] = None
    merchant: Optional[str] = None
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    delivery: Optional[str] = None


class ShoppingResponse(BaseModel):
    """Shopping results for one clothing item."""

    query: str
    products: List[ShoppingProduct]
