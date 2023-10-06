import requests
import pandas as pd
import datetime


headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
country = "США"
json ={
  "name_search": country
}
r = requests.post("https://api-seller.ozon.ru/v2/posting/fbs/product/country/list", headers=headers, json=json)

arrCountry = r.json()["result"]
for i in arrCountry:
    if i["name"] == country:
        isoCode = i["country_iso_code"]
        break
print(isoCode)