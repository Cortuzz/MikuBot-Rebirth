from database import Database


class DatabaseInterface:
    def __init__(self):
        self.db = Database("mmobot.db")
        self.db.create_tables()

        # self.db.wipe_data("players")
        # self.db.insert_data("players", 375795594, ("Cortuzz", 314324, 325254, "Сварщик"))

    def update_player_data(self, player_id, type, value):
        raw_data = 'Unknown', 1, 1000, 'Отсутствует'

        if not self.db.check_user("players", player_id):
            self.db.insert_data("players", player_id, raw_data)

        self.db.update_data("players", player_id, type, value)

    def print_data(self):
        for value in self.db.get_table("players"):
            print(value)
