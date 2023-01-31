import xml.etree.cElementTree as ET
from peewee import *
from models import *


# заполнение таблицы видов групп
def add_gruppa_a(root):
    Gruppa_a().create_table()
    for m in root.iter("agrokhimikaty"):
        group = m.find("gruppa").text
        nomer = Gruppa_a.get_or_create(naimenovanie=group)
    print("Файл обработан для таблицы gruppa_a")

# заполнение таблицы областей
def add_oblast(root):
    Oblast().create_table()
    for m in root.iter("agrokhimikaty"):
        nomer = Oblast.get_or_create(naimenovanie=m.find("oblast").text)
    print("Файл обработан для таблицы oblast")

# заполнение таблицы с агрохимикатами
def add_agrokhimikaty(root):
    Agrokhimikaty().create_table()

    for m in root.iter("agrokhimikaty"):
        gosnomer = m.find("rn").text
        if gosnomer == "": # проверка на отсутсвие номера регистрации
            continue

        # создание строки со всеми марками агрохимиката
        marka_list = ''
        name = m.find("preparat").text
        for n in root.iter("agrokhimikaty"):
            if n.find("preparat").text==name:
                marka = n.find("marka").text
                marka_list = marka_list + str(marka) + ' '

        # проверка на существование агрохимиката в базе данных
        agro = Agrokhimikaty.get_or_none(Agrokhimikaty.rn == gosnomer)
        if agro:

            # обновление всех данных об агрохимикате
            agro.rn = gosnomer
            agro.FK_gruppa = Gruppa_a.get(Gruppa_a.naimenovanie==m.find("gruppa").text)
            agro.preparat = m.find("preparat").text
            agro.marka = marka_list
            agro.FK_oblast = Oblast.get(Oblast.naimenovanie==m.find("oblast").text)
            agro.registrant = m.find("registrant").text
            agro.srok_registracii_Po = m.find("srok_registratsii_po").text
            agro.save()

        else:   # добавление агрохимиката в базу данных, если он в ней не найден
            nomer = Agrokhimikaty.create(rn=gosnomer,
            FK_gruppa=Gruppa_a.get(Gruppa_a.naimenovanie==m.find("gruppa").text),
            preparat=m.find("preparat").text, 
            marka=marka_list,
            FK_oblast=Oblast.get(Oblast.naimenovanie==m.find("oblast").text),
            registrant=m.find("registrant").text, 
            srok_registracii_Po=m.find("srok_registratsii_po").text)

    print("Файл обработан для таблицы agrochimikaty")







