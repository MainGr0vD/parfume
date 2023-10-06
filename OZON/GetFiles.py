import pandas as pd
import requests
import urllib
import json


folder_url = 'https://disk.yandex.ru/d/LWJGnftEDuIoFw'

def GetXLSX(file_url):
    url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download' + '?public_key=' + urllib.parse.quote(folder_url) + '&path=/' + urllib.parse.quote(file_url)
    r = requests.get(url) # запрос ссылки на скачивание
    h = json.loads(r.text)['href'] # 'парсинг' ссылки на скачивание
    df = pd.read_excel(h)
    if file_url.find("Отливанты")>=0:
        df.to_excel("Отливанты.xlsx",index=False)
    elif file_url.find("Парфюмерия")>=0:
        df.to_excel("Парфюмерия.xlsx",index=False)

def GetFiles():
    url = 'https://cloud-api.yandex.net/v1/disk/public/resources' + '?public_key=' + urllib.parse.quote(folder_url)+ '&path=/'
    print(url)
    r = requests.get(url)
    items = r.json()["_embedded"]["items"]
    arFiles = []
    for item in items:
        print(item["name"])
        if item["name"].find("Отливанты")>=0 or item["name"].find("Парфюмерия")>=0:
            arFiles.append(item["name"])

    return arFiles

def main():
    arFiles =GetFiles()
    print(arFiles)
    for i in arFiles:
        GetXLSX(i)

if __name__ == '__main__':
    main()