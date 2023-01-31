from peewee import *

# подключение базы данных
pg_db = PostgresqlDatabase('chemie', user='postgres', password='5545591pen',
                           host='localhost', port=5432)
                        
class BaseModel(Model):
    class Meta:
        database = pg_db
 
class Klass_opasnosti(BaseModel):
    ID = BigAutoField(null=False, column_name = "ID")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Класс опасности")

    class Meta:
        db_table = "klass_opasnosti"

class Preparativnaya_forma(BaseModel):
    ID = BigAutoField(null=False, column_name = "ID")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Препаративная форма")

    class Meta:
        db_table = "preparativnaya_forma"

class Gruppa_p(BaseModel):
    ID = BigAutoField(null=False, column_name = "ID")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Группа")

    class Meta:
        db_table = "gruppa_p"

class Pesticidy(BaseModel):
    kode = BigAutoField(null=False, column_name = "Код")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Наименование")
    FK_preparativnaya_forma = ForeignKeyField(Preparativnaya_forma, field="ID", column_name = "ID препаративная форма") 
    deystvuyushee_veshestvo = CharField(max_length=500, null=True, column_name = "Действующее вещество")
    soderzhanie_deystvuyushego_veshestva = CharField(max_length=500, null=True,column_name = "Содержание действующего вещества")
    registrant = CharField(max_length=256, null=True,column_name = "Регистрант")
    FK_klass_opasnosti = ForeignKeyField(Klass_opasnosti, field="ID", column_name = "ID класс опасности") 
    srok_registracii_Po = CharField(max_length=256, null=True,column_name = "Срок регистрации по")
    nomer_gosudarstvennoy_registracii = CharField(max_length=500, null=True, column_name = "Номер государственной регистрации")

    class Meta:
        db_table = "pesticidy"

class Gruppa_Pesticidy(BaseModel):
    preparat = ForeignKeyField(Pesticidy, field="kode", column_name = "FK пестицид") 
    gruppa = ForeignKeyField(Gruppa_p, field="ID", column_name = "FK группа") 

    class Meta:
        db_table = "gruppa_pesticidy"

class Instrukcia(BaseModel):
    id = BigAutoField(null=False, column_name = "ID")
    FK_kode = ForeignKeyField(Pesticidy, field="kode", column_name = "FK код пестицида") 
    FK_ID = ForeignKeyField(Gruppa_p, field="ID", column_name = "FK ID группы") 
    vrednyy_obekt_naznachenie = CharField(max_length=2000, null=True,column_name = "Вредный объект назначение")
    kultura_obrabatyvaemyy_obekt = CharField(max_length=2000, null=True, column_name = "Культура обрабатываемого объекта")
    sposob_i_vremya_obrabotki = CharField(max_length=2000, null=True, column_name = "Способ и время обработки")
    srok_ozhidaniya_krathost_obrabotok = CharField(max_length=2000, null=True,column_name = "Срок ожидания и кратость обработок")
    sroki_vyhoda_dlya_ruchyh_mehanizirovannyh_rabot = CharField(max_length=2000, null=True,column_name = "Сроки выхода для ручных и механизированных работ")
    norma_primeneniya_preparata_lga_kgga_lt_kgt = CharField(max_length=2000, null=True, column_name = "Норма применения препарата")

    class Meta:
        db_table = "instrukcia"

class Oblast(BaseModel):
    ID = BigAutoField(null=False, column_name = "ID")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Область")

    class Meta:
        db_table = "oblast"

class Gruppa_a(BaseModel):
    ID = BigAutoField(null=False, column_name = "ID")
    naimenovanie = CharField(max_length=500, null=True,column_name = "Группа")

    class Meta:
        db_table = "gruppa_a"

class Agrokhimikaty(BaseModel):
    kode = BigAutoField(null=False, column_name = "Код")
    rn = CharField(max_length=2000, null=True, column_name = "RN")
    FK_gruppa = ForeignKeyField(Gruppa_a, field="ID", column_name = "ID группа") 
    preparat = CharField(max_length=3000, null=True,column_name = "Препарат")
    marka = CharField(max_length=3000, null=True, column_name = "Марка")
    FK_oblast = ForeignKeyField(Oblast, field="ID", column_name = "ID область") 
    registrant = CharField(max_length=256, null=True,column_name = "Регистрант")
    srok_registracii_Po = CharField(max_length=256, null=True,column_name = "Срок регистрации по")

    class Meta:
        db_table = "agrokhimikaty"

pg_db.close()