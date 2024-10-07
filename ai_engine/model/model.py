from ast import Tuple
import math
from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from ai_engine.logging.logger import InternalLogger
from ai_engine.models.response_models import PriceRecommendationResponse

def predict_price(data: List[dict], seed_data: dict) -> PriceRecommendationResponse:
   _lowest: list = []
   _average: list = []
   _highest: list = []
   for i in range(25):
      print(f"Predicting price {i}")
      lowest, average, highest = get_predictions(data, seed_data)
      _lowest.append(lowest)
      _average.append(average)
      _highest.append(highest)

   lowest = math.floor(sum(_lowest) / len(_lowest))
   average = math.floor(sum(_average) / len(_average))
   highest = math.floor(sum(_highest) / len(_highest))

   return PriceRecommendationResponse(RecommendedPrice=average, RecommendedPriceCurrency="PLN", RecommendedPriceLowest=lowest, RecommendedPriceHighest=highest, ProcessedAds=len(data))


def get_predictions(resolved_data: List[dict], seed_data: dict) -> List[PriceRecommendationResponse]:
   predicted_prices = []

   for i in range(25):
      predicted_prices.append(get_predicted_price(resolved_data, seed_data))

   return _analyze_prices(predicted_prices)

def get_predicted_price(resolved_data: List[dict], seed_data: dict) -> PriceRecommendationResponse:
   resolved_data = _transform_order(resolved_data)
   seed_data = _transform_order([seed_data])[0]
   data_frame = transform_data(resolved_data)
   data_frame = sort_data_frame_columns(data_frame)
   X, y = data_frame.drop('Price', axis=1), data_frame['Price']
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
   req = LinearRegression()
   req.fit(X_train, y_train)
   prediction_data = _fill_missing_features(transform_data([seed_data], True), pd.get_dummies(data_frame))
   prediction_data = sort_data_frame_columns(prediction_data)

   return math.floor(req.predict(prediction_data)[0])

def convert_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
   columns_to_transform = ['Price', 'Mileage', 'ProductionYear', 'HorsePower', 'Capacity']
   dropped: list = []
   for column in columns_to_transform:
      if column not in df.columns:
         continue
      df[column] = df[column].astype(int)
      dropped.append(column)

   return df.dropna(subset=dropped)

def drop_not_needed(df: pd.DataFrame, drop_y: bool = False) -> pd.DataFrame:
   columns_to_drop = ['PriceCurrency', 'AdvertisementLink', 'Source', 'Thumbnails', 'Generation', 'Make', 'Model']
   InternalLogger.LogDebug(f"Dropping not needed columns, drop_y: {drop_y}")
   if drop_y:
      InternalLogger.LogDebug("Dropping Price column")
      columns_to_drop.append('Price')

   for column in columns_to_drop:
      InternalLogger.LogDebug(f"Dropping column: {column}")
      if column not in df.columns:
         continue
      InternalLogger.LogDebug(f"Dropped column: {column}")
      df = df.drop(column, axis=1)
   return df

def pre_process(df: pd.DataFrame) -> pd.DataFrame:
   # Transmision
   df["Transmision"] = df["Transmision"].apply(lambda x: 1 if x == "automatic" else 0)
   df = df.join(pd.get_dummies(df.FuelType, dtype=int, prefix="FuelType")).drop("FuelType", axis=1)

   return df

def transform_data(seed_data: List[dict], drop_y: bool = False) -> pd.DataFrame:
   data_frame = pd.DataFrame(seed_data)
   data_frame = drop_not_needed(data_frame, drop_y)
   data_frame = convert_to_numeric(data_frame)
   data_frame = pre_process(data_frame)
   return data_frame

def _fill_missing_features(data: pd.DataFrame, data_frame: pd.DataFrame) -> pd.DataFrame:
   missing_features = set(data_frame.columns) - set(data.columns)
   for feature in missing_features:
      if feature == "Price":
         continue
      data[feature] = 0
   return data

def _transform_order(data: List[dict]) -> pd.DataFrame:
   return [_model_data_transform(x) for x in data]

def _model_data_transform(data: dict) -> dict:
   return {
      "Price": data["Price"] if "Price" in data else 0,
      "PriceCurrency": data["PriceCurrency"] if "PriceCurrency" in data else "PLN",
      "Mileage": data["Mileage"],
      "ProductionYear": data["ProductionYear"],
      "FuelType": data["FuelType"],
      "Transmision": data["Transmision"],
      "HorsePower": data["HorsePower"],
      "Capacity": data["Capacity"]
   }

def sort_data_frame_columns(data: pd.DataFrame) -> pd.DataFrame:
   columns_names = data.columns.values.tolist()
   columns_names.sort()
   return data[columns_names]
   
def _analyze_prices(prices: List[int]):
   prices = [x for x in prices]
   return min(prices), math.floor(sum(prices) / len(prices)), max(prices)