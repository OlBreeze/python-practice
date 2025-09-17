import sqlite3


class DataConn:  # usage

    def __init__(self, db_name):
        """Ініціалізатор"""
        self.db_name = db_name

    def __enter__(self):
        """
        Відкриваємо підключення з базою даних.
        """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Закриваємо підключення.
        """
        self.conn.close()
        if exc_val:
            raise


if __name__ == '__main__':
    db = 'test.db'

    with DataConn(db) as conn:
        cursor = conn.cursor()