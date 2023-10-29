import requests  # Импорт модуля для выполнения HTTP-запросов
import pandas as pd  # Импорт библиотеки для работы с данными
from woocommerce import API  # Импорт класса API для взаимодействия с WooCommerce

# Инициализация объекта для взаимодействия с API WooCommerce
wcapi = API(
    url="https://reginaparfum.ru",
    consumer_key="ck_e1f86d878c9f23199f87c6c59db9a014c3046a0d",
    consumer_secret="cs_105a48b97b242e976f5a0f039015d71e08f9e065",
    wp_api=True,
    version="wc/v2"
)

def GetTovar(file):
    """
    Функция для получения информации о товарах из файла Excel.
    Читает данные из файла и преобразует их в список списков для обработки.
    """
    df = pd.read_excel(file, engine='openpyxl')  # Чтение данных из Excel в DataFrame
    newdf = df.to_dict()  # Преобразование DataFrame в словарь
    dictNamesAndId = newdf["Наименование"]
    dictPrice = newdf["Ozon ID"]
    dictCountry = newdf["Страна"]
    NamesAndIdSite = []
    for i in range(len(dictNamesAndId)):
        # Создание списка списков с информацией о товарах
        NamesAndIdSite.append([dictNamesAndId[i], dictPrice[i], dictCountry[i]])
    return NamesAndIdSite  # Возвращение списка списков с информацией о товарах

def GetTovarInSite1(file):
    """
    Функция для получения информации о товарах (вариант 1) из файла Excel.
    Читает данные из файла и преобразует их в список списков для обработки.
    """
    df = pd.read_excel(file, engine='openpyxl')  # Чтение данных из Excel в DataFrame
    newdf = df.to_dict()  # Преобразование DataFrame в словарь
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["до 10 000р"]
    NamesAndIdSite = []
    for i in range(len(dictNamesPost)):
        # Создание списка списков с информацией о товарах (вариант 1)
        NamesAndIdSite.append([dictNamesPost[i], dictPricePost[i]])
    return NamesAndIdSite  # Возвращение списка списков с информацией о товарах (вариант 1)

def GetTovarInSite2(file):
    """
    Функция для получения информации о товарах (вариант 2) из файла Excel.
    Читает данные из файла и преобразует их в список списков для обработки.
    """
    df = pd.read_excel(file, engine='openpyxl')  # Чтение данных из Excel в DataFrame
    newdf = df.to_dict()  # Преобразование DataFrame в словарь
    dictNamesPost = newdf["Наименование"]
    dictPricePost = newdf["Цена"]
    NamesAndIdSite = []
    for i in range(len(dictNamesPost)):
        # Создание списка списков с информацией о товарах (вариант 2)
        NamesAndIdSite.append([dictNamesPost[i], dictPricePost[i]])
    return NamesAndIdSite  # Возвращение списка списков с информацией о товарах (вариант 2)

headers = {
    "Content-Type": "application/json",
    "Client-Id": "819970",
    "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
}

def GetPrice(oldPrice, dop):
    """
    Функция для вычисления новой цены товара на основе старой цены и дополнительного коэффициента.
    """
    if oldPrice < 1000:
        newPrice = (oldPrice + 900) * dop
    elif 1000 <= oldPrice < 3000:
        newPrice = (oldPrice + 1100) * dop
    elif 3000 <= oldPrice < 5000:
        newPrice = (oldPrice + 1300) * dop
    elif 5000 <= oldPrice < 8000:
        newPrice = (oldPrice + 1700) * dop
    elif 8000 <= oldPrice < 11000:
        newPrice = (oldPrice + 2000) * dop
    elif 11000 <= oldPrice < 15000:
        newPrice = (oldPrice + 2500) * dop
    else:
        newPrice = (oldPrice + 1800) * dop
    return newPrice  # Возвращение новой цены товара

def GetParameters(atrs):
    """
    Функция для получения параметров товара из списка атрибутов.
    """
    d = {"ml": 0}
    for i in atrs:
        if i["attribute_id"] == 8163:
            d["ml"] = i["values"][0]["value"]
        elif i["attribute_id"] == 4191:
            d["description"] = i["values"][0]["value"]
        elif i["attribute_id"] == 9461:
            d["cat"] = i["values"][0]["value"]
        elif i["attribute_id"] == 8050:
            d["structure"] = i["values"][0]["value"]
    return d  # Возвращение словаря с параметрами товара

def GetImg(jsonInfoTov):
    """
    Функция для получения ссылки на изображение товара из JSON-информации о товаре.
    """
    return jsonInfoTov["result"]["primary_image"]  # Возвращение ссылки на изображение товара


def GetInfoTovar(jsonInfoTov, atrs, oldPrice, name, id_prod):
    """
    Функция для получения информации о товаре на основе JSON-данных, атрибутов товара, старой цены, названия и ID.
    """
    name = name
    dop = 1.19
    price = GetPrice(oldPrice, dop)
    parameters = GetParameters(atrs)
    img = GetImg(jsonInfoTov)
    short_description = parameters["description"].split(".")[0]
    return {
        "id": id_prod,
        "name": name,
        "price": price,
        "description": parameters["description"],
        "short_description": short_description + ".",
        "image": img,
        "ml": parameters["ml"],
        "cat": parameters["cat"],
        "structure": parameters["structure"]
    }

def GetCat(cat):
    """
    Функция для определения категории товара на основе наименования категории.
    """
    if cat == "Парфюмерная вода мужская":
        return 20
    # ... (продолжение для других категорий)

def ToWoocommerce(tov):
    """
    Функция для загрузки товара в WooCommerce.
    """
    data = {
        "name": tov["name"],
        "type": "simple",
        "regular_price": str(int(tov["price"])),
        "description": tov["description"],
        "short_description": tov["short_description"],
        "categories": [
            {"id": GetCat(tov["cat"])}
        ],
        "images": [
            {"src": tov["image"], "position": 0}
        ]
    }
    jsonSite = wcapi.post("products", data).json()
    return (jsonSite["id"], jsonSite["name"], tov["id"], tov["price"])

def SetPoductAPI(id_prod, oldPrice, name):
    """
    Функция для настройки продукта через API.
    """
    # (ваш код)

def OzonToSite(inSite, inPost1):
    """
    Функция для переноса товаров с Ozon на сайт.
    """
    allTovInSite = []
    for i in inSite:
        for j in inPost1:
            if i[0].replace(" ", "") == j[0].replace(" ", ""):
                allTovInSite.append(SetPoductAPI(i[1], j[1], i[0]))
                break
    return allTovInSite


def GetXSLX(allTov):
    """
    Функция для создания файла XLSX с информацией о товарах на сайте.
    """
    d = {
        "id": [i for i in range(1, len(allTov) + 1)],
        "ID Site": [i[0] for i in allTov],
        "ID OZON": [i[2] for i in allTov],
        "Наименование": [i[1] for i in allTov],
        "Цена": [i[3] for i in allTov]
    }
    df = pd.DataFrame(d)
    df.to_excel("Товары на сайте.xlsx", index=False)

def main():
    filePost1 = "Парфюмерия 16.06.2023.xlsx"
    filePost2 = "Отливанты 16.06.2023.xlsx"
    fileSite = "Файл для добавления товаров.xlsx"
    inPost1 = GetTovarInSite1(filePost1)
    inPost2 = GetTovarInSite2(filePost2)
    inPost1.extend(inPost2)
    inSite = GetTovar(fileSite)
    allTovInSite = OzonToSite(inSite, inPost1)
    GetXSLX(allTovInSite)

if __name__ == '__main__':
    main()
