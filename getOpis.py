import pandas as pd
import csv

def GetWs():
    df = pd.read_excel("forOzon.xlsx", engine='openpyxl')
    dfm = df.to_dict()
    print(len(dfm.get("Имя")))
    # print(list(df["Имя"]))
    # print(list(df["Описание"]))
    return list(df["Имя"])
    # df = csv.reader("wc-product-export-3-12-2022-1670077990262.csv")
    # print(list(df["ИНН"]))
    # lis = []
    # with open('wc-product-export-3-12-2022-1670077990262.csv', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in spamreader:
    #         lis.append(row)

    # print(lis)

def GetOzon():
    df = pd.read_excel("ozon.xlsx",engine='openpyxl')
    print(list(df["Наименование"]))
    return list(df["Наименование"])
    # newdf = list(df.values)
    # print(newdf)

def GetOpis(ws,ozon):
    df = pd.read_excel("forOzon.xlsx", engine='openpyxl')
    opis = list(df["Описание"])
    l = []
    for i in range(len(ozon)):
        for j in range(len(ws)):
            if ozon[i]==ws[j]:
                l.append(opis[j])
                break
    return l

def SetOpis(content):
    d= {"Описание":content}
    df = pd.DataFrame(d)
    df.to_excel("opis.xlsx")

def main():
    ws = GetWs()
    # ozon = GetOzon()
    # opis = GetOpis(ws,ozon)
    # SetOpis(opis)

if __name__ == '__main__':
    main()