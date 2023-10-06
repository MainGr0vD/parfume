import requests
import pandas as pd
from woocommerce import API

wcapi = API(
    url="https://parfumlight.ru",
    consumer_key="ck_a0c80b91327ff3740cdb6124dc68859e1bf46480",
    consumer_secret="cs_ab2d81ce9112540343a325b6c6d61474bc18667d",
    wp_api=True,
    version="wc/v2"
)

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

headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }

def GetPrice(oldPrice,dop):
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
    return newPrice

def GetParameters(atrs):
    d = {}
    d["ml"] = 0
    for i in atrs:

        if i["attribute_id"] == 8163:
            d["ml"]=i["values"][0]["value"]
        elif i["attribute_id"] == 4191:
            d["description"]=i["values"][0]["value"]
        elif i["attribute_id"] == 9461:
            d["cat"]=i["values"][0]["value"]
        elif i["attribute_id"] == 8050:
            d["structure"]=i["values"][0]["value"]

    return d

def GetImg(jsonInfoTov):
    return jsonInfoTov["result"]["primary_image"]

def GetInfoTovar(jsonInfoTov,atrs,oldPrice,name,id_prod):
    name = name
    dop = 1.19
    price = GetPrice(oldPrice,dop)
    parameters = GetParameters(atrs)
    # description = GetDescription(jsonInfoTov)
    print(jsonInfoTov)
    img = GetImg(jsonInfoTov)
    short_description = parameters["description"].split(".")[0]
    return {
        "id" : id_prod,
        "name" : name,
        "price" : price,
        "description" : parameters["description"],
        "short_description": short_description+".",
        "image" : img,
        "ml" :  parameters["ml"],
        "cat" :  parameters["cat"],
        "structure" : parameters["structure"]
            }

def GetCat(cat):
    if cat == "Парфюмерная вода мужская":
        return 20
    elif cat == "Парфюмерная вода женская":
        return 29
    elif cat == "Туалетная вода мужская":
        return 20
    elif cat == "Туалетная вода женская":
        return 29
    elif cat == "Духи женские":
        return 29
    elif cat == "Духи мужские":
        return 20
    elif cat == "Одеколон мужской":
        return 20
    elif cat == "Одеколон женский":
        return 29


def ToWoocommerce(tov):
    data = {
        "name": tov["name"],
        "type": "simple",
        "regular_price": str(int(tov["price"])),
        "description": tov["description"],
        "short_description": tov["short_description"],
        "categories": [
            {
                "id": GetCat(tov["cat"])
            },
        ],
        "images": [
            {
                "src": tov["image"],
                "position": 0
            }
        ]
    }
    print(data)
    jsonSite = wcapi.post("products", data).json()
    print(jsonSite)
    return (jsonSite["id"],jsonSite["name"],tov["id"],tov["price"])

def SetPoductAPI(id_prod,oldPrice,name):
    data = {
        "product_id":id_prod,
    }
    r = requests.post("https://api-seller.ozon.ru/v2/product/info", json=data, headers=headers)

    data = {
        "filter": {
            "product_id": [
                str(id_prod)
            ],
            "visibility": "ALL"
        },
        "limit": 100,
        "last_id": "okVsfA==«",
        "sort_dir": "ASC"
    }
    p = requests.post("https://api-seller.ozon.ru/v3/products/info/attributes", json=data, headers=headers)
    atrs = p.json()["result"][0]["attributes"]

    print(p.text)
    tov = GetInfoTovar(r.json(),atrs,oldPrice,name,id_prod)

    return ToWoocommerce(tov)

def OzonToSite(inSite, inPost1):
    allTovInSite = []
    for i in inSite:
        for j in inPost1:
            # print(j)
            # print(i)
            if i[0].replace(" ", "") == j[0].replace(" ", ""):
                print(str(i[0]))
                #     price = GetPrice(i[1])

                allTovInSite.append(SetPoductAPI(i[1], j[1],i[0]))
                break
    return allTovInSite

def GetXSLX(allTov):
    d ={}
    d["id"] = [i for i in range(1, len(allTov) + 1)]
    d["ID Site"] = [i[0] for i in allTov]
    d["ID OZON"] = [i[2] for i in allTov]
    d["Наименование"] = [i[1] for i in allTov]
    d["Цена"] = [i[3] for i in allTov]
    df = pd.DataFrame(d)
    df.to_excel("Товары на сайте.xlsx", index=False)

def main():
    filePost1 = "Парфюмерия 16.06.2023.xlsx"
    filePost2 = "Отливанты 16.06.2023.xlsx"
    fileSite = "Файл для добавления товаров.xlsx"
    inPost1 = GetTovarInSite1(filePost1)
    inPost2 = GetTovarInSite2(filePost2)
    inPost1.extend(inPost2)
    # массив с Именами и Индификаторами товаров
    # print(inPost)
    inSite = GetTovar(fileSite)
    allTovInSite = OzonToSite(inSite, inPost1)
    GetXSLX(allTovInSite)

if __name__ == '__main__':
    main()