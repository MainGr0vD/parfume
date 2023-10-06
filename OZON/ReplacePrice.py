import requests
import pandas as pd


def GetTovarInSite(fileSite):
    df = pd.read_excel(fileSite, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Ozon ID"]
    print(dictNamesPost)
    return dictNamesPost
# https://api-seller.ozon.ru/v4/product/info/prices

def GetPrice(id_tovar):
    json={

        "filter": { "product_id": [ str(id_tovar) ], "visibility": "ALL" },
        "last_id": "",
        "limit": 100

    }
    headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
    r = requests.post('https://api-seller.ozon.ru/v4/product/info/prices', json=json, headers=headers)
    # print(r.text)
    try:
        price = r.json()["result"]["items"][0]["price"]["price"]
    except Exception as ex:
        price = 0
    return price

def SetPrice(id_tovar,price,kef,sim):
    if sim == "+":
        newPrice = float(price) + float(kef)
    elif sim =="*":
        newPrice = (float(price) * float(kef))
        newPrice = "%.4f" % round(newPrice, 0)
    else:
        newPrice = float(price)

    json={
        "prices": [
            {
                "auto_action_enabled": "UNKNOWN",
                "currency_code": "RUB",
                "old_price": '0',
                "price": str(newPrice),
                "product_id":id_tovar
            }
        ]
    }
    headers = {
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
    print(price)
    print(json)
    r = requests.post("https://api-seller.ozon.ru/v1/product/import/prices", json=json, headers=headers)
    print(r.text)


def PriceReplace(inSite,kef,sim):
    for i in inSite:
        if str(inSite.get(i))=='nan':
            continue
        price = GetPrice(int(inSite.get(i)))
        # print(price)
        if price==0:
            continue
        SetPrice(int(inSite.get(i)),price,kef,sim)


def main():
    fileSite = "Файл для изменения ценыТЕСТ2.xlsx"
    kef = 120
    sim = "+"
    inSite = GetTovarInSite(fileSite)  # массив Индификаторами товаров
    PriceReplace(inSite,kef,sim)


if __name__ == '__main__':
    main()