import requests
import pandas as pd
import datetime

headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }

def GetZakaz():
    data = datetime.datetime.now()
    data3Day = data - datetime.timedelta(days=5)
    dataNextDay = data + datetime.timedelta(days=5)
    json ={
        "dir": "asc",
        "filter": {"cutoff_from": datetime.datetime.strftime(data3Day,"%Y-%m-%d")+"T00:00:00.359Z",
                   "cutoff_to": datetime.datetime.strftime(dataNextDay ,"%Y-%m-%d")+"T00:00:00.359Z",
                    "status": "awaiting_packaging",
                    "delivery_method_id": [648629,658515],
                    "warehouse_id":[1020000190634000]
                    },
        "limit": 1000,
        "offset": 0,
        "with": {"analytics_data": True, "barcodes": True, "financial_data": True}
    }
    allTov = []
    print(json)
    r = requests.post("https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list",headers=headers,json=json)
    print(r.text)
    js = r.json()["result"]["postings"]
    for i in js:
        mainInfo = [
            i["posting_number"],
            i["customer"]["address"]["address_tail"],
            i["customer"]["name"],
        ]
        for j in i["products"]:

            jsons = {

                "offer_id":j["offer_id"],

            }
            rs = requests.post("https://api-seller.ozon.ru/v2/product/info", headers=headers,
                              json=jsons)
            miniInfo=mainInfo
            miniInfo.append(j["name"])
            miniInfo.append(j["quantity"])
            miniInfo.append(j["price"])
            miniInfo.append(rs.json()["result"]["id"])
            allTov.append(miniInfo)
    return allTov

def GetTovarInSite1(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["до 10 000р"]
    NamesPOST=[]
    for i in range(len(dictNamesPost)):
        NamesPOST.append([dictNamesPost[i],dictPricePost[i]])
    # print(NamesAndIdSite)
    return NamesPOST

def GetTovarInSite2(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["Цена"]
    NamesPOST=[]
    for i in range(len(dictNamesPost)):
        NamesPOST.append([dictNamesPost[i],dictPricePost[i]])
    # print(NamesAndIdSite)
    return NamesPOST

# нужно два аргумента в inPost(наименование у поставщика и цена)
def GetPrice(id,inPost,inSite):
    for i in inSite:
        if i[1]==id:
            for j in inPost:
                if j[0].replace(" ","")==i[0].replace(" ",""):
                    return j[1]

# нужно имя берем из наших прайсов
def GetName(id,inPost,inSite):
    for i in inSite:
        if i[1] == id:
            return i[0]

def GetTovar(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    NamesAndIdSite = []
    dictNames = newdf["Наименование у поставщика"]
    dictPrice = newdf["ID"]
    for i in range(len(dictNames)):
        NamesAndIdSite.append([dictNames[i], dictPrice[i]])
    # print(NamesAndIdSite)
    return NamesAndIdSite

def GetXSLX(allTov,inPost,inSite):
    d ={}
    index = [i for i in range(1, len(allTov) + 1)]
    d["id"] = index
    d["OZON ID"] = [i[6] for i in allTov]
    d["Покупатель"] = [i[2] for i in allTov]
    d["Номер заказа"] = [i[0] for i in allTov]
    d["Наименование товара на OZON"] = [i[3] for i in allTov]
    d["Наименование товара у поставщика"] = [GetName(i[6],inPost,inSite) for i in allTov]
    d["Количество заказа"] = [i[4] for i in allTov]
    d["Наша цена"] = [i[5] for i in allTov]
    d["Цена у поставщика"] = [GetPrice(i[6],inPost,inSite) for i in allTov]
    d["Адрес"] = [i[1] for i in allTov]
    df = pd.DataFrame(d)
    df.to_excel("Отчет по покупкам за сегодня.xlsx", index=False)

def main():
    filePost1 = "Парфюмерия 13.06.2023.xlsx"
    filePost2 = "Отливанты 13.06.2023.xlsx"
    inPost1 = GetTovarInSite1(filePost1)  # массив с Именами и Индификаторами товаров
    inPost2 = GetTovarInSite2(filePost2)
    inPost1.extend(inPost2)
    # print(inPost1)
    fileSite = "Файл для проверки на складе.xlsx"
    inSite = GetTovar(fileSite)
    # print(inSite)
    allTov =GetZakaz()

    GetXSLX(allTov,inPost1,inSite)


if __name__ == '__main__':
    main()