import traceback
from database import Database


class DatabaseInterface:
    def __init__(self):
        self.db = Database("mmobot.db")
        self.db.create_tables()

    def get_max(self, data):
        return self.db.get_max_values("players", data, 5)

    def update_player_data(self, player_id, type, value):
        raw_data = 'Unknown', 1, 1000, 'Отсутствует'

        if not self.db.check_user("players", player_id):
            self.db.insert_data("players", player_id, raw_data)

        self.db.update_data("players", player_id, type, value)

    def print_data(self):
        for value in self.db.get_table("players"):
            print(value)

    def raw_sql_input(self, command):
        response = "SQL request completed."
        try:
            self.db.run_command(command)
        except:
            return "SQL request rejected.\n" + traceback.format_exc()

        for val in self.db.get_table("players"):
            response += "\n" + str(val)

        return response
