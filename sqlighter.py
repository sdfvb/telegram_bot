import functools
import os

import psycopg2


class SQLighter:

    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        # URI
        # DATABASE_URL = 'postgres://tarmlfqchphjjh:ab7f8ea16abf3b85eb5b261dbe2df7bdd20fc4c1dd9f13620d4e8b33a1078b9b@ec2-54-246-87-132.eu-west-1.compute.amazonaws.com:5432/da9dtbh5qu9e2t'
        # self.connection = psycopg2.connect(
        #     host='ec2-54-246-87-132.eu-west-1.compute.amazonaws.com',
        #     database='da9dtbh5qu9e2t',
        #     user='tarmlfqchphjjh',
        #     password='ab7f8ea16abf3b85eb5b261dbe2df7bdd20fc4c1dd9f13620d4e8b33a1078b9b'
        # )

        pass

    def base_connectiong(self):
        # DATABASE_URL = os.environ['DATABASE_URL']
        DATABASE_URL = 'postgres://tarmlfqchphjjh:ab7f8ea16abf3b85eb5b261dbe2df7bdd20fc4c1dd9f13620d4e8b33a1078b9b@ec2-54-246-87-132.eu-west-1.compute.amazonaws.com:5432/da9dtbh5qu9e2t'

        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status='true'):
        self.base_connectiong()
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscribe WHERE status = '{status}'")
            return self.cursor.fetchall()

    def subscriber_exists(self, user_id):
        self.base_connectiong()
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            self.cursor.execute(f"SELECT * FROM subscribe WHERE user_id = '{user_id}'")
            return bool(len(self.cursor.fetchall()))

    def get_last_field(self, user_id):
        self.base_connectiong()
        self.cursor.execute(f"SELECT topic FROM subscribe WHERE user_id = '{user_id}'")
        self.close()
        return self.cursor.fetchall()[0][0]

    def add_last_me(self, id, cource):
        self.base_connectiong()
        self.cursor.execute(f"""UPDATE subscribe 
                            SET topic = '{cource}' WHERE user_id = '{id}' """)
        self.connection.commit()
        self.close()

    def get_rows(self):
        self.base_connectiong()
        self.cursor.execute(f"SELECT * FROM subscribe")
        print(self.cursor.fetchall())
        self.close()

    def add_subscriber(self, user_id, status=True):
        self.base_connectiong()
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO subscribe (user_id, status) VALUES('{user_id}',{status})")

    def update_subscription(self, user_id, status):
        self.base_connectiong()
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute(f"UPDATE subscribe SET status = {status} WHERE user_id = '{user_id}'")

    def delete_all(self):
        self.base_connectiong()
        self.cursor.execute("DELETE FROM subscribe")
        self.connection.commit()
        self.close()
        return

    def delete_table(self):
        self.base_connectiong()
        self.cursor.execute("DROP TABLE  subscribe")
        self.connection.commit()
        self.close()
        return

    def name_table(self):
        self.base_connectiong()
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');")
        print(self.cursor.fetchall)
        self.close()

    def create_table(self):
        self.base_connectiong()
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
        self.base_connectiong()
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
