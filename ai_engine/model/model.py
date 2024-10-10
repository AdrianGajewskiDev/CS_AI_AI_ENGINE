from ast import Tuple
import math
from typing import List
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ai_engine.logging.logger import InternalLogger
from ai_engine.models.response_models import PriceRecommendationResponse

# data = [
#    {
#       "Price":"24900",
#       "PriceCurrency":"PLN",
#       "Mileage":"214300",
#       "ProductionYear":"1990",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"137",
#       "Capacity":"2226",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-2-3benz-quatro-ID6GO98I.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjB0eWhyaWV3aXd4ODItT1RPTU9UT1BMIn0.TcSX6wNc-AJGucSpuwebGubBpTOlJao7N1ruAT1qTpU/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjB0eWhyaWV3aXd4ODItT1RPTU9UT1BMIn0.TcSX6wNc-AJGucSpuwebGubBpTOlJao7N1ruAT1qTpU/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"19800",
#       "PriceCurrency":"PLN",
#       "Mileage":"205000",
#       "ProductionYear":"1991",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"174",
#       "Capacity":"2771",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-2-8-v6-z-hiszpani-ID6GiXG9.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InhscWZtcmpjMW5sbTEtT1RPTU9UT1BMIn0.Ny0N2QnMeNmUzoQZkmtZ8SEbG2Qxmg_Msw4E7WuMDBs/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InhscWZtcmpjMW5sbTEtT1RPTU9UT1BMIn0.Ny0N2QnMeNmUzoQZkmtZ8SEbG2Qxmg_Msw4E7WuMDBs/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"7400",
#       "PriceCurrency":"PLN",
#       "Mileage":"320000",
#       "ProductionYear":"1991",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"133",
#       "Capacity":"2309",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-2-3-benz-sedan-mechaniczny-wtrysk-paliwa-ID6GGGnO.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjY3YmQybDB6azNtdjItT1RPTU9UT1BMIn0.4cyEd54dEtALvaoKuiLr8RcHzwWMNVFF0XsT-OBLjEk/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjY3YmQybDB6azNtdjItT1RPTU9UT1BMIn0.4cyEd54dEtALvaoKuiLr8RcHzwWMNVFF0XsT-OBLjEk/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"12900",
#       "PriceCurrency":"PLN",
#       "Mileage":"250000",
#       "ProductionYear":"1991",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"174",
#       "Capacity":"2771",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-v6-manual-ID6GCfyY.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6Ind2NTBnejUxcGN5dS1PVE9NT1RPUEwifQ.XGJDtQKsaX0vZg2GnEP-Vr7X75UMUU644Nd8Njn-XIg/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6Ind2NTBnejUxcGN5dS1PVE9NT1RPUEwifQ.XGJDtQKsaX0vZg2GnEP-Vr7X75UMUU644Nd8Njn-XIg/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"38000",
#       "PriceCurrency":"PLN",
#       "Mileage":"199284",
#       "ProductionYear":"1989",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"116",
#       "Capacity":"1994",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-silnik-2-3-136km-bez-rdzy-import-cygaro-super-stan-ID6G9jsN.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjBreXV3d3F0cjI3aDItT1RPTU9UT1BMIn0.UQG-iNM1UKd_rdA4IHCCacsCV5pQm56mYcXELMogqqE/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6IjBreXV3d3F0cjI3aDItT1RPTU9UT1BMIn0.UQG-iNM1UKd_rdA4IHCCacsCV5pQm56mYcXELMogqqE/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"19990",
#       "PriceCurrency":"PLN",
#       "Mileage":"101000",
#       "ProductionYear":"1993",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"174",
#       "Capacity":"2771",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-2-8-v6-174-km-lakier-wyblakniety-od-hiszpanii-0-rdzy-101-tys-km-ID6GMjuR.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImhhMm9qbTdna2lpNDMtT1RPTU9UT1BMIn0.m3YJKeK1MqB5kpQgSaPz0hLzbZQlSkRA7wB2rrwOI1Q/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImhhMm9qbTdna2lpNDMtT1RPTU9UT1BMIn0.m3YJKeK1MqB5kpQgSaPz0hLzbZQlSkRA7wB2rrwOI1Q/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"15900",
#       "PriceCurrency":"PLN",
#       "Mileage":"245000",
#       "ProductionYear":"1990",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"133",
#       "Capacity":"2309",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-2-3-benzyna-zarejestrowany-w-pl-sprawny-jezdzacy-ladna-baza-ID6FQphL.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InExZHM0eDMyaGdxbTMtT1RPTU9UT1BMIn0.pJYoM-XrH7_2SVhDU6lHYFSnDkJws9VjiNj8F29FPss/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InExZHM0eDMyaGdxbTMtT1RPTU9UT1BMIn0.pJYoM-XrH7_2SVhDU6lHYFSnDkJws9VjiNj8F29FPss/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"18900",
#       "PriceCurrency":"PLN",
#       "Mileage":"182000",
#       "ProductionYear":"1991",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"174",
#       "Capacity":"2771",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-2-8-e-quattro-4x4-1991-rok-super-stan-ID6GH4F4.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6Im5jMHlkdnpkZXR6NjEtT1RPTU9UT1BMIn0.UCfkrXeg6xDekms5sO7FssDclxNxfvq3h3E8LVLLmBg/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6Im5jMHlkdnpkZXR6NjEtT1RPTU9UT1BMIn0.UCfkrXeg6xDekms5sO7FssDclxNxfvq3h3E8LVLLmBg/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"10900",
#       "PriceCurrency":"PLN",
#       "Mileage":"173000",
#       "ProductionYear":"1992",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"174",
#       "Capacity":"2771",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-ID6Eahjo.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImN2MGsxa3hyMmprNzEtT1RPTU9UT1BMIn0.VubJiBw_n8A_Fswg0z5de3-UFYzhN325gdq2OB-Mr5I/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImN2MGsxa3hyMmprNzEtT1RPTU9UT1BMIn0.VubJiBw_n8A_Fswg0z5de3-UFYzhN325gdq2OB-Mr5I/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"11900",
#       "PriceCurrency":"PLN",
#       "Mileage":"269700",
#       "ProductionYear":"1992",
#       "FuelType":"petrol",
#       "Transmision":"manual",
#       "HorsePower":"101",
#       "Capacity":"1984",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-audi-100-2-0-e-ID6GK1r8.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InI4bWFrOTFwemYyODEtT1RPTU9UT1BMIn0.hOriyfyMCap7DLQcHwLjsrEWkFRb5uTqK0IY-JO-B6k/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InI4bWFrOTFwemYyODEtT1RPTU9UT1BMIn0.hOriyfyMCap7DLQcHwLjsrEWkFRb5uTqK0IY-JO-B6k/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    },
#    {
#       "Price":"29999",
#       "PriceCurrency":"PLN",
#       "Mileage":"142000",
#       "ProductionYear":"1992",
#       "FuelType":"petrol",
#       "Transmision":"automatic",
#       "HorsePower":"150",
#       "Capacity":"2598",
#       "AdvertisementLink":"https://www.otomoto.pl/osobowe/oferta/audi-100-2-6-v6-tylko-142-tys-km-wlasciciel-z-1933r-stan-kolekcjonerski-ID6Fg57F.html",
#       "Thumbnails":[
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImhsMGlzb2ZtbDhqbDEtT1RPTU9UT1BMIn0.PEN0QCwcMMZgHRKG8GjHxTj6FkP5a3zXrJapms3sfDQ/image;s=320x240",
#          "https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6ImhsMGlzb2ZtbDhqbDEtT1RPTU9UT1BMIn0.PEN0QCwcMMZgHRKG8GjHxTj6FkP5a3zXrJapms3sfDQ/image;s=640x480"
#       ],
#       "Source":"https://www.otomoto.pl"
#    }
# ]

