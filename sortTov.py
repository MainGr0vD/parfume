# -*- coding: utf-8 -*-
import csv
import re


def RenameTov(string):
    string = string.replace('TESTER', '')
    string = re.sub('\*', '', string)
    string = re.sub('\+', '', string)
    string = string.replace('.', '')
    string = string.replace(',', '')
    string = re.sub('[0-9]{0,4}ml', '', string)


    return string

def GetAllTovName():
    newar=[]
    with open("Polny_prays.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        for row in file_reader:

            name=row[0]
            name = RenameTov(name).strip()

            name = name.split("  ")[0]


            if newar.count(name)==0 and (name.count('edp')>0 or name.count('edc')>0 \
                    or name.count('edt')>0 or name.count('parfume')>0):
                newar.append(name)
    print(newar)
    return newar

def GetTxt(tovs):
    f = open('nameTov.txt','w')
    for i in tovs:
        f.write(i+"\n")

def main():
    nameTovars=GetAllTovName()
    GetTxt(nameTovars)

if __name__ == '__main__':
    main()