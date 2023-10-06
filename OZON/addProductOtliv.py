import requests
import pandas as pd

headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }

def GetTovar(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    NamesAndIdSite = []
    dictNames = newdf["Наименование"]
    dictPrice = newdf["Ozon ID"]
    dictCountry = newdf["Страна"]
    for i in range(len(dictNames)):
        NamesAndIdSite.append([dictNames[i], dictPrice[i],dictCountry[i]])
    # print(NamesAndIdSite)
    return NamesAndIdSite

def GetTovarInSite(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["Цена"]
    NamesAndIdSite = []
    for i in range(len(dictNamesPost)):
        NamesAndIdSite.append([dictNamesPost[i], dictPricePost[i]])

    return NamesAndIdSite

def SetPoductAPI(id_prod,oldPrice):
    if oldPrice < 1000:
        newPrice = oldPrice * 1.19 + 1100
    elif oldPrice >= 1000 and oldPrice < 3000:
        newPrice = oldPrice * 1.19 + 1300
    elif oldPrice >= 3000 and oldPrice < 5000:
        newPrice = oldPrice * 1.19 + 1500
    elif oldPrice >= 5000 and oldPrice < 8000:
        newPrice = oldPrice * 1.19 + 1800
    elif oldPrice >= 8000 and oldPrice < 11000:
        newPrice = oldPrice * 1.19 + 2000
    elif oldPrice >= 11000 and oldPrice < 15000:
        newPrice = oldPrice * 1.19 + 2500
    else:
        newPrice = oldPrice * 1.19 + 1800

    newPrice = "%.4f" % round(newPrice, 0)
    json = {
        "prices": [
            {
                "auto_action_enabled": "UNKNOWN",
                "currency_code": "RUB",
                "old_price": '0',
                "price": str(newPrice),
                "product_id": id_prod
            }
        ]
    }
    r = requests.post("https://api-seller.ozon.ru/v1/product/import/prices", json=json, headers=headers)
    print(r.text)
    data = {
        "stocks": [
                {
                "product_id": id_prod,
                "stock": 9000
                }
            ]
        }
    print(data)
    r = requests.post("https://api-seller.ozon.ru/v1/product/import/stocks", json=data, headers=headers)
    print(r.text)

def GetPrice(id_tovar):
    json={

        "filter": { "product_id": [ str(id_tovar) ], "visibility": "ALL" },
        "last_id": "",
        "limit": 100

    }

    r = requests.post('https://api-seller.ozon.ru/v4/product/info/prices', json=json, headers=headers)
    # print(r.text)
    try:
        price = r.json()["result"]["items"][0]["price"]["price"]
    except Exception as ex:
        price = 0
    return price

def Ozon(inSite,inPost):
    for i in inSite:
        for j in inPost:
            # print(j[0].replace("  "," "),end=" - ")
            # print(i[0].replace("  "," "))
            if i[0].replace(" ","")==j[0].replace(" ",""):
                print(str(i[0]))
            #     price = GetPrice(i[1])
                SetPoductAPI(i[1],j[1] )
                break



def main():
    filePost = "Отливанты 05.06.2023.xlsx"
    fileSite = "Файл для добавления товаров.xlsx"
    inPost = GetTovarInSite(filePost) # массив с Именами и Индификаторами товаров
    # print(inPost)
    inSite = GetTovar(fileSite) # массив с Именами
    # print(inSite)
    Ozon(inSite,inPost)

if __name__ == '__main__':
    main()