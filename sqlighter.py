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
            return self.cursor.execute("SELECT * FROM subscriptions WHERE status = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status=True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO subscriptions (user_id, status) VALUES(?,?)",
                                       (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE subscriptions SET status = ? WHERE user_id = ?", (status, user_id))

    def delete_all(self):
        self.cursor.execute("DELETE FROM subscriptions")
        self.connection.commit()
        return

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

