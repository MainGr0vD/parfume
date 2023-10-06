import requests
import pandas as pd
from woocommerce import API
import urllib
import json
import re

folder_url = 'https://disk.yandex.ru/d/LWJGnftEDuIoFw'

headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }

headersSber = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"

}

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
    dictSite = newdf["ID Site"]
    dictOZON = newdf["ID OZON"]
    dictPrice = newdf["Цена"]
    for i in range(len(dictNames)):
        NamesAndIdSite.append([dictSite[i],dictOZON[i],dictNames[i],dictPrice[i] ])
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

def NameReplace(oldName):
    strCard = oldName.replace("  ", " ")
    objectML = re.search("([0-9]{0,5}ml)|([0-9]{0,5} мл)", strCard)
    strCard = strCard[:objectML.start()]
    objectPOL = re.search("(Женский)|(Мужской)|(Унисекс)", strCard)
    if objectPOL != None:
        strCard = strCard[:objectPOL.start()]
    print(strCard)
    return strCard

def GetAtributeTerms(strML):
    arrTerms = wcapi.get("products/attributes/3/terms").json()
    for i in arrTerms:
        if i["name"]==strML:
            return True
    return False

def CreateAtributeTerms( strML):

    data = {
        "name":  strML
    }

    print(wcapi.post("products/attributes/3/terms", data).json())


def UpdatePoductAPI(id,name,oldPrice,DICTCARD):
    objectML = re.search("([0-9]{0,5}ml)|([0-9]{0,5} мл)", name)
    strML = name[objectML.start():objectML.end() - 2].replace(" ", "")
    if not GetAtributeTerms(strML):
        CreateAtributeTerms(strML)
    # print(DICTCARD)
    newName = NameReplace(name)
    listCard = DICTCARD[newName]
    price = GetPrice(oldPrice,1.19)


    data = {
        "name":newName,
        "regular_price": str(price),
        "related_ids": listCard,
        "grouped_products":listCard,
        "upsell_ids":listCard,
        "type": "grouped",
        "default_attributes": {
            "name": "Объем",
            "slug": "size",
            "option": strML
        }
    }
    print(data)
    print(wcapi.put("products/"+str(id), data).json())
    # wcapi.put("products/"+str(id), data).json()

def DeletePoductAPI(id):
    print(wcapi.put("products/"+str(id), params={"force": True},data={}).json())

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
        elif i["attribute_id"] == 10289:
            d["ID OZON"] = i["values"][0]["value"]


    return d

def GetImg(jsonInfoTov):
    return jsonInfoTov["result"]["primary_image"]

def GetInfoTovar(jsonInfoTov,atrs,price,name,DICTCARD):
    name = name
    parameters = GetParameters(atrs)
    # description = GetDescription(jsonInfoTov)
    img = GetImg(jsonInfoTov)
    short_description = parameters["description"].split(".")[0]
    return {
        "OZON ID" : parameters["ID OZON"],
        "name" : name,
        "price" : str(int(price)),
        "description" : parameters["description"],
        "short_description": short_description+".",
        "image" : img,
        "ml" :  parameters["ml"],
        "cat" :  parameters["cat"],
        "structure" : parameters["structure"]
            }


def AppendProductSberAPI(tov):
    data = {
      "data": [
        {
          "attributes": [
          ],

          "categories_ids": [

          ],
          "description": tov["description"],
          "id": tov["OZON ID"],
          "images": [
            {
              "name": tov["name"]+".jpg",
              "url": tov["image"]
            }
          ],
          "items_per_pack": 1,
          "name": tov["name"],
          "pack_type": "per_pack",
          "position": 1,
          "status": "ACTIVE",
          "weight_netto": str(int(tov["ml"])/1000)
        }
      ]
    }
    r = requests.post("https://merchant-api.sbermarket.ru/api/v1/import/offers", json=data, headers=headersSber)
    print(r.text)
    data = {
      "data": [
        {
          "offer_id": tov["OZON ID"],
          "outlet_id": "12",
          "price": {
            "amount": tov["price"],
            "currency": "RUB"
          },
          "vat": "NO_VAT"
        }
      ]
    }

    p = requests.post("https://merchant-api.sbermarket.ru/api/v1/import/prices", json=data, headers=headersSber)
    print(p.text)

