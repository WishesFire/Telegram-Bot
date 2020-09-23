import psycopg2

class DataBase_users:
    def __init__(self):
        self.root_connect = psycopg2.connect(database='postgres', user='*', password='*',
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

    def get_using_set(self, tg_ids):
        self.curs.execute(f'SELECT using_set FROM users WHERE user_id = {tg_ids}')
        return self.curs.fetchone()[0]

    def change_using_set(self, tg_ids, num):
        self.curs.execute(f'UPDATE users set using_set = {num} where user_id = {tg_ids}')
        self.root_connect.commit()

    def change_data(self, tg_ids, text):
        self.curs.execute(f"UPDATE users set words_time = '{text}' where user_id = {tg_ids}")
        self.root_connect.commit()

    def change_count(self, tg_ids, count):
        self.curs.execute(f"UPDATE users set count_word = {count} where user_id = {tg_ids}")
        self.root_connect.commit()

    def get_all_users(self):
        self.curs.execute('SELECT user_id FROM users')
        row = self.curs.fetchall()
        return row

    def user_for_time(self, user):
        self.curs.execute(f"SELECT words_time, count_word from users where user_id = {user}")
        rows = self.curs.fetchone()
        return rows

    def delete_user(self, tg_id):
        self.curs.execute(f"DELETE from users where user_id= {tg_id}")
        self.root_connect.commit()

    def delete_all_user(self):
        self.curs.execute("DELETE from users")
        self.root_connect.commit()

    def connect_close(self):
        self.root_connect.close()
        print('Database close')


#c = DataBase_users()
#print(c.get_using_set())
#c.connect_close()

#c = DataBase_users()
#c.delete_all_user()
#c.connect_close()