import psycopg2

class DataBase_users:
    def __init__(self):
        self.root_connect = psycopg2.connect(database='postgres', user='', password='',
                                             host='127.0.0.1', port='5432')
        self.curs = self.root_connect.cursor()
        print('Database opened successfully')

    def create_db(self):
        self.curs.execute("CREATE TABLE users (user_id serial PRIMARY KEY, words_time TEXT NOT NULL,"
                          " count_word INTEGER, using_set INTEGER)")
        print("Table created successfully")
        self.root_connect.commit()

    def push_date(self, tg_id, w_time, c_words, using=1):

        self.curs.execute(f"INSERT INTO users (user_id, words_time, count_word, using_set) "
                          f"VALUES ({tg_id}, '{w_time}', {c_words}, {using})")
        self.root_connect.commit()

    def user_check(self, tg_ids):
        self.curs.execute(f"SELECT exists (SELECT 1 FROM users WHERE user_id = {tg_ids})")
        return self.curs.fetchone()[0]

    def delete_user(self):
        self.curs.execute("DELETE from users where user_id=576178407")
        self.root_connect.commit()

    def connect_close(self):
        self.root_connect.close()
        print('Database close')
