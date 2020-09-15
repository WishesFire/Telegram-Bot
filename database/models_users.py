import psycopg2

class DataBase_users:
    def __init__(self):
        self.root_connect = psycopg2.connect(database='*', user='*', password='*',
                                             host='*', port='*')
        self.curs = self.root_connect.cursor()
        print('Database opened successfully')

    def create_db(self):
        self.curs.execute("CREATE TABLE users (user_id serial PRIMARY KEY, words_time TEXT NOT NULL, count INTEGER, using INTEGER)")
        print("Table created successfully")
        self.root_connect.commit()

    def push_date(self, user_id, words_time, using=1):
        self.curs.execute()


    def connect_close(self):
        self.root_connect.close()


c = DataBase_users()
c.create_db()
c.connect_close()
