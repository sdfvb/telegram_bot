import functools
import os

import psycopg2


class SQLighter:

    def base_connectiong(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        # DATABASE_URL = 'postgres://tarmlfqchphjjh:ab7f8ea16abf3b85eb5b261dbe2df7bdd20fc4c1dd9f13620d4e8b33a1078b9b@ec2-54-246-87-132.eu-west-1.compute.amazonaws.com:5432/da9dtbh5qu9e2t'
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        return connection

    def get_subscriptions(self, status='true'):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"SELECT * FROM subscribe WHERE status = '{status}'")
            return cursor.fetchall()

    def subscriber_exists(self, user_id):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"SELECT * FROM subscribe WHERE user_id = '{user_id}'")
            return bool(len(cursor.fetchall()))

    def get_last_field(self, user_id):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"SELECT topic, data FROM subscribe WHERE user_id = '{user_id}'")
        return cursor.fetchall()[0]

    def add_last_me(self, id, cource, date):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"""UPDATE subscribe SET topic = '{cource}', data = '{date}' WHERE user_id = '{id}' """)
            connection.commit()

    def add_subscriber(self, user_id, status=True):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"INSERT INTO subscribe (user_id, status) VALUES('{user_id}',{status})")
            connection.commit()

    def update_subscription(self, user_id, status):
        connection = self.base_connectiong()
        cursor = connection.cursor()
        with connection:
            cursor.execute(f"UPDATE subscribe SET status = {status} WHERE user_id = '{user_id}'")
            connection.commit()

#     def get_data(self, user_id, data):
#         connection = self.base_connectiong()
#         cursor = connection.cursor()
#         with connection:
#             cursor.execute(f"UPDATE subscribe SET data = '{data}' WHERE user_id = '{user_id}'")
#             connection.commit()
#
#
# new=SQLighter()
#
# new.get_data(753110279, '01-01-2020 10:10')
# new.get_data(824893928, '01-01-2020 10:10')