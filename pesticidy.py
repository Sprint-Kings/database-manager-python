import xml.etree.cElementTree as ET
from peewee import *
from models import *


# заполнение таблицы видов групп
def add_gruppa_p(root):
    Gruppa_p().create_table()
    for m in root.iter("items"):
        group = m.find("Gruppa")[0].text
        nomer = Gruppa_p.get_or_create(naimenovanie=group)
    print("Файл обработан для таблицы gruppa_p")

# заполнение таблицы видов препаративных форм
def add_preparativnaya_forma(root):
    Preparativnaya_forma().create_table()
    for m in root.iter("items"):
        nomer = Preparativnaya_forma.get_or_create(naimenovanie=m.find("Preparativnaya_forma")[0].text)
    print("Файл обработан для таблицы preparativnaya_forma")

# заполнение таблицы классов опасности
def add_klass_opasnosti(root):
    Klass_opasnosti().create_table()
    for m in root.iter("items"):
        nomer = Klass_opasnosti.get_or_create(naimenovanie=m.find("Klass_opasnosti")[0].text)
    print("Файл обработан для таблицы klass_opasnosti")

# заполнение таблиц с пестицидами, их группами и инструкциями
def add_pesticidy(root):
    Pesticidy().create_table()
    Gruppa_Pesticidy().create_table()
    Instrukcia().create_table()

    for m in root.iter("items"):
        gosnomer = m.find("Nomer_gosudarstvennoy_registracii")[0].text
        if gosnomer == "": # проверка на отсутсвие номера регистрации
            continue

        group = m.find("Gruppa")[0].text

        # проверка на существование пестицида в базе данных
        pest = Pesticidy.get_or_none(Pesticidy.nomer_gosudarstvennoy_registracii == gosnomer)
        if pest:
            # обновление всех данных о пестициде
            pest.naimenovanie = m.find("Naimenovanie")[0].text
            pest.FK_preparativnaya_forma = Preparativnaya_forma.get(Preparativnaya_forma.naimenovanie==m.find("Preparativnaya_forma")[0].text)
            pest.deystvuyushee_veshestvo = m.find("Deystvuyushee_veshestvo")[0].text
            pest.soderzhanie_deystvuyushego_veshestva = m.find("Soderzhanie_deystvuyushego_veshestva")[0].text
            pest.registrant = m.find("Registrant")[0].text
            pest.FK_klass_opasnosti = Klass_opasnosti.get(Klass_opasnosti.naimenovanie==m.find("Klass_opasnosti")[0].text)
            pest.srok_registracii_Po = m.find("Srok_registracii_Po")[0].text
            pest.nomer_gosudarstvennoy_registracii = m.find("Nomer_gosudarstvennoy_registracii")[0].text
            pest.save()

            # поиск в файле, сколько раз попадается пестицид
            name = m.find("Naimenovanie")[0].text
            group_all=[] # список групп, к которым относится пестицид в файле
            for n in root.iter("items"):
                if n.find("Naimenovanie")[0].text==name:
                    group_all.append(n.find("Gruppa")[0].text)

            c=[] # список, к каким группам препарат относится в базе данных
            for connection in Gruppa_Pesticidy.select().where(Gruppa_Pesticidy.preparat==Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer)):
                c.append(connection.id)

            # удаление устаревших групп препарата в базе данных и вставка новых из файла
            if len(c)>len(group_all):
                for i in reversed(range(len(group_all),(len(c)-len(group_all))+1)):
                    pest_id = Gruppa_Pesticidy.get_by_id(c[i])
                    Gruppa_Pesticidy.delete_by_id(c[i])
                    '''instukcia_del = Instrukcia.delete().where(Instrukcia.FK_kode==pest_id.preparat,
                    Instrukcia.FK_ID==pest_id.gruppa)
                    instukcia_del.execute()
                    Pesticidy.delete_by_id(pest_id.preparat)'''
                for i in range(len(group_all)):
                    connection = Gruppa_Pesticidy.get_by_id(c[i])
                    connection.gruppa = Gruppa_p.get(Gruppa_p.naimenovanie == group_all[i])
                    connection.save()

            # обновление всех групп препарата в базе данных из файла
            elif len(c)==len(group_all):
                for i in range(len(c)):
                    connection = Gruppa_Pesticidy.get_by_id(c[i])
                    connection1 = Gruppa_p.get(Gruppa_p.ID == connection.gruppa)
                    if connection1.naimenovanie == group_all[i]:
                        continue
                    else:
                        connection.gruppa = Gruppa_p.get(Gruppa_p.naimenovanie == group_all[i])
                        connection.save()

            # добавление новых групп препарату и обновление старых в базе данных из файла           
            else:
                for i in range(len(c)):
                    connection = Gruppa_Pesticidy.get_by_id(c[i])
                    connection.gruppa = Gruppa_p.get(Gruppa_p.naimenovanie == group_all[i])
                    connection.save()
                for i in range(len(c),len(group_all)):
                    connection = Gruppa_Pesticidy.create(preparat=Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer),
                    gruppa=Gruppa_p.get(Gruppa_p.naimenovanie == group_all[i]))

            b= [] # список, какие инстукции есть у препарата в файле
            for g in m.find("fulldataset"):
                for n in g.iter("item"):
                    b.append([0]*6)

            i = 0 # заполнение матрицы с данными инстукций препарата
            for g in m.find("fulldataset"):
                for n in g.iter("item"):
                    b[i][0]=n[0].text
                    b[i][1]=n[1].text
                    b[i][2]=n[2].text
                    b[i][3]=n[3].text
                    b[i][4]=n[4].text
                    b[i][5]=n[5].text
                    i+=1

            a = [] # список, какие инструкции у препарата в базе данных
            for fulld in Instrukcia.select().where(Instrukcia.FK_kode==Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer),
            Instrukcia.FK_ID==Gruppa_p.get(Gruppa_p.naimenovanie==group)):
                a.append(fulld.id)

            # удаление устаревших инстукций препарата в базе данных и вставка новых из файла
            if len(a)>len(b):
                for i in reversed(range(len(b),(len(a)-len(b))+1)):
                    Instrukcia.delete_by_id(a[i])
                for i in range(len(b)):
                    connection = Instrukcia.get_by_id(a[i])
                    connection.FK_kode = Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer)
                    connection.FK_ID = Gruppa_p.get(Gruppa_p.naimenovanie==group)
                    connection.vrednyy_obekt_naznachenie = b[i][0]
                    connection.kultura_obrabatyvaemyy_obekt = b[i][1]
                    connection.sposob_i_vremya_obrabotki = b[i][2]
                    connection.srok_ozhidaniya_krathost_obrabotok = b[i][3]
                    connection.sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot = b[i][4]
                    connection.norma_primeneniya_preparata_lga_kgga_lt_kgt = b[i][5]
                    connection.save()

            # обновление всех инстукций препарата в базе данных из файла    
            elif len(a)==len(b):
                for i in range(len(a)):
                    connection = Instrukcia.get_by_id(a[i])
                    connection.FK_kode = Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer)
                    connection.FK_ID = Gruppa_p.get(Gruppa_p.naimenovanie==group)
                    connection.vrednyy_obekt_naznachenie = b[i][0]
                    connection.kultura_obrabatyvaemyy_obekt = b[i][1]
                    connection.sposob_i_vremya_obrabotki = b[i][2]
                    connection.srok_ozhidaniya_krathost_obrabotok = b[i][3]
                    connection.sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot = b[i][4]
                    connection.norma_primeneniya_preparata_lga_kgga_lt_kgt = b[i][5]
                    connection.save()

            # добавление новых инстукций препарату и обновление старых в базе данных из файла    
            else:
                for i in range(len(a)):
                    connection = Instrukcia.get_by_id(a[i])
                    connection.FK_kode = Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer)
                    connection.FK_ID = Gruppa_p.get(Gruppa_p.naimenovanie==group)
                    connection.vrednyy_obekt_naznachenie = b[i][0]
                    connection.kultura_obrabatyvaemyy_obekt = b[i][1]
                    connection.sposob_i_vremya_obrabotki = b[i][2]
                    connection.srok_ozhidaniya_krathost_obrabotok = b[i][3]
                    connection.sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot = b[i][4]
                    connection.norma_primeneniya_preparata_lga_kgga_lt_kgt = b[i][5]
                    connection.save()
                for i in range(len(a),len(b)):
                    Instrukcia.create(FK_kode=Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer), 
                    FK_ID=Gruppa_p.get(Gruppa_p.naimenovanie==group), vrednyy_obekt_naznachenie=b[i][0], 
                    kultura_obrabatyvaemyy_obekt=b[i][1],sposob_i_vremya_obrabotki=b[i][2],
                    srok_ozhidaniya_krathost_obrabotok=b[i][3], 
                    sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot=b[i][4], 
                    norma_primeneniya_preparata_lga_kgga_lt_kgt=b[i][5],)    

        else:   # добавление пестицида в базу данных, если он в ней не найден
            nomer = Pesticidy.create(naimenovanie=m.find("Naimenovanie")[0].text,
            FK_preparativnaya_forma=Preparativnaya_forma.get(Preparativnaya_forma.naimenovanie==m.find("Preparativnaya_forma")[0].text),
            deystvuyushee_veshestvo=m.find("Deystvuyushee_veshestvo")[0].text, 
            soderzhanie_deystvuyushego_veshestva=m.find("Soderzhanie_deystvuyushego_veshestva")[0].text,
            registrant=m.find("Registrant")[0].text, 
            FK_klass_opasnosti=Klass_opasnosti.get(Klass_opasnosti.naimenovanie==m.find("Klass_opasnosti")[0].text),
            srok_registracii_Po=m.find("Srok_registracii_Po")[0].text,
            nomer_gosudarstvennoy_registracii=m.find("Nomer_gosudarstvennoy_registracii")[0].text)

            # создание связи между пестицидом и группами, к которым он относится в базе данных
            connection = Gruppa_Pesticidy.create(preparat=Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==gosnomer),
            gruppa=Gruppa_p.get(Gruppa_p.naimenovanie == group))

            # создание инструкций к препарату в базе данных
            for g in m.find("fulldataset"):
                for n in g.iter("item"):
                    Instrukcia.create(FK_kode=Pesticidy.get(Pesticidy.nomer_gosudarstvennoy_registracii==m.find("Nomer_gosudarstvennoy_registracii")[0].text), 
                    FK_ID=Gruppa_p.get(Gruppa_p.naimenovanie==group), vrednyy_obekt_naznachenie=n[0].text, 
                    kultura_obrabatyvaemyy_obekt=n[1].text,sposob_i_vremya_obrabotki=n[2].text,
                    srok_ozhidaniya_krathost_obrabotok=n[3].text, 
                    sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot=n[4].text, 
                    norma_primeneniya_preparata_lga_kgga_lt_kgt=n[5].text,)
    print("Файл обработан для таблиц pesticidy, instrukcia, gruppa_pesticidy")







