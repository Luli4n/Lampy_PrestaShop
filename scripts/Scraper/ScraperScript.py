from bs4 import BeautifulSoup
import requests
import json

from PageModel import PageModel
from ProductModel import ProductModel
import time

def initializer():
    pages = []
    pages.append(PageModel("nowoczesne-kinkiety-scienne,29", "NOWOCZESNE", "KINKIETY"))
    pages.append(PageModel("lampy-biurkowe-stolowe,28", "NOWOCZESNE", "LAMPY BIURKOWE"))
    pages.append(PageModel("klasyczne-lampy-i-zyrandole,32", "KLASYCZNE", "ŻYRANDOLE"))
    pages.append(PageModel("lampki-dzieciece-lampy-do-pokoju-dziecka,24", "DZIECIĘCE", ""))
    pages.append(PageModel("lampy-lazienkowe,23", "ŁAZIENKOWE", ""))
    pages.append(PageModel("zarowki-led-energooszczedne,56", "ŻARÓWKI", ""))
    return pages

mainUrl = "https://www.imperiumlamp.pl/"
productsIdInUrl = "products"
productValueSubstring = "product-cell product-main-cell"
lamps = []
pages = initializer()
file = open('productsInJSON.json', 'w')
file.write("[")
file.close()

def get_content(url, prodID):
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    products = soup.find(id = prodID)
    return products

def get_images(productInfo):
    images = productInfo.find_all("img")
    mainPhoto = images[0]
    logo = images[3]
    return mainPhoto["src"], logo["src"]

def get_header(url):
    content = get_content(url, "productHead")
    return content.find("h2").next

def get_main_info(productInfo):
    keys = productInfo.find_all("dt")
    values = productInfo.find_all("dd")
    mainInfo = {}
    for i in range(len(keys)):
        if(i == 0):
            mainInfo[keys[i].text] = values[i].next.attrs['href']
            producer = values[i].text
        else:
            mainInfo[keys[i].text] = values[i].text
    return producer, mainInfo

def get_tech_info(productInfo):
    keys = productInfo.find_all("li")
    techInfo = []
    for key in keys:
        techInfo.append(key.text)
    return techInfo

for page in pages:
    url = page.url
    title = page.title
    subtitle = page.subtitle
    products = get_content(mainUrl + url, productsIdInUrl)
    results = products.find_all("div", lambda value: value and value.startswith(productValueSubstring))
    for result in results:
        href = result.find("a").attrs['href']
        header = get_header(mainUrl + href)
        productInfo = get_content(mainUrl + href, "product")
        mainPhoto, logo = get_images(productInfo)
        try:
            shortDesc = productInfo.find("h2").text
            if not isinstance(shortDesc, str):
                shortDesc = ""
        except:
            shortDesc = ""  
        producer, mainInfo = get_main_info(productInfo)
        price = productInfo.find("div", id = "price").text
        techInfo = get_tech_info(productInfo)
        lamp = ProductModel(title, subtitle, mainUrl+href, header, 
            mainPhoto, logo, shortDesc, producer, mainInfo, price, techInfo)
        product = lamp.convert_to_JSON()
        start_time = time.time()
        with open('productsInJSON.json', 'a', encoding='utf-8') as file:
            json.dump(product, file, ensure_ascii=False)
            file.write(",")
        print("--- %s seconds ---" % (time.time() - start_time))
file = open('productsInJSON.json', 'a')
file.write("]")
file.close()