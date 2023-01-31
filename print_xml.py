import xml.etree.cElementTree as ET
from models import *
from pesticidy import *
from agrokhimikaty import *
from bs4 import BeautifulSoup
import requests, re, zipfile, os
from io import BytesIO

# создание списка ссылок на файлы
def add_links(html_url):
    link=[]
    html_page = html_url
    r = requests.get(html_page)
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.findAll(href=re.compile("data-")):
        link.append(a.text)
    return link

# метод открытия файла xml
def file_open(f: str):
    tree = ET.parse(f)
    root=tree.getroot()
    return root

# метод переборки файлов и заполнения их данных в базу данных 
def autofill(link: list, func):
    for i in range(len(link)-5, len(link)):
        r = requests.get(link[i])
        z = zipfile.ZipFile(BytesIO(r.content))
        name_f = z.namelist()
        z.extractall()
        root = file_open(name_f[0])
        func(root)
        os.remove(name_f[0])
        print('Заполнение базы данных завершено!')

# ссылки на сайт с каталогами пестицидов и агрохимикатов
pest_url = 'http://opendata.mcx.ru/opendata/7708075454-pestitsidy'
agro_url = 'http://opendata.mcx.ru/opendata/7708075454-agrokhimikaty'

# списки методов заполнения таблиц для передачи в метод автозаполнения базы данных
pest_func_list = [add_gruppa_p,add_preparativnaya_forma,add_klass_opasnosti,add_pesticidy]
agro_func_list = [add_gruppa_a,add_oblast,add_agrokhimikaty]

print("Добро пожаловать в менеджер базы данных!")
while True:
    print("Выберите действие:")
    print("1.Автозаполнение базы данных пестицидов")
    print("2.Автозаполнение базы данных агрохимикатов")
    print("3.Выход.")
    menu=int(input("Выберите действие: "))
    if menu == 1:
        link = add_links(pest_url)
        for i in range(len(pest_func_list)):
            autofill(link, pest_func_list[i])
    elif menu == 2:
        link = add_links(agro_url)
        for i in range(len(agro_func_list)):
            autofill(link,agro_func_list[i])
    else:
        break






