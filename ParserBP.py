import requests
from bs4 import BeautifulSoup as BS
import time
from fake_useragent import UserAgent

def GetHtml_(url):
    while True:
        try:
            ua = UserAgent()

            r = requests.get(url,headers={'User-Agent': ua.ie })
            break
        except:
            time.sleep(5)

    return r.text

def GetProduct(soup):
    print(soup)
    name = soup.find('h1').text

    img = soup.find('div',class_ = "cell small-6 text-center").find('img').get('src')
    description = soup.find('div',itemprop="description").find('p').text

    return {
        'name': name,
        'img': img,
        'description':description
    }


def main():
    #https://www.fragrantica.ru/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html
    url = 'https://www.fragrantica.ru/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html'
    html = GetHtml_(url)
    soup = BS(html, 'html.parser')
    product = GetProduct(soup)
    print(product)


if __name__ == '__main__':
    main()