headerYoula = {
        "Content-Type": "application/json",
        "Authorization": "lj9K6tOUv8S30HKg2oU3oPlEl2K65E56"
    }

def AppendProductYuolaAPI(tov):
    data = {
      "category": 14,
      "description": tov["description"],
      "images": [
          tov["image"]
      ],
      "location": {
        "address": "город Москва, Варшавское шоссе, дом 122",
        "description": "Москва",
      },
      "name": tov["name"],
      "owner_id": tov["OZON ID"],
      "price": tov["price"],
      "subcategory": 1403
    }
    print(data)
    r = requests.post("https://partner-api.youla.io/products", headers=headerYoula, json=data)
    # print("Youla - " + r.text)

def GetIDYuolaAPI(id):
    r = requests.get("https://partner-api.youla.io/products/youlaId/"+id,headers=headerYoula)
    # print("Youla - " + r.text)
    dataJs = r.json()
    if "data" in dataJs:
        if dataJs["id"]!=None:
            return dataJs["id"]
    return None


def UpdatePoductYuolaAPI(tov):
    id = GetIDYuolaAPI(tov["OZON ID"])
    data = {
        "category": 14,
        "contact_ids": [
            "string"
        ],
        "description": "",
        "images": [
            tov["image"]
        ],
        "location": {
            "address": "город Москва, Варшавское шоссе, дом 122",
            "description": "Москва",
        },
        "name": tov["name"],
        "owner_id": tov["OZON ID"],
        "price": tov["price"],
        "subcategory": 1403
    }
    r = requests.post("https://partner-api.youla.io/products/"+id,headers=headerYoula,data=data)
    # print("Youla - "+ r.text)

def SetPoductAPI(id_prod,oldPrice,name,DICTCARD):
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
    # print(p.text)
    atrs = p.json()["result"][0]["attributes"]


    tov = GetInfoTovar(r.json(),atrs,oldPrice,name,DICTCARD)
    # AppendProductSberAPI(tov)
    AppendProductYuolaAPI(tov)
    # if GetIDYuolaAPI(tov["OZON ID"])==None:
    #     AppendProductYuolaAPI(tov)
    # else:
    #     UpdatePoductYuolaAPI(tov)
    return tov





def OzonToSite(inSite, inPost1,DICTCARD):
    allTovInSite = []
    # print(DICTCARD)
    deleteTovInSite = []
    for i in inSite:
        isUpdate = False
        for j in inPost1:
            if i[2].replace(" ", "") == j[0].replace(" ", ""):
                print(str(i))
                # UpdatePoductAPI(i[0],i[2],j[1],DICTCARD)
                allTovInSite.append(SetPoductAPI(i[1],i[3],i[2],DICTCARD))
                isUpdate = True
                break
        if not isUpdate:
            # DeletePoductAPI(i[0])
            deleteTovInSite.append(i[2])
        # break


    return (allTovInSite,deleteTovInSite)

def GetXSLX(allTov):
    df = pd.DataFrame(allTov)
    df.to_excel("Товары для Avito.xlsx", index=False)

def  DeleteToExcel(deleteTovInSite):
    d = {}
    d["Name"] = []
    for i in range(len(deleteTovInSite)):
        d["Name"].append(deleteTovInSite[i])

    df = pd.DataFrame(d)
    df.to_excel("Товары, которые надо удалить на авито.xlsx", index=False)


