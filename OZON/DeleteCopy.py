import requests
import pandas as pd

headers = {
        "Content-Type": "application/json",
        "Client-Id": "819970",
        "Api-Key": "eb79fcb1-fef4-41b0-ad47-5b2c3cfe3b72"
    }

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

def GetAllTovOzon(file):
    df = pd.read_excel(file, engine='openpyxl')
    newdf = df.to_dict()
    NamesAndIdSite = []
    dictNames = newdf["Название"]
    dictArticul = newdf["Артикул"]
    dictStatus = newdf["Статус"]
    for i in range(len(dictNames)):
        NamesAndIdSite.append([dictNames[i], dictArticul[i],dictStatus[i]])
    # print(NamesAndIdSite)
    return NamesAndIdSite


def GetTovVspArr(vspArr,i):
    for j in vspArr:
        if  i[0] == j[0]:
            return True
    return False

def GetIdProd(art):
    jsons = {

        "offer_id": art,

    }
    rs = requests.post("https://api-seller.ozon.ru/v2/product/info", headers=headers,
                       json=jsons)
    print(rs)
    return rs.json()["result"]["id"]

def DeleteTov(el):
    headers = {
        "Client-Id": "819970",
        "Api-Key": "5e62aeff-680a-4ba4-a2d2-dcb3171d5762"
    }
    print(el[1])
    id_prod = GetIdProd(el[1])
    print(id_prod)
    json = {
        "product_id": [
            id_prod
        ]
    }
    r = requests.post("https://api-seller.ozon.ru/v1/product/archive", json=json, headers=headers)
    print(r.text)

def GetProdInSite(allTovOzon):
    vspArr = []
    c=0
    for i in allTovOzon:
        if i[2]=="Продается" or (not GetTovVspArr(vspArr,i)):
            vspArr.append(i)
        else:
            c+=1
            DeleteTov(i)
            
    print(c)



def main():
    fileAllTovOzon="Шаблон цен.xlsx"
    fileSite = "Файл для проверки на складе.xlsx"
    inSite = GetTovar(fileSite)
    allTovOzon = GetAllTovOzon(fileAllTovOzon)
    GetProdInSite(allTovOzon)

if __name__ == '__main__':
    main()


