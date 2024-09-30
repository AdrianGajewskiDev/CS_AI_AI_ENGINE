from ai_engine.models.response_models import PriceRecommendationResponse, RelatedAdsResponse


def combine_results(price_rec: PriceRecommendationResponse, relate_ads: RelatedAdsResponse) -> dict:
    return {
        "PriceRecommendation": price_rec.dict(),
        "RelatedAds": relate_ads.dict()
    }

   