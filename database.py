import sqlite3 as sql


class Database:
    def __init__(self, address):
        self.db = sql.connect(address)
        self.sql = self.db.cursor()

    def create_tables(self):
        self.sql.execute("""
        CREATE TABLE IF NOT EXISTS players
        (
        id INT,
        nickname TEXT,
        experience BIGINT,
        money BIGINT,
        job TEXT
        )""")

        self.db.commit()

    def insert_data(self, table, user_id, raw_data):
        self.sql.execute(f"INSERT INTO {table} VALUES (?, ?, ?, ?, ?)",
                         (user_id, raw_data[0], raw_data[1], raw_data[2], raw_data[3]))

        self.db.commit()

    def check_user(self, table, user_id):
        self.sql.execute(f"SELECT id FROM {table} WHERE id = {user_id}")
        if self.sql.fetchone() is None:
            return False

        return True

    def update_data(self, table, user_id, data, value):
        self.sql.execute(f"UPDATE {table} SET {data} = '{value}' WHERE id = {user_id}")
        self.db.commit()

    def wipe_data(self, table):
        self.sql.execute(f"DELETE FROM {table}")
        # self.sql.execute(f"DROP TABLE {table}")
        self.db.commit()

    def get_max_values(self, table, data, count):
        return self.sql.execute(f"SELECT * FROM {table} ORDER BY {data} DESC LIMIT {count}")

    def get_table(self, table):
        return self.sql.execute("SELECT * FROM {}".format(table))

    def run_command(self, command):
        self.sql.execute(command)
        self.db.commit()
