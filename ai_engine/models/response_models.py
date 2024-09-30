from typing import List
from pydantic import BaseModel

from ai_engine.models.shared import AdItem


class PriceRecommendationResponse(BaseModel):
    RecommendedPrice: float
    RecommendedPriceCurrency: str
    RecommendedPriceLowest: float
    RecommeneddPriceHighest: float
    ProcessedAds: int

class RelatedAdsResponse(BaseModel):
    RelatedAds: List[AdItem] 