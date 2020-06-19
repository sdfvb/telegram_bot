import psycopg2


class SQLighter:

    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""


        self.connection = psycopg2.connect(
            host='ec2-54-246-87-132.eu-west-1.compute.amazonaws.com',
            database='da9dtbh5qu9e2t',
            user='tarmlfqchphjjh',
            password='ab7f8ea16abf3b85eb5b261dbe2df7bdd20fc4c1dd9f13620d4e8b33a1078b9b'
        )
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status='true'):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscribe WHERE status = '{status}'")
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscribe WHERE user_id = '{user_id}'")
            return bool(len(self.cursor.fetchall()))

    def get_last_field(self, user_id):
        self.cursor.execute(f"SELECT topic FROM subscribe WHERE user_id = '{user_id}'")
        return self.cursor.fetchall()[0][0]

    def add_last_me(self, id, cource):
        self.cursor.execute(f"""UPDATE subscribe 
                            SET topic = '{cource}' WHERE user_id = '{id}' """)
        self.connection.commit()

    def get_rows(self):
        self.cursor.execute(f"SELECT * FROM subscribe")
        print(self.cursor.fetchall())

    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO subscribe (user_id, status) VALUES('{user_id}',{status})")


    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(f"UPDATE subscribe SET status = {status} WHERE user_id = '{user_id}'")


    def delete_all(self):
        self.cursor.execute("DELETE FROM subscribe")
        self.connection.commit()
        return

    def delete_table(self):
        self.cursor.execute("DROP TABLE  subscribe")
        self.connection.commit()
        return




    def name_table(self):
        self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');")
        print(self.cursor.fetchall)

    def create_table(self):
        self.cursor.execute("""  CREATE TABLE subscribe(
                                user_id serial PRIMARY KEY,
                                status VARCHAR (5) NOT NULL,
                                topic TEXT
                            );""")
#
#         self.cursor.execute("""ALTER TABLE subscriptions
# ADD COLUMN topic TEXT""")
        self.connection.commit()


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

# new = SQLighter()
# # new.create_table()
# # # # # # # new.delete_all()
# print(new.add_last_me(824893928, 'Оптимизация блоков'))
# #
# # new.create_table()
# print(new.get_subscriptions())
# print(new.get_rows())