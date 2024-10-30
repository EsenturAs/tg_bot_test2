import sqlite3


class Database:

    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS homeworks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    group_number TEXT,
                    hw_number INTEGER,
                    github_link TEXT
                    )
            """)
            connection.commit()

    def execution(self, sql, parameters=None):
        with sqlite3.connect(self.path) as connection:
            if parameters is not None:
                connection.execute(sql, parameters)
            else:
                connection.execute(sql)
            connection.commit()

    def fetch(self, sql, parameters=None):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            if parameters is not None:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)
            data = cursor.fetchall()
            return data
