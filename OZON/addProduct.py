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

def GetTovarInSite1(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["до 10 000р"]
    NamesAndIdSite = []
    for i in range(len(dictNamesPost)):
        NamesAndIdSite.append([dictNamesPost[i], dictPricePost[i]])

    return NamesAndIdSite

def GetTovarInSite2(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["Цена"]
    NamesAndIdSite = []
    for i in range(len(dictNamesPost)):
        NamesAndIdSite.append([dictNamesPost[i], dictPricePost[i]])

    return NamesAndIdSite

RECLAMA =["436172848",
"436172813",
"436172745",
"436172839",
"439897583",
"437149827",
"439898139",
"436172714",
"436172742",
"436173959",
"436172782",
"436172764",
"436173315",
"437150167",
"439897527",
"436173073",
"439897711",
"439897711",
"447800324",
"436172894",
"446348995",
"447546274",
"447546590",
"447546899",
"447567248",
"447798139",
"447800238",
"447800485",
"448162517",
"448162604",
"448892930",
"449997467",
"450016686",
"450017074",
"450017064",
"448181957"]

def IsReclama(id_prod):
    for i in RECLAMA:
        # print(str(i)+"=="+str(id_prod))
        if str(i)==str(id_prod):
            print(str(i) + "==" + str(id_prod))
            return True
    return False

def SetPoductAPI(id_prod,oldPrice,country):
    dop = 1.19
    print(id_prod)
    if IsReclama(id_prod):
       dop = dop+0.14 
    print(dop)
    # newPrice = (oldPrice + 1800) * dop
    if oldPrice<1000:
        newPrice = (oldPrice + 900)* dop
    elif oldPrice>=1000 and oldPrice<3000:
        newPrice = (oldPrice + 1100)* dop
    elif oldPrice>=3000 and oldPrice<5000:
        newPrice = (oldPrice + 1300)* dop
    elif oldPrice>=5000 and oldPrice<8000:
        newPrice = (oldPrice + 1700)* dop
    elif oldPrice>=8000 and oldPrice<11000:
        newPrice = (oldPrice + 2000)* dop
    elif oldPrice>=11000 and oldPrice<15000:
        newPrice = (oldPrice + 2500) * dop
    else:
        newPrice = (oldPrice + 1800) * dop

    print(str(oldPrice)+" - "+str(newPrice))

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
    print(r)
    # print(r.json()["result"][0]["offer_id"])
    # offerId =r.json()["result"][0]["offer_id"]
    # json = {
    #     "name_search": country
    # }
    # r = requests.post("https://api-seller.ozon.ru/v2/posting/fbs/product/country/list", headers=headers, json=json)
    # print(r.json())
    # arrCountry = r.json()["result"]
    # for i in arrCountry:
    #     if i["name"] == country:
    #         isoCode = i["country_iso_code"]
    #         break
    # print(isoCode)
    #
    #
    #
    # js ={
    #   "items": [
    #     {
    #       "attributes": [
    #         { "id": 4389,
    #           "name": "Страна-изготовитель",
    #           "description": "Выберите одно или несколько значений из списка. В xls-файле варианты заполняются через точку с запятой (;) без пробелов.",
    #           "type": "string",
    #           "is_collection": True,
    #           "is_required": False,
    #           "group_id": 0,
    #           "group_name": "",
    #           "dictionary_id": 1935,
    #           "is_aspect": False,
    #           "category_dependent": False,
    #           "values": [
    #               {
    #
    #                   "value": country
    #               }
    #           ]
    #           }
    #       ],
    #       "offer_id": offerId
    #     }
    #   ]
    # }
    # print(js)
    # r = requests.post("https://api-seller.ozon.ru/v1/product/attributes/update", json=js, headers=headers)
    # print(r.text)



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
            # print(j)
            # print(i)
            if i[0].replace(" ","")==j[0].replace(" ",""):
                print(str(i[0]))
            #     price = GetPrice(i[1])
                SetPoductAPI(i[1],j[1],i[2])
                break




def main():
    filePost1 = "Парфюмерия 16.06.2023.xlsx"
    filePost2 = "Отливанты 16.06.2023.xlsx"
    fileSite = "Файл для добавления товаров.xlsx"
    inPost1 = GetTovarInSite1(filePost1)
    inPost2 = GetTovarInSite2(filePost2)
    inPost1.extend(inPost2)
    # массив с Именами и Индификаторами товаров
    # print(inPost)
    inSite = GetTovar(fileSite) # массив с Именами
    # print(inSite)
    Ozon(inSite,inPost1)

if __name__ == '__main__':
    main()