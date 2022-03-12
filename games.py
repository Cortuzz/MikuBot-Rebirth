from random import randint, choice


class Casino:
    def __init__(self):
        self.blackjack_players = dict()

    def add_blackjack_player(self, player_id, bet):
        game = BlackJack(bet)
        self.blackjack_players.update({player_id: game})

    def get_blackjack_players(self):
        return self.blackjack_players

    def remove_blackjack_player(self, player_id):
        self.blackjack_players.pop(player_id)

    def roulette(self, bet, prediction):
        if isinstance(prediction, int):
            place = int(prediction)

        bet_multiplier = 0
        colors = 'ч', 'к'
        evens = 'чет', 'нечет'

        numbers = 0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, \
                  10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26

        ball_place = randint(0, 36)
        ball_value = numbers[ball_place]
        color = 'з'
        even = None

        if ball_value:
            color = colors[ball_place % 2]
            even = evens[ball_value % 2]

        if prediction in (color, even):
            bet_multiplier = 2

        if prediction == ball_value:
            bet_multiplier = 36

        return bet * bet_multiplier, ball_value, color

    def slot_machine(self, bet):
        symbols = '🍒' * 5 + '🍓' * 5 + '💥' * 3 + '⭐' * 2 + '💎'
        symbols_double_worth = {'🍒': 1, '🍓': 2, '💥': 3, '⭐': 5, '💎': 7}
        symbols_triple_worth = {'🍒': 4, '🍓': 8, '💥': 10, '⭐': 20, '💎': 100}
        rows = []
        string_rows = ""

        for i in range(3):
            rows.append([])
            for j in range(3):
                symbol = choice(symbols)
                rows[i].append(symbol)
                string_rows += symbol + " "
            string_rows += "\n"

        win_line = rows[1]
        if (win_line[0] == win_line[1] == win_line[2]):
            return bet * symbols_triple_worth[win_line[0]], string_rows

        for i in range(3):
            for j in range(i + 1, 3):
                if win_line[i] == win_line[j]:
                    return bet * symbols_double_worth[win_line[i]], string_rows

        return 0, string_rows

class BlackJack:
    def __init__(self, bet):
        self.first_action = True
        self.bet = bet
        self.is_blackjack = False

        suits = '♠', '♥', '♦', '♣'
        numbers = [i for i in range(2, 15)]

        self.cards_replace = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        for i in range(2, 10):
            self.cards_replace.update({i: str(i)})

        self.deck = list()
        for i in range(len(numbers)):
            for j in range(len(suits)):
                self.deck.append(self.cards_replace[numbers[i]] + suits[j])

        self.cards = [choice(self.deck), choice(self.deck)]
        self.dealer_cards = [choice(self.deck)]

    def __calculate_score(self, cards):
        score = 0
        is_ace = False

        for card in cards:
            card_value = self.__score(card)
            score += card_value

            if card_value == 11:
                is_ace = True

            if score > 21 and is_ace:
                score -= 10
                is_ace = False

        return score

    def __score(self, card):
        points = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  'T': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

        card_value = points[card[0]]
        return card_value

    def get_dealer_cards(self):
        while True:
            if self.__calculate_score(self.dealer_cards) >= 17:
                break

            self.dealer_cards.append(choice(self.deck))

    def deal_card(self):
        self.first_action = False
        card = choice(self.deck)
        self.cards += [card]

        return card

    def get_data(self):
        player_bj = False
        dealer_bj = False

        score = self.__calculate_score(self.cards)
        dealer_score = self.__calculate_score(self.dealer_cards)

        if len(self.cards) == 2 and score == 21:
            player_bj = True

        if len(self.dealer_cards) == 2 and dealer_score == 21:
            dealer_bj = True

        return score, self.cards, self.dealer_cards, dealer_score, player_bj, dealer_bj


casino = Casino()
casino.slot_machine(300)
