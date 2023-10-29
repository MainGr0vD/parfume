# Импорт необходимых библиотек
import requests  # Импорт модуля для выполнения HTTP-запросов
import pandas as pd  # Импорт библиотеки для работы с данными в формате таблиц Excel
from woocommerce import API  # Импорт класса API для взаимодействия с WooCommerce
import urllib  # Импорт для различных операций с URL
import json  # Импорт для работы с JSON-данными
import re  # Импорт для работы с регулярными выражениями

# URL-адрес папки на Yandex.Disk
folder_url = 'https://disk.yandex.ru/d/LWJGnftEDuIoFw'

# Заголовки для запросов к API
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

# Инициализация объекта для взаимодействия с API WooCommerce
wcapi = API(
    url="https://reginaparfum.ru",
    consumer_key="ck_e1f86d878c9f23199f87c6c59db9a014c3046a0d",
    consumer_secret="cs_105a48b97b242e976f5a0f039015d71e08f9e065",
    wp_api=True,
    version="wc/v2"
)

# Функция GetTovar для извлечения информации о товарах из файла Excel
def GetTovar(file):
    # Чтение данных из файла Excel и преобразование в словарь
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    NamesAndIdSite = []
    # Извлечение данных о товарах из различных столбцов и добавление в список списков
    dictNames = newdf["Наименование"]
    dictSite = newdf["ID Site"]
    dictOZON = newdf["ID OZON"]
    dictPrice = newdf["Цена"]
    for i in range(len(dictNames)):
        NamesAndIdSite.append([dictSite[i], dictOZON[i], dictNames[i], dictPrice[i]])
    return NamesAndIdSite

# Функция GetTovarInSite1 для извлечения информации о товарах на сайте из файла Excel
def GetTovarInSite1(file):
    # Чтение данных из файла Excel и преобразование в словарь
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    NamesAndIdSite = []
    # Извлечение данных о товарах на сайте из различных столбцов и добавление в список списков
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["до 10 000р"]
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

def CreateAtributeTerms(strML):
    """
    Создает новый атрибут по его названию.
    """
    data = {
        "name": strML
    }
    print(wcapi.post("products/attributes/3/terms", data).json())

def UpdatePoductAPI(id, name, oldPrice, DICTCARD):
    """
    Обновляет информацию о продукте через API.
    """
    objectML = re.search("([0-9]{0,5}ml)|([0-9]{0,5} мл)", name)
    strML = name[objectML.start():objectML.end() - 2].replace(" ", "")
    if not GetAtributeTerms(strML):
        CreateAtributeTerms(strML)
    
    newName = NameReplace(name)
    listCard = DICTCARD[newName]
    price = GetPrice(oldPrice, 1.19)

    data = {
        "name": newName,
        "regular_price": str(price),
        "related_ids": listCard,
        "grouped_products": listCard,
        "upsell_ids": listCard,
        "type": "grouped",
        "default_attributes": {
            "name": "Объем",
            "slug": "size",
            "option": strML
        }
    }
    print(data)
    print(wcapi.put("products/" + str(id), data).json())

def DeletePoductAPI(id):
    """
    Удаляет информацию о продукте через API.
    """
    print(wcapi.put("products/" + str(id), params={"force": True}, data={}).json())

def GetParameters(atrs):
    """
    Получает параметры продукта из атрибутов.
    """
    d = {}
    d["ml"] = 0
    for i in atrs:
        if i["attribute_id"] == 8163:
            d["ml"] = i["values"][0]["value"]
        elif i["attribute_id"] == 4191:
            d["description"] = i["values"][0]["value"]
        elif i["attribute_id"] == 9461:
            d["cat"] = i["values"][0]["value"]
        elif i["attribute_id"] == 8050:
            d["structure"] = i["values"][0]["value"]
        elif i["attribute_id"] == 10289:
            d["ID OZON"] = i["values"][0]["value"]
    return d
    
def GetImg(jsonInfoTov):
    """
    Возвращает ссылку на основное изображение из JSON информации о товаре.
    """
    return jsonInfoTov["result"]["primary_image"]

def GetInfoTovar(jsonInfoTov, atrs, price, name, DICTCARD):
    """
    Формирует информацию о товаре на основе переданных данных.
    """
    name = name
    parameters = GetParameters(atrs)
    # description = GetDescription(jsonInfoTov)
    img = GetImg(jsonInfoTov)
    short_description = parameters["description"].split(".")[0]
    return {
        "OZON ID": parameters["ID OZON"],
        "name": name,
        "price": str(int(price)),
        "description": parameters["description"],
        "short_description": short_description + ".",
        "image": img,
        "ml": parameters["ml"],
        "cat": parameters["cat"],
        "structure": parameters["structure"]
    }