# seed_data = {'Make': 'Audi', 'Model': '100', 'Generation': '', 'ProductionYear': 1991, 'Mileage': 235695, 'Capacity': 2771, 'HorsePower': 150, 'FuelType': 'petrol', 'Transmision': 'manual'}


def predict_price(data: List[dict], seed_data: dict) -> PriceRecommendationResponse:
   _lowest: list = []
   _average: list = []
   _highest: list = []
   for i in range(1):
      print(f"Predicting price {i}")
      lowest, average, highest = get_predictions(data, seed_data)
      _lowest.append(lowest)
      _average.append(average)
      _highest.append(highest)

   lowest = math.floor(sum(_lowest) / len(_lowest))
   average = math.floor(sum(_average) / len(_average))
   highest = math.floor(sum(_highest) / len(_highest))
   print(f"Lowest: {lowest}, Average: {average}, Highest: {highest}")
   return PriceRecommendationResponse(RecommendedPrice=roundup(average), RecommendedPriceCurrency="PLN", RecommendedPriceLowest=roundup(lowest), RecommendedPriceHighest=roundup(highest), ProcessedAds=len(data))


def get_predictions(resolved_data: List[dict], seed_data: dict) -> List[PriceRecommendationResponse]:
   predicted_prices = []

   for i in range(1):
      prediction = get_predicted_price(resolved_data, seed_data)
      if prediction < 0:
         continue
      predicted_prices.append(prediction)
   print(predicted_prices)
   return _analyze_prices(predicted_prices)

def get_predicted_price(resolved_data: List[dict], seed_data: dict) -> float:
   resolved_data = _transform_order(resolved_data)
   seed_data = _transform_order([seed_data])[0]
   data_frame = transform_data(resolved_data)
   data_frame = sort_data_frame_columns(data_frame)
   X, y = data_frame.drop('Price', axis=1), data_frame['Price']
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
   req = RandomForestClassifier()
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
   df = df.join(pd.get_dummies(df.Transmision, dtype=int, prefix="Transmision")).drop("Transmision", axis=1)
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

def roundup(x: float | int) -> int:
   return int(math.ceil(x / 100.0)) * 100