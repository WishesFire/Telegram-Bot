import psycopg2
import os
import random

class DataBase_words:
    def __init__(self):
        # info database
        self.root_connect = psycopg2.connect(database='postgres', user='*',
                                        password='*', host='127.0.0.1', port='5432')
        self.curs = self.root_connect.cursor()
        print("Database opened successfully")

    def create_db(self):
        self.curs.execute("CREATE TABLE english_words_date (id serial PRIMARY KEY, eng_word TEXT NOT NULL, rus_word TEXT NOT NULL)")
        print("Table created successfully")
        self.root_connect.commit()

    def push_date(self):
        path = os.getcwd()
        with open(f'{path}\\kk.csv') as p:
            self.curs.copy_from(p, 'english_words_date', sep=',')
        print('Pushed data successfully')
        self.root_connect.commit()

    def request_random_word(self):
        random_id = tuple(random.randint(1, 51380) for i in range(5))
        self.curs.execute(f"SELECT eng_word, rus_word from english_words_date where id in {random_id}")
        row = self.curs.fetchall()
        return row

    def delete_date(self):
        self.curs.execute('DELETE FROM english_words_date')
        self.root_connect.commit()

    def connect_close(self):
        self.root_connect.close()


#c = DataBase_words()
#c.request_random_word()
#c.connect_close()