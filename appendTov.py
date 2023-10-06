# -*- coding: utf-8 -*-
from woocommerce import API
import csv
from decimal import Decimal
from time import sleep

def GetAPIConnect():
    wcapi = API(
        # url="http://roma28.beget.tech",
        # consumer_key="ck_aa7763a2a2b844b03fdd67a3aa752812922ac5ab",
        # consumer_secret="cs_04eda7aa92e03331b14e581eb60fbd02494b81a3",
        url="https://t.parfumelight.ru",
        consumer_key="ck_e9a9cd7d5bec35dd781de2ca343bb549bbfb38c3",
        consumer_secret="cs_0400759a72f786596bb9fe97ab6546239d54f9c1",
        version="wc/v3",
        timeout = 18
    )
    return wcapi
# Query example.

def RenameNameProbnik(name,categories):
    name = name.replace(" edt "," Туалетная вода ")

    name = name.replace(" edp ", " Парфюмерная вода ")
    name = name.replace(" edc ", " Одеколон ")
    name = name.replace(" edT ", " Туалетная вода ")
    name = name.replace(" edP ", " Парфюмерная вода ")
    name = name.replace(" PARFUME ", " Парфюм ")
    name = name.replace(" parfume ", " Парфюм ")
    name = name.replace("    ", "")
    if categories[0].get("name") == "Женская парфюмерия":
        name = name + " Ж"
        name = name.replace("(w)",'')
    elif categories[0].get("name") == "Мужская парфюмерия":
        name = name + " М"
        name = name.replace("(m)", '')
    elif categories[0].get("name") == "Унисекс":
        name = name + " У"
        name = name.replace("(y)", '')
    return name

def GetTovar(wcapi):
    page = 1
    dataproducts = []
    while True:
        while True:
            try:
                products = wcapi.get('products', params={'per_page': 100, "type":"grouped",'stock_status': 'instock', 'page': page}).json()
                break
            except:
                sleep(5)

        print(products)
        for i in products:
            # print(i)
            # print(i.get("name"))
            # print(i.get("grouped_products"))
            dataproducts.append({
                "id": i.get("id"),
                "name" : i.get("name"),
                "grouped_products" : i.get("grouped_products"),
                "images": i.get("images"),
                "description": i.get("description"),
                "categories": i.get("categories"),
            })
        if len(products) == 0:  # no more products
            break
        page = page + 1

    return dataproducts

def GetOneTovar(wcapi,id):
    while True:
        try:
            jsProd = wcapi.get("products/"+str(id)).json()
            break
        except:
            sleep(5)
    return jsProd


# def ReplaceOtl(str):
#     str = str.replace("отливант","")
#     str = str.replace("ml", "")
#     str = str.replace("1","")

def CheckTov(name,wcapi):
    products = wcapi.get('products',params={"search":name}).json()
    if len(products)>0:
        return True
    else:
        return False

def PostDopTov(data,name,priceUSA,wcapi):
    name = RenameNameProbnik(name,data.get("categories"))

    dataForDop= {
       "name": name,
        "description": data.get("description"),
        "images": data.get("images"),
        "regular_price": str((int(float(priceUSA.replace(',','.')))*70)*1.16)
        }
    while True:
        try:
            jsonProd = wcapi.post("products", dataForDop).json()
            break
        except:
            sleep(5)
        # print(jsonProd.get("id"))
    grouped_products = []
    for i in list(data.get("grouped_products")):
        grouped_products.append(i)
    grouped_products.append(jsonProd.get("id"))
    print(grouped_products)
    dataForMain = {
            "grouped_products": grouped_products
                # ....

        }
    while True:
        try:
            jsonProd = wcapi.put("products/" + str(data.get("id")), dataForMain).json()
            break
        except:
            sleep(5)


def GetCSVProduct(dataproducts,wcapi):
    with open('mikrooptovye_Otlivanty .csv', 'r', newline='', encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        c=0
        for row in spamreader:
            # print(row[1].replace(" ","").lower())
            prod = row[0].split("   ")[0]
            # print(prod)

            for i in dataproducts:
                if i.get("name").replace(" ","").replace("&amp;","").lower() == prod.replace(" ","").replace("&","").lower() :
                    c+=1

                    tovar = GetOneTovar(wcapi,i.get("id"))
                    # print(i.get("name")+" - "+ row[1])
                    # print(RenameNameProbnik(row[1],i.get("categories")))
                    PostDopTov(tovar,row[0],row[1],wcapi)
    print(c)


def main():
    wcapi = GetAPIConnect()
    dataproducts = GetTovar(wcapi)
    GetCSVProduct(dataproducts,wcapi)


if __name__ == '__main__':
    main()