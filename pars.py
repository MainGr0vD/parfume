from bs4 import BeautifulSoup as BS
import requests
import time
from multiprocessing import Pool
import csv

def GetHtml(url):
    while True:
        try:


            r = requests.get(url)
            break
        except:
            time.sleep(5)

    return r.text

def GetTovar(html):
    soup = BS(html, 'html.parser')
    name = soup.find('h4',itemprop="name")
    if name == None:
        return None
    else:
        name = name.text.strip()
        print(name)
    des = soup.find('section',id = "description")
    if des == None:
        des = ""
    else:
        des = des.find('p')
        if des == None:
            des = ""
        else:
            des = des.text
    atrs = soup.find_all('div',class_='mb-1')
    atrOld = ''
    atrGrup = ''
    atrVerh = ''
    atrSerd = ''
    atrBaz = ''
    if atrs !=None:
        for atr in atrs:
            atr_key = atr.find('p',class_="mb-2").text
            atr_value = atr.find('p',class_="mb-0").text
            atr_value = atr_value.strip().replace('\n','').replace('\t','')
            if atr_key == "Год выпуска:":
                atrOld = atr_value
            if atr_key == "Группа ароматов:":
                atrGrup = atr_value
            if atr_key == 'Верхние ноты:':
                atrVerh = atr_value
            if atr_key == "Ноты сердца:":
                atrSerd= atr_value
            if atr_key == "Базовые ноты:":
                atrBaz = atr_value

    img = soup.find("img",class_="img-fluid multi")
    if img == None:
        return None
    else:
        img=img.get('src')
    return {
        'name' : name.replace(';',',').replace('\n',''),
        "description": des.replace(';',',').replace('\n',''),
        "img":"	https://xn--d1ai6ai.xn--p1ai"+img,
        "atrOld":atrOld,
        "atrGrup":atrGrup,
        "atrVerh":atrVerh,
        "atrSerd":atrSerd,
        "atrBaz":atrBaz,
    }

def GetUrls():
    f = open("urls.txt",encoding="utf-8")
    ar = f.read().split("\n")
    return ar

# def GetCsv(tovars):
#     with open('lll1.csv', 'w', newline='',encoding="utf-8") as csvfile:
#         file_writer = csv.writer(csvfile, delimiter=";", lineterminator="\r")
#         fieldnames = ['name', 'description', "img","atrOld","atrGrup","atrVerh","atrSerd","atrBaz"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for i in tovars:
#             if i != None:
#                 writer.writerow(i)

def GetCsv(tovars):
    print(tovars)
    with open("lll1.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        for i in tovars:
            print("-----------------------------")
            print(i)
            if i != None:
                file_writer.writerow([i.get("name"),i.get("description"), i.get("img"),i.get("atrOld"),i.get("atrGrup"),i.get("atrVerh"),i.get("atrSerd"),i.get("atrBaz")])

def GetDataInPage(url):
    print(url)
    html = GetHtml(url)

    tovar = GetTovar(html)
    return tovar

def GetAllContent(urls):
    print("Все ок!")
    mainArr = []
    with Pool(20) as p:
        mainArr.extend(p.map(GetDataInPage, urls))
    print(len(mainArr))
    GetCsv(mainArr)

            # AppendTovarInMyFile(i)# Переделать
            #AppendInMysqlTovar(i)

def main():
    # url= "https://духи.рф/catalog/men/Azzaro/Chrome-Pure"
    # html = GetHtml(url)
    urls = GetUrls()
    GetAllContent(urls)
    # tovar = GetTovar(html)


if __name__ == '__main__':
    main()