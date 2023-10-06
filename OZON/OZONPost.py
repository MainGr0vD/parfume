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

def ApiArchive(id_prod):
    headers = {
        "Client-Id":"819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
    json ={
        "product_id": [
            id_prod
        ]
    }
    r = requests.post("https://api-seller.ozon.ru/v1/product/archive",json=json,headers=headers)
    print(r.text)

def ApiUnarchive(id_prod):
    headers = {
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
    data = {
        "product_id": [
            id_prod
        ]
    }
    r = requests.post("https://api-seller.ozon.ru/v1/product/unarchive", json=data, headers=headers)
    print(r.text)



def Ozon(inSite,inPost):
    for i in inSite:
        isPost = False
        for j in inPost:
            # print(i[0],j)
            if i[0].replace(" ","")==j.replace(" ",""):
                print(str(i[1])+"TRUE")
                isPost = True
                ApiArchive(i[1])
                # ApiUnarchive(i[1])
                break
        if not isPost:
            print(str(i[1])+"FALSE")
            ApiArchive(i[1])


def main():
    filePost1 = "Парфюмерия 13.06.2023.xlsx"
    filePost2 = "Отливанты 13.06.2023.xlsx"
    fileSite = "Файл для проверки на складе.xlsx"
    inPost1 = GetTovarInSite(filePost1) # массив с Именами и Индификаторами товаров
    inPost2 = GetTovarInSite(filePost2)

    inPost1.extend(inPost2)
    # print(inPost1)
    inSite = GetTovar(fileSite) # массив с Именами
    Ozon(inSite,inPost1)

if __name__ == '__main__':
    main()