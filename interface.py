import locale
from player import Player
from games import Casino
from database_interface import DatabaseInterface


class BotInterface:
    def __init__(self):
        locale.setlocale(locale.LC_ALL, '')
        self.commands = {'профиль': self.get_profile, 'рулетка': self.roulette}
        self.players = dict()
        self.db_interface = DatabaseInterface()
        self.db_interface.print_data()

        self.debug_player()
        self.save_data()
        self.db_interface.print_data()

    def debug_player(self):
        pl = Player(375795594,
                    {'nickname': 'Cortuzz', 'experience': 4311, 'money': 2431345, 'job': 'Сварщик'})

        self.players.update({375795594: pl})

    def get_player(self, player_id):
        return self.players[player_id]

    def add_player(self, player_id):
        player = Player(player_id)
        self.players.update({player_id: player})

    def try_command(self, command, player_id, *args):
        if player_id not in self.players:
            self.add_player(player_id)

        player = self.get_player(player_id)
        method = self.commands[command]

        if len(args):
            return method(player, args)

        return method(player)

    def format_values(self, value):
        return locale.format_string('%d', value, grouping=True)

    def get_profile(self, player):
        localization = {
                        'level': '🌟 Уровень', 'nickname': '👤 Никнейм',
                        'luck': '🍀 Удача', 'job': '💼 Работа',
                        'money': '💰 Наличные'
        }

        formatting = {'level': int, 'money': self.format_values}

        measurement = {'level': '', 'nickname': '', 'job': '', 'money': '₽', 'currency': '$', 'bank': '$',
                       'health': '%', 'food': '%', 'water': '%', 'energy': '%', 'luck': '%'}

        response = "Ваш профиль:\n"
        player_stats = player.get_stats()
        for stat in player_stats:
            value = player_stats[stat]
            try:
                try:
                    format_ = formatting[stat]
                    value = format_(value)
                except KeyError:
                    pass

                response += "{}: {}{}\n".format(localization[stat], value, measurement[stat])
            except KeyError:
                pass

        return response

    def roulette(self, player, args):
        if len(args) != 2:
            return 'Укажите ставку и значение [номер/четность/цвет].'

        bet, value = args[0], args[1]
        bet = self.convert_bets(player, bet)

        if not bet:
            return 'Неверная ставка.'

        try:
            value = int(value)
            if not (0 <= value <= 36):
                return 'Укажите ячейку от 0 до 36.'
        except ValueError:
            if value not in ('чет', 'нечет', 'к', 'ч'):
                return 'Неверные данные.'

        if not player.change_value('money', -bet):
            return 'Недостаточно средств.'

        color = {'к': '🔴', 'ч': '⚫', 'з': '🟢'}
        casino = Casino()
        data = casino.roulette(bet, value)
        text = 'Выпадает {} {}\n'.format(data[1], color[data[2]])

        if data[0]:
            text += 'Вы выиграли {}$.'.format(self.format_values(data[0] - bet))
            player.change_value('money', data[0])

        else:
            text += 'Ваша ставка сгорела.'

        return text

    def convert_bets(self, player, bet):
        money = player.get_stats()['money']
        if bet in ('все', 'всё'):
            return money
        elif bet[:2] == '1/':
            try:
                bet = int(bet[2:])
            except ValueError:
                return False

            return money // bet
        elif bet[-1:] == 'к':
            count = 0
            for i in range(1, 100):
                if bet[-i] == 'к':
                    count += 1
                else:
                    break

            try:
                bet = int(bet[:-count]) * 1000**count
            except ValueError:
                return False

        try:
            bet = int(bet)
        except ValueError:
            return False

        if bet <= 0:
            return False

        return bet

    def save_data(self):
        savable = 'nickname', 'experience', 'money', 'job'
        for player_id in self.players:
            player = self.players[player_id]
            stats = player.get_stats()

            for stat in stats:
                if stat in savable:
                    self.db_interface.update_player_data(player_id, stat, stats[stat])