def AppendProductSberAPI(tov):
    """
    Добавляет информацию о товаре в SberMarket API.
    """
    data = {
        "data": [
            {
                "attributes": [],
                "categories_ids": [],
                "description": tov["description"],
                "id": tov["OZON ID"],
                "images": [{
                    "name": tov["name"] + ".jpg",
                    "url": tov["image"]
                }],
                "items_per_pack": 1,
                "name": tov["name"],
                "pack_type": "per_pack",
                "position": 1,
                "status": "ACTIVE",
                "weight_netto": str(int(tov["ml"]) / 1000)
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
    """
    Добавляет информацию о товаре в API Youla.
    """
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
    """
    Получает идентификатор товара из API Youla по его идентификатору.
    """
    r = requests.get("https://partner-api.youla.io/products/youlaId/" + id, headers=headerYoula)
    # print("Youla - " + r.text)
    dataJs = r.json()
    if "data" in dataJs:
        if dataJs["id"] is not None:
            return dataJs["id"]
    return None

def UpdatePoductYuolaAPI(tov):
    """
    Обновляет информацию о товаре в API Youla.
    """
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
    r = requests.post("https://partner-api.youla.io/products/" + id, headers=headerYoula, data=data)

    # print("Youla - "+ r.text)

def SetPoductAPI(id_prod, oldPrice, name, DICTCARD):
    """
    Получает информацию о товаре, анализирует её и добавляет/обновляет информацию в API различных платформ (SberMarket, Youla).
    """
    data = {
        "product_id": id_prod,
    }
    r = requests.post("https://api-seller.ozon.ru/v2/product/info", json=data, headers=headers)

    data = {
        "filter": {
            "product_id": [str(id_prod)],
            "visibility": "ALL"
        },
        "limit": 100,
        "last_id": "okVsfA==«",
        "sort_dir": "ASC"
    }
    p = requests.post("https://api-seller.ozon.ru/v3/products/info/attributes", json=data, headers=headers)
    atrs = p.json()["result"][0]["attributes"]

    tov = GetInfoTovar(r.json(), atrs, oldPrice, name, DICTCARD)
    AppendProductSberAPI(tov)
    AppendProductYuolaAPI(tov)
    return tov

def OzonToSite(inSite, inPost1, DICTCARD):
    """
    Обрабатывает товары и информацию о них, взаимодействуя с различными API.
    """
    allTovInSite = []
    deleteTovInSite = []
    for i in inSite:
        isUpdate = False
        for j in inPost1:
            if i[2].replace(" ", "") == j[0].replace(" ", ""):
                UpdatePoductAPI(i[0], i[2], j[1], DICTCARD)
                allTovInSite.append(SetPoductAPI(i[1], i[3], i[2], DICTCARD))
                isUpdate = True
                break
        if not isUpdate:
            DeletePoductAPI(i[0])
            deleteTovInSite.append(i[2])
    return (allTovInSite, deleteTovInSite)

def GetXSLX(allTov):
    """
    Создает файл Excel на основе переданной информации о товарах.
    """
    df = pd.DataFrame(allTov)
    df.to_excel("Товары для Avito.xlsx", index=False)

def DeleteToExcel(deleteTovInSite):
    """
    Создает файл Excel для товаров, которые требуется удалить из Avito на основе переданной информации.
    """
    d = {"Name": deleteTovInSite}
    df = pd.DataFrame(d)
    df.to_excel("Товары, которые надо удалить на авито.xlsx", index=False)

def ToExcel(allTovInSite):
    """
    Создает Excel-файл на основе информации о товарах для сайта и Avito.
    """
    d = {
        "Id": [item["OZON ID"] for item in allTovInSite],
        "Title": [item["name"] for item in allTovInSite],
        "Price": [item["price"] for item in allTovInSite],
        "ImageUrls": [item["image"] for item in allTovInSite],
        "Address": ["город Москва, Варшавское шоссе, дом 122"] * len(allTovInSite),
        "Description": [f"Объем в ml - {item['ml']}. {item['description']}" for item in allTovInSite],
        "Category": ["Красота и здоровье"] * len(allTovInSite),
        "GoodsType": ["Парфюмерия"] * len(allTovInSite),
        "AdType": ["Товар от производителя"] * len(allTovInSite),
        "Condition": ["Новое"] * len(allTovInSite)
    }

    df = pd.DataFrame(d)
    df.to_excel("Товары на сайте и авито.xlsx", index=False)
    return d

def SetFiles(file_path, destination_path, yandex_token):
    """
    Загружает файл на Яндекс.Диск.
    """
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
    """
    Создает словарь карточек товаров для их группировки.
    """
    dictCard = {}
    for i in inSite:
        if i != "":
            strCard = NameReplace(i[2])
            if strCard not in dictCard:
                dictCard[strCard] = [i[0]]
            else:
                dictCard[strCard].append(i[0])
    return dictCard

def GetAllTov():
    """
    Получает все товары из API.
    """
    allTov = []
    for i in range(1, 200):
        data = {"page": i, "per_page": 100}
        jsAllProd = wcapi.get("products", params=data).json()
        allTov.extend(jsAllProd)
    return allTov

def GetDubl(inSite):
    """
    Ищет дубликаты товаров.
    """
    orig = []
    dubl = []
    jsAllProd = GetAllTov()

    for i in jsAllProd:
        dublCheck = False
        for j in orig:
            if i["name"] == j[1]:
                dubl.append([i["id"], i["name"]])
                dublCheck = True
        if not dublCheck:
            orig.append([i["id"], i["name"]])
    return dubl


def DeleteDubl(dubl):
    """
    Удаляет дубликаты товаров.
    """
    for i in dubl:
        print(wcapi.delete("products/"+str(i[0]), params={"force": True}).json())

def main():
    filePost1 = "Парфюмерия 09.10.2023.xlsx"
    filePost2 = "Отливанты 09.10.2023.xlsx"
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