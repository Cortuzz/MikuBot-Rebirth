from math import log2, sqrt


class Player:
    def __init__(self, player_id, player_stats=False):
        self.id = player_id
        self.nickname = 'Unknown' if not player_stats else player_stats['nickname']

        self.experience = 1 if not player_stats else player_stats['experience']
        self.level = self.get_level()

        self.money = 1000 if not player_stats else player_stats['money']
        self.job = 'Отсутствует' if not player_stats else player_stats['job']

        self.stats = {"id": self.id, "nickname": self.nickname, "experience": self.experience,
                      "money": self.money, "level": self.level, "job": self.job}

    def get_stats(self):
        return self.stats

    def get_level(self):
        level = self.experience**(1/4) * log2(self.experience)**(1/4)
        return level if level < 80 else 80

    def change_value(self, value, difference, is_absolutely=False):
        if is_absolutely and difference < 0:
            return False
        if not is_absolutely and self.stats[value] + difference < 0:
            return False

        if is_absolutely:
            self.stats[value] = difference
        else:
            self.stats[value] += difference

        if value is "experience":
            self.level = self.get_level()

        return True
