# -*- coding: utf-8 -*-
import csv
import re

def DelSubStr(string):

    string = string.replace(' edp ', '')
    string = string.replace(' edc ', '')
    string = string.replace(' edt ', '')
    string = string.replace(' TESTER ', '')
    string = string.replace(' parfume ', '')
    string = string.replace('deo stick', '')
    string = string.replace('(w)', '')
    string = string.replace('(m)', '')
    string = string.replace('пробник', '')
    string = string.replace('старый дизайн', '')
    string = string.replace('старый дизайн', '')
    string = re.sub('[0-9]{0,4}ml', '', string)
    string = re.sub('[0-9][0-9].[0-9]ml', '', string)
    string = re.sub('[0-9].[0-9][0-9]ml', '', string)
    string = string.replace('*', '')
    string = string.replace('+', '')
    string = string.replace('b/l', '')
    string = string.replace('b/oil', '')
    string = string.replace('body spray', '')
    string = string.replace('sh/g', '')
    string = string.replace('shampoo','')
    string = string.replace('deo', '')
    string = string.replace('пудра', '')
    string = string.replace('af/sh', '')
    string = string.replace('запаска', '')
    string = string.replace('ароматическая вода', '')
    string = string.replace('VINTAGE', '')
    string = string.replace('дизайн 2019', '')
    string = string.replace('.', '')
    string = string.replace('mini', '')
    string = string.replace('roller', '')
    string = string.replace('refill', '')
    string = string.replace('roll', '')
    string = string.replace('без спрея', '')
    string = string.replace('с крышкой', '')
    string = string.replace('без крышки', '')
    string = string.strip()
    return  string


def GetCSV():
    products = []
    with open('lll.csv', 'r', newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            name = DelSubStr(row[0])
            if products.count(name)==0:
                products.append(name)

    return products

def ToCSV(products):
    f = open('To.txt', "w")
    for i in products:
        f.write(i+"\n")



def main():
    products=GetCSV()
    ToCSV(products)
    print(products)

if __name__ == '__main__':
    main()