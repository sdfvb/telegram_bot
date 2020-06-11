import psycopg2


class SQLighter:

    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""


        self.connection = psycopg2.connect(
            host='ec2-54-75-246-118.eu-west-1.compute.amazonaws.com',
            database='d257do0tk4c4e6',
            user='hnchjioxmlmwrz',
            password='dd3d8f890ebe96f0b4f64bb9cd6ad19aeb441ad8c0ad233d6b3c6e76df423aa7'
        )
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM subscribe WHERE status = {status}")

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
        # print(self.cursor.fetchall())

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
                                status VARCHAR (50) UNIQUE NOT NULL,
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
# # # # # # new.delete_all()
# print(new.get_last_field(824893928))
# # #
# # new.create_table()
