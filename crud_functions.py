from sqlite3 import Connection #, Cursor
import pprint

connection = Connection('healthcare_shop.db')
cursor = connection.cursor()

ID = 0
TITLE = 1
DESCRIPTION = 2
PRICE = 3
IMG_FILE = 4

U_USER_ID = 0
U_USERNAME = 1
U_EMAIL = 2
U_AGE = 3
U_BALANCE = 4
U_LOGGED_IN = 5
U_FIRST_NAME = 6
U_LAST_NAME = 7
U_LANG_CODE = 8
U_PASSWORD = 9


############ DB Init ##############
cursor.executescript('''
    create table if not exists Products (
        id INTEGER PRIMARY KEY
        , title text not null
        , description text
        , price int not null
        , img_file text
        );
    create table if not exists Users (
        user_id int,
        username text,
        email text,
        age int,
        balance int,
        logged_in int,
        first_name text,
        last_name text,
        lang_code text,
        password int);
    CREATE UNIQUE INDEX if not exists "idxUsers_user_id" ON "Users" ("user_id")
    ''')
connection.commit()

rows_cnt = cursor.execute('select count(*) from Products').fetchone()
if not rows_cnt[0]:
    cursor.execute('''
        insert into Products (title, description, price, img_file)
        values
          ('VARTIF Notien', 'Витамин для вартифнотов', 100, 'Product1.jpg')
          , ('BODPEARINER Pterox K.NRG', 'Витамин для бодов с Перинера', 200, 'Product2.jpg')
          , ('EOPITAMIC', 'Витамин Эопитам', 300, 'Product3.jpg')
          , ('RAFTFIADEON Bhe Ahcencl', 'БАД с моря Bhe планеты Ahcencl', 400, 'Product4.jpg')
    ''')
    connection.commit()

cursor.execute("update Users set logged_in = ?", (0,))
connection.commit()


############ Products ##############
def get_all_products():
    return cursor.execute('select * from Products').fetchall()


############ Users ###############
def get_all_users():
    return cursor.execute("SELECT * from Users").fetchall()

def start_user(from_user):
    if get_user_info(from_user.id):
        cursor.execute("update Users set logged_in = 1 where user_id = ?", (from_user.id,))
    else:
        cursor.execute(f"insert into Users ( user_id, username, logged_in, first_name, Last_name, lang_code)"
                       f"values(?, ?, ?, ?, ?, ?)",
                       (from_user.id, from_user.username, 1, from_user.first_name,
                        from_user.last_name, from_user.language_code))
    connection.commit()
    return

def exit_user(user_id: int):
    cursor.execute(f"update Users set logged_in = 0 where user_id = ?", (user_id,))
    connection.commit()

def is_logged_in(user_id):
    try: return get_user_info(user_id)[U_LOGGED_IN]
    except Exception: return False

def is_registered(user_id):
    return get_user_info(user_id)[U_EMAIL] is not None

def get_user_info(user_id):
    return cursor.execute("select * from Users where user_id = ?", (user_id, )).fetchone()

def register_user(user_id, username, email, age):
    cursor.execute("update Users set UserName = ?, email = ?, age = ?, logged_in = ?, balance = ? where user_id = ?",
                   (username, email, age, 1, 1000, user_id))
    connection.commit()

def user_exists(username) -> bool:
    return cursor.execute("select count(*) from Users where username = ?", (username,)).fetchone()[0]

if __name__ == '__main__':
    ui = get_user_info(15)
    if not ui:
        print("No such user")
    else:
        print(ui)