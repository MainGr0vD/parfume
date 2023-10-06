from bs4 import BeautifulSoup as BS
import requests
import time
from multiprocessing import Pool
import csv
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 YaBrowser/20.7.1.70 Yowser/2.5 Yptp/1.23 Safari/537.36','accept':'*/*' }
def GetHtml(url):
    while True:
        try:

            r = requests.get(url)

            soup = BS(r.text, 'html.parser')

            name = soup.find('h1')
            if name == None:
                return None
            else:
                name = name.text
            if (name != "Service Temporarily Unavailable"):
                break

        except:
            time.sleep(5)
    return r.text


def GetNote(note):
    allThisNotes = ""
    thisNotes = note.find_all('a', target="_blank")

    for thisNote in thisNotes:
        if thisNote != None:
            if allThisNotes == "":
                allThisNotes += thisNote.text
            else:
                allThisNotes += ", " + thisNote.text
    return allThisNotes

def GetContent(html):
    soup = BS(html, 'html.parser')

    name = soup.find('h1')
    if name == None:
        return None
    else:
        name = name.text
    img =  soup.find('div',class_='card-img')
    if img == None:
        return None
    else:
        img = img.find('a').get("href")
    des = soup.find("div",class_="card-text")
    if des == None:
        des = ""
    else:
        des=des.text
    pol = soup.find("div",class_="card-sex")
    if pol==None:
        pol="-"
    else:
        pol = pol.text
    notes = soup.find_all('div',class_="card-hr")
    allVerhNote = ""
    allSerdNote = ""
    allBasNote = ""
    if notes != []:
        for note in notes:
            noteName = note.find("strong").text
            if noteName == "Верхние ноты:":
                allVerhNote=GetNote(note)
            if noteName == "Ноты сердца:":
                allSerdNote=GetNote(note)
            if noteName == "Базовые ноты:":
                allBasNote=GetNote(note)

    hars = soup.find_all('div', class_="card-dhit")
    allSem = ""
    allYear = ""
    if hars !=[]:
        for har in hars:
            noteName = har.find("strong").text
            if noteName == "Семейства:":
                allSem=GetNote(har)
            if noteName == "Год начала выпуска:":
                allYear=GetNote(har)
    return [
        name.replace(';',',').replace('\n','').replace('\r',''),
        'https://allureparfum.ru'+img,
        des.replace(';',',').replace('\n','').replace('\r',''),
        pol.replace(';',',').replace('\n','').replace('\r',''),
        allVerhNote.replace(';',',').replace('\n','').replace('\r',''),
        allSerdNote.replace(';',',').replace('\n','').replace('\r',''),
        allBasNote.replace(';',',').replace('\n','').replace('\r',''),
        allSem.replace(';',',').replace('\n','').replace('\r',''),
        allYear.replace(';',',').replace('\n','').replace('\r','')

    ]




def GetUrls():
    f = open("lol.txt")
    f= f.read().split("\n")[:-1]
    return f

def GetDataInPage(url):
    url = "https://allureparfum.ru"+url
    print(url)
    while True:
        try:
            html = GetHtml(url)
            tovar = GetContent(html)
            break
        except:
            time.sleep(2)
    return tovar

def GetCsv(tovars):
    with open("L1.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        for i in tovars:
            if i != []:
                for j in i:
                    file_writer.writerow([j[0],j[1], j[2],j[3],j[4],j[5],j[6],j[7],j[8]])


def GetAllContent(urls):
    print("Все ок!")
    mainArr = []
    with Pool(20) as p:
        mainArr.append(p.map(GetDataInPage, urls))
    print(mainArr)
    GetCsv(mainArr)

def main():
    urls = GetUrls()
    GetAllContent(urls)


if __name__ == '__main__':
    main()