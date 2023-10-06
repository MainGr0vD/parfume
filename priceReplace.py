import pandas as pd
import re

def GetNameProductWithOZON(fileName):
    df = pd.read_excel(fileName, engine='openpyxl')
    newdf = df.to_dict()
    # print(newdf["Наименование"])
    NamesOzon = []
    dictNames =newdf["Наименование"]
    for i in range(len(dictNames)):
        NamesOzon.append(dictNames[i])
    return NamesOzon


def GetPriceAndNameProductWithPriceList(fileName):
    df = pd.read_excel(fileName, engine='openpyxl')
    newdf = df.to_dict()
    # print(1)
    # print(newdf)
    NamesAndPricePostavshic = []
    dictNames = newdf["Наименование"]
    # print(newdf["Наименование"])
    dictPrice = newdf["Цена"]
    for i in range(len(dictNames)):
        NamesAndPricePostavshic.append([dictNames[i],dictPrice[i]])
    # print(NamesAndPricePostavshic)
    return NamesAndPricePostavshic

def SearchProductName(NamesOzon,NamesAndPricePostavshic):
    for i in NamesOzon:
        for j in NamesAndPricePostavshic:
            print(i,end=" ")
            index = re.search('[0-9]{0,4}ml', i)
            print(j[0])
            print(int(index))
            break
        break

def main():
    NamesOzon = GetNameProductWithOZON("OZON (2).xlsx")
    NamesAndPricePostavshic = GetPriceAndNameProductWithPriceList("Postavshic.xlsx")
    SearchProductName(NamesOzon,NamesAndPricePostavshic)

if __name__ == '__main__':
    main()