from sqlite3 import Connection, Cursor

connection = Connection('healthcare_shop.db')
cursor = connection.cursor()

ID = 0
TITLE = 1
DESCRIPTION = 2
PRICE = 3
IMG_FILE = 4

U_ID = 0
U_USERNAME = 1
U_EMAIL = 2
U_AGE = 3
U_BALANCE = 4
U_LOGGED_IN = 5
U_USER_ID = 6
U_FIRST_NAME = 7
U_LAST_NAME = 8
U_LANG_CODE = 9
U_PASSWORD = 10


def initiate_db():
    try:
        rows_cnt = cursor.execute('select count(*) from Products').fetchone()
        rows_cnt = cursor.execute('select count(*) from Users').fetchone()
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
            id INTEGER PRIMARY KEY,
            username text,
            email text,
            age int,
            balance int,
            logged_in int,
            user_id int,
            first_name text,
            last_name text,
            lang_code text,
            password int
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

    cursor.execute("update Users set logged_in = ?", (0,))
    connection.commit()


############ Products ##############
def get_all_products():
    return cursor.execute('select * from Products').fetchall()


############ Users ###############
def start_user(from_user):
    if not cursor.execute("select count(*) from Users where user_id = ?",
                          (from_user.id,)).fetchone()[0]:
        cursor.execute(f"insert into Users (username, logged_in, user_id, first_name, Last_name, lang_code)"
                       f"values(?, ?, ?, ?, ?, ?)",
                       (from_user.username, 1, from_user.id, from_user.first_name,
                        from_user.last_name, from_user.language_code))
    else:
        cursor.execute("update Users set logged_in = 1 where user_id = ?", (from_user.id,))
    connection.commit()
    return get_user_info(from_user.id)

def exit_user(user_id: int):
    cursor.execute(f"update Users set logged_in = 0 where user_id = ?", (user_id,))
    connection.commit()

def is_logged_in(user_id):
    try:
        return cursor.execute(f"select logged_in from Users where user_id = ?", (user_id,)).fetchone()[0]
    except TypeError:
        return False

def is_registered(user_id):
    return cursor.execute("select age from Users where user_id = ?", (user_id,)).fetchone()[0]

def get_user_info(user_id):
    return cursor.execute("select * from Users where user_id = ?", (user_id, )).fetchone()

def register_user(user_id, username, email, age):
    cursor.execute("update Users set UserName = ?, email = ?, age = ?, logged_in = ?, balance = ? where user_id = ?",
                   (username, email, age, 1, 1000, user_id))
    connection.commit()


