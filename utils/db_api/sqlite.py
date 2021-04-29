import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None

        if commit:
            connection.commit()

        if fetchone:
            data = cursor.fetchone()

        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id int NOT NULL,
        name varchar(255) NOT NULL,
        email varchar(255),
        number_party int,
        time varchar(255),
        
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, name: str, email: str = None):
        sql = "INSERT INTO Users(id, name, email) VALUES(?, ?, ?)"

        parameters = (id, name, email)

        self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])

        return sql, tuple(parameters.values())

    def select_all_users(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        sql = "SELECT COUNT(*) FROM Users;"

        return self.execute(sql, fetchone=True)

    def update_user_time(self, time, id):

        sql = f"UPDATE Users SET time=? WHERE id=?"

        return self.execute(sql, parameters=(time, id), commit=True)

    def update_user_email(self, email, id):

        sql = f"UPDATE Users SET email=? WHERE id=?"

        return self.execute(sql, parameters=(email, id), commit=True)

    def update_number_party(self, number_party, id):

        sql = f"UPDATE Users SET number_party=? WHERE id=?"

        return self.execute(sql, parameters=(number_party, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def create_table_schedule_migraine(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Schedule (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        id_recording int NOT NULL,
        date varchar(255) NOT NULL,
        status varchar(255),
        FOREIGN KEY (id_recording) REFERENCES Users(id)
        );
        """
        self.execute(sql, commit=True)

    def add_recording(self, id_recording: int, date: str, status: str = None):
        sql = "INSERT INTO Schedule(id_recording, date, status) VALUES(?, ?, ?)"

        parameters = (id_recording, date, status)

        self.execute(sql, parameters=parameters, commit=True)

    def select_all_recording(self):
        sql = "SELECT * FROM Schedule"
        return self.execute(sql, fetchall=True)

    def select_record(self, **kwargs):
        sql = "SELECT * FROM Schedule WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)

    def delete_last_record(self):
        self.execute("DELETE FROM Schedule WHERE id = (SELECT id FROM Schedule ORDER BY id DESC LIMIT 1)",
                     commit=True)
        # self.execute("DELETE FROM Schedule WHERE TRUE", commit=True)