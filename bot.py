from API import VkAPI
from API import DebugAPI
from interface import BotInterface


class Bot:
    def __init__(self, group_id, token, debug):
        self.group_id = group_id
        self.token = token
        self.debug = debug

        self.api = DebugAPI(self.group_id, self.token)
        self.api = VkAPI(self.group_id, self.token)

        self.interface = BotInterface()
        self.handler = self.api.get_handler()

    def run(self):
        for event in self.handler:
            try:
                request = self.api.handle_request(event)
            except ValueError:
                continue

            user_id = self.api.get_user_id(event)
            chat_id = self.api.get_chat_id(event)

            self.get_response(request, user_id, chat_id)

    def get_response(self, request, player_id, chat_id):
        request = request.split()

        command = request[0]
        args = request[1:]

        text = self.interface.try_command(command, player_id, *args)
        if text is not None:
            self.api.response(text, player_id, chat_id)
