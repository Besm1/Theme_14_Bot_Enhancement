from sqlite3 import Connection, Cursor

connection = Connection('healthcare_shop.db')
cursor = connection.cursor()

ID = 0
TITLE = 1
DESCRIPTION = 2
PRICE = 3
IMG_FILE = 4

def initiate_db():
    try:
        rows_cnt = cursor.execute('select count(*) from Products').fetchone()
    except Exception as e:
        cursor.executescript('''
        create table if not exists Products (
            id INTEGER PRIMARY KEY
            , title text not null
            , description text
            , price int not null
            , img_file text
            );
        create table if not exists Users (
            id int,
            username text,
            email text,
            age int,
            balance int
            );
        
        ''')
        connection.commit()
        rows_cnt = cursor.execute('select count(*) from Products').fetchone()


    if not rows_cnt[0]:
        cursor.execute('''
            insert into Products 
          (title, description, price, img_file)
        values
          ('VARTIF Notien', 'Витамин для вартфнотов', 100, 'images\Product1.jpg')
          , ('BODPEARINER Pterox K.NRG', 'Витамин для бодов с Перинера', 200, 'images\Product2.jpg')
          , ('EOPITAMIC', 'Витамин Эопитам', 300, 'images\Product3.jpg')
          , ('RAFTFIADEON Bhe Ahcencl', 'БАД с моря Bhe планеты Ahcencl', 400, 'images\Product4.jpg')
        ''')
        connection.commit()


def get_all_products():
    return cursor.execute('select * from Products').fetchall()