def ToExcel(allTovInSite):
    d={}
    d["Id"] = []
    d["Title"]=[]
    d["Price"] = []
    d["ImageUrls"] = []
    d["Address"] = []
    d["Description"]=[]
    d["Category"] = []
    d["GoodsType"] = []
    d["AdType"] = []
    d["Condition"] = []
    for i in range(len(allTovInSite)):
        d["Id"].append(allTovInSite[i]["OZON ID"])
        d["Title"].append(allTovInSite[i]["name"])
        d["Price"].append(allTovInSite[i]["price"])
        d["ImageUrls"].append(allTovInSite[i]["image"])
        d["Address"].append("город Москва, Варшавское шоссе, дом 122")
        d["Description"].append("Объем в ml - "+str(allTovInSite[i]["ml"])+". "+str(allTovInSite[i]["description"]))
        d["Category"].append("Красота и здоровье")
        d["GoodsType"].append("Парфюмерия")
        d["AdType"].append("Товар от производителя")
        d["Condition"].append("Новое")
    for i in d:
        print(len(d[i]),i)
    df = pd.DataFrame(d)
    df.to_excel("Товары на сайте и авито.xlsx", index=False)
    return d

def SetFiles(file_path, destination_path, yandex_token):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {"Authorization": "OAuth " + yandex_token}
    params = {"path": destination_path, "overwrite": "true"}
    response = requests.get(upload_url, headers=headers, params=params)
    href = response.json()["href"]
    with open(file_path, "rb") as file:
        upload_response = requests.put(href, files={"file": file})
    if upload_response.status_code == 201:
        print("Файл успешно загружен на Яндекс.Диск.")
    else:
        print("Ошибка при загрузке файла на Яндекс.Диск.")



def GetDictCard(inSite):
    print(inSite)
    dictCard={}

    for i in inSite:
        if i!="":
            strCard = NameReplace(i[2])
            if not strCard in dictCard:
                dictCard[strCard]= [i[0]]
            else:
                dictCard[strCard].append(i[0])
    # print(dictCard)
    return dictCard

def GetAllTov():
    allTov = []
    for i in range(1,200):
        data = {
            "page": i,
            "per_page": 100,
        }
        jsAllProd = wcapi.get("products", params=data).json()
        allTov.extend(jsAllProd)
    return allTov

def GetDubl(inSite):
    orig = []
    dubl = []
    jsAllProd=GetAllTov()

    print(len(jsAllProd))
    for i in jsAllProd:
        dublCheck = False
        for j in orig:
            if i["name"] == j[1]:
                dubl.append([i["id"],i["name"]])
                dublCheck = True
        if dublCheck == False:
            orig.append([i["id"],i["name"]])
    return dubl

def DeleteDubl(dubl):
    for i in dubl:
        print(wcapi.delete("products/"+str(i[0]), params={"force": True}).json())

def main():
    filePost1 = "Парфюмерия 03.10.2023.xlsx"
    filePost2 = "Отливанты 03.10.2023.xlsx"
    fileSite = "Товары на сайте.xlsx"
    inPost1 = GetTovarInSite1(filePost1)
    inPost2 = GetTovarInSite2(filePost2)
    inPost1.extend(inPost2)
    # массив с Именами и Индификаторами товаров
    # print(inPost)
    inSite = GetTovar(fileSite)
    print(inSite)
    DICTCARD = GetDictCard(inSite)
    # dubl = GetDubl(inSite)
    # print(dubl)
    # DeleteDubl(dubl)
    allTovInSite,deleteTovInSite = OzonToSite(inSite, inPost1,DICTCARD)
    tovForExcel = ToExcel(allTovInSite)
    DeleteToExcel(deleteTovInSite)
    GetXSLX(tovForExcel)
    file_path = "Товары на сайте и авито.xlsx"
    destination_path = "/Парфюмерия/Файл для авито.xlsx"
    yandex_token = "y0_AgAAAAARJzI4AADLWwAAAADmsooK2kCxxwyQS2qlqDCwJtJoLoAZCdI"
    SetFiles(file_path, destination_path, yandex_token)

if __name__ == '__main__':
    main()