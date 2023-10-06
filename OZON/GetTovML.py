import requests
import pandas as pd

def GetTovarInSite(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    dictNamesPost = newdf["Наименование"]
    NamesPOST=[]
    for i in range(len(dictNamesPost)):
        NamesPOST.append(dictNamesPost[i])
    return NamesPOST

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

headers = {
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }

def ApiGetML(id_prod):
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
    r = requests.post("https://api-seller.ozon.ru/v3/products/info/attributes", json=data, headers=headers)
    atrs=r.json()["result"][0]["attributes"]
    for i in atrs:
        print(i["attribute_id"], i["values"][0]["value"])
        if i["attribute_id"] == 8163:
            return (id_prod,r.json()["result"][0]["name"],i["values"][0]["value"])
    return (id_prod,r.json()["result"][0]["name"],"NNNNN")

def Ozon(inSite):
    arrTovMIS = []
    for i in inSite:
        # print(i[0])
        infoJson = ApiGetML(i[1])
        print(infoJson)
        break
        # if infoJson[1].count(str(infoJson[2])+"ml")==0:
        #     arrTovMIS.append([infoJson[0],infoJson[1],infoJson[2]])
    return arrTovMIS

def GetXSLX(allTov):
    d ={}
    d["id"] = [i for i in range(1, len(allTov) + 1)]
    d["OZON ID"] = [i[0] for i in allTov]
    d["Наименование"] = [i[1] for i in allTov]
    d["Объем сейчас"] = [i[2] for i in allTov]
    df = pd.DataFrame(d)
    df.to_excel("Ошибки в объемах сейчас.xlsx", index=False)

def main():
    fileSite = "Файл для проверки на складе.xlsx"
    inSite = GetTovar(fileSite) # массив с Именами
    # print(inSite)
    arrTovMIS = Ozon(inSite)
    GetXSLX(arrTovMIS)


if __name__ == '__main__':
    main